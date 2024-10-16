import docker
import os
from pathlib import Path
from docker.errors import BuildError, ImageNotFound, APIError
from docker.models.images import Image
from docker.models.containers import Container
import tempfile
import shutil
import os

from typing import List
from tests4py.projects import Project

from debugging_framework.docker import get_base_dockerfile, get_docker_runner_files

BASE_IMAGE_TAG = 'base_image'


def copy_files_to_temp(src_files, temp_dir):
    for file in src_files:
        shutil.copy(file, temp_dir)


class DockerManagerNew:

    def __init__(self, project: Project):
        self.base_image = None
        self.image = None
        self.docker_socket = self._configure_docker_socket()
        # self.client = docker.from_env()
        self.client = docker.DockerClient(base_url=self.docker_socket)
        self.container: List[Container] = []
        self.dockerfile_path = None

        self.project: Project = project

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def _configure_docker_socket():
        if os.path.exists("/var/run/docker.sock"):
            docker_socket = "unix:///var/run/docker.sock"
        else:
            user = os.environ.get("USER")
            if os.path.exists(f"/Users/{user}/.docker/run/docker.sock"):
                docker_socket = f"unix:///Users/{user}/.docker/run/docker.sock"
            else:
                raise FileNotFoundError(
                    (
                        "Neither '/var/run/docker.sock' nor '/Users/<USER>/.docker/run/docker.sock' are available."
                        "Please make sure you have Docker installed and running."
                    )
                )
        os.environ["DOCKER_HOST"] = docker_socket
        return docker_socket

    def _image_exists(self, image_tag: str) -> Image | None:
        try:
            return self.client.images.get(image_tag)
        except ImageNotFound:
            return None

    def _build_image(self, path_to_docker_dir: str, dockerfile: str, image_tag: str) -> Image:
        try:
            image, build_logs = self.client.images.build(
                path=path_to_docker_dir,
                dockerfile=dockerfile,
                tag=image_tag,
                rm=True
            )
            for chunk in build_logs:
                if 'stream' in chunk:
                    print(chunk['stream'].strip())
            return image
        except BuildError as e:
            print(f"Build failed: {e}")
            self.cleanup()
            raise

    def build_image(self, path_to_docker_dir: str, image_tag: str, dockerfile: str = "Dockerfile") -> Image:
        image = self._image_exists(image_tag)
        if not image:
            return self._build_image(path_to_docker_dir, dockerfile, image_tag)
        print(f"Image {image_tag} already exists. Skipping build.")
        return image

    def build(self):
        # build base image
        base_dockerfile = get_base_dockerfile()
        base_dockerfile_name = str(base_dockerfile.name)
        base_dockerfile_path = str(base_dockerfile.parent)

        base_image = self.build_image(path_to_docker_dir=base_dockerfile_path, image_tag=BASE_IMAGE_TAG, dockerfile=base_dockerfile_name)
        self.base_image = base_image

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            print("Temporary directory created at:", temp_dir)

            # build subject image
            subject_image_tag = f'{self.project.get_identifier()}_image'
            subject_dockerfile_name = f'Dockerfile.{self.project.get_identifier()}'

            dockerfile_file_location = temp_dir + "/" + subject_dockerfile_name
            self._create_subject_dockerfile(dockerfile_file_location)

            # Copy files to the temporary directory
            copy_files_to_temp(get_docker_runner_files(), temp_dir)
            print(f"Files {get_docker_runner_files()} copied to temporary directory.")

            # Perform build operations
            self.image = self.build_image(path_to_docker_dir=temp_dir, image_tag=subject_image_tag, dockerfile=subject_dockerfile_name)

    def build_container(self, number_of_containers: int):
        container_name = f'{self.project.get_identifier()}_container'
        for i in range(number_of_containers):
            self._create_container(container_name=f'{container_name}_{i}')

    def _create_container(self, container_name=None):
        if not self.image:
            raise RuntimeError("Image has not been built. Call build() first.")
        try:
            container = self.client.containers.create(
                self.image.id,
                name=container_name,
                detach=True,
                tty=True,
                stdin_open=True,
            )
            container.start()

            self.container.append(container)
        except APIError as e:
            print(f"Error creating container: {e}")
            self.cleanup()
            raise

    def cleanup(self):
        for container in self.container:
            try:
                container.kill()
                container.remove()
            except docker.errors.NotFound:
                print("Container already removed.")
            except Exception as e:
                print(f"Error during container cleanup: {e}")

    def _run_container(self, container):
        try:
            exec_result = container.exec_run(["python3", "docker_runner.py"], tty=True)
            print(exec_result.output.decode('utf-8'))
        except Exception as e:
            print(f"Error executing command in container: {e}")
            self.cleanup()
            raise

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.container)) as executor:
            futures = [
                executor.submit(
                    self._run_container,
                    container
                )
                for container in self.container
            ]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Container run failed: {e}")

    def _create_subject_dockerfile(self, file_location: str):
        dockerfile = f'''FROM {BASE_IMAGE_TAG}

# Install python using pyenv
RUN bash -c "source ~/.bashrc && pyenv install {self.project.python_version}"

COPY ./docker_setup.py /app
COPY ./docker_runner.py /app

RUN bash -c "python3 docker_setup.py {self.project.project_name} {self.project.bug_id}"

# Set the command to keep the container running
CMD ["tail", "-f", "/dev/null"]
'''
        with open(file_location, 'w') as file:
            file.write(dockerfile)


class DockerManager:
    def __init__(self, image_tag="my_python_app", container_name="my_python_app_container"):
        self.client = docker.from_env()
        self.image_tag = image_tag
        self.container_name = container_name
        self.container = None
        self.image = None
        self.dockerfile_path = None

    def _image_exists(self, image_tag):
        try:
            self.client.images.get(image_tag)
            return True
        except ImageNotFound:
            return False

    def _build_image(self, dir_path=".", dockerfile=None, image_name="tests4py_base_image"):
        try:
            self.image, build_logs = self.client.images.build(
                path=dir_path,
                dockerfile=dockerfile,
                tag=image_name,
                rm=True
            )
            for chunk in build_logs:
                if 'stream' in chunk:
                    print(chunk['stream'].strip())
        except BuildError as e:
            print(f"Build failed: {e}")
            self.cleanup()
            raise

    def build(self, dir_path=".", dockerfile=None, image_name="tests4py_base_image"):
        if self._image_exists(image_name):
            print(f"Image {image_name} already exists. Skipping build.")
        else:
            self._build_image(dir_path, dockerfile, image_name)

    def _write_files(self):
        dockerfile = '''
        FROM python:3.12
        WORKDIR /app
        COPY script.py .
        COPY requirements.txt .
        # RUN if [ -s requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
        # CMD ["/bin/bash"]
        # ENTRYPOINT ["/bin/bash"]
        CMD ["tail", "-f", "/dev/null"]
        '''
        with open('Dockerfile', 'w') as file:
            file.write(dockerfile)

        script = '''import sys
message = sys.argv[1] if len(sys.argv) > 1 else "No message provided"
print(f"Message from the host: {message}")
        '''
        with open('script.py', 'w') as file:
            file.write(script)

        requirements = '''
        # Add your required Python packages here
        '''
        with open('../../debugging_benchmark/tests4py_benchmark/resources/requirements.txt', 'w') as file:
            file.write(requirements)

    def run(self, image_tag, container_name=None):
        if not self._image_exists(image_tag):
            raise RuntimeError("Image has not been built. Call build() first.")
        container = None
        try:
            cmd = ["python3", "-c", "print('12')"]
            cmd = ["t4p", "systemtest", "test", "-p", "./tmp/pysnooper_2/tests4py_systemtest_diversity"]
            image = self.client.images.get(image_tag)

            container = self.client.containers.create(
                image.id,
                name=container_name,
                detach=True,
                command=cmd,
            )
            container.start()
            logs = container.logs(stream=True)
            for log in logs:
                print(log.strip().decode('utf-8'))
        except Exception as e:
            print(f"Error running container: {e}")
            raise
        finally:
            if container:
                container.remove(force=True)

    def cleanup(self):
        # Stop and remove containers with the specific label
        try:
            #self.container.kill()
            #self.container.remove()
            pass
        except docker.errors.NotFound:
            print("Container already removed.")
        except Exception as e:
            print(f"Error during container cleanup: {e}")
        # Remove the image if it exists
        if self.image:
            try:
                pass
                # self.client.images.remove(self.image.id, force=True)
            except docker.errors.ImageNotFound:
                print("Image already removed.")
            except Exception as e:
                print(f"Error during image cleanup: {e}")
        # Remove the temporary files
        for file in ['Dockerfile', 'script.py', 'requirements.txt']:
            if os.path.exists(file):
                os.remove(file)

    def create_container(self, image_tag, container_name=None):
        if not self._image_exists(image_tag):
            raise RuntimeError("Image has not been built. Call build() first.")
        try:
            image = self.client.images.get(image_tag)

            container = self.client.containers.create(
                image.id,
                name=container_name,
                detach=True,
                tty=True,
                stdin_open=True,
            )
            container.start()
        except APIError as e:
            print(f"Error creating container: {e}")
            self.cleanup()
            raise

    def exec_command(self, message="Hello from inside the container!"):
        if not self.container:
            raise RuntimeError("Container has not been created. Call create_container() first.")
        try:
            exec_result = self.container.exec_run(["python3", "/app/script.py", message], tty=True)
            print(exec_result.output.decode('utf-8'))
        except Exception as e:
            print(f"Error executing command in container: {e}")
            self.cleanup()
            raise

    @staticmethod
    def write_subject_dockerfile(subject):
        dockerfile = f'''FROM tests4py_base_image

# Install python using pyenv
RUN bash -c "source ~/.bashrc && pyenv install {subject["pyenv-version"]} # && pyenv global {subject["pyenv-version"]}"

# RUN bash -c "t4p checkout -p {subject["project_name"]} -i {subject["bug_ids"][0]}"
# RUN bash -c "t4p build" 

COPY ./docker_setup.py /app

# RUN bash -c "python3 docker_setup.py {subject["project_name"]} {subject["bug_ids"][0]}"

RUN bash -c "python3 docker_setup.py"

# Set the command to keep the container running
CMD ["tail", "-f", "/dev/null"]
'''
        with open(f'Dockerfile.{subject["project_name"]}', 'w') as file:
            file.write(dockerfile)


import concurrent.futures


def run_container(manager, image_tag, container_name):
    manager.run(image_tag=image_tag, container_name=container_name)


def parallel_run(manager, subject, num_containers=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_containers) as executor:
        futures = [
            executor.submit(
                run_container,
                manager,
                f'{subject["project_name"]}_image',
                f'{subject["project_name"]}_container_{i}'
            )
            for i in range(num_containers)
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Container run failed: {e}")


if __name__ == "__main__":
    subject_dir = {
        "pysnooper": {"project_name": "pysnooper", "bug_ids": [2, 3], "pyenv-version": "3.8.4"},
        "fastapi": {"project_name": "fastapi", "bug_ids": [1], "pyenv-version": "3.8.3"},
    }

    subject = subject_dir["pysnooper"]

    manager = DockerManager()
    try:
        manager.build(dockerfile='Dockerfile.base')
        manager.write_subject_dockerfile(subject)
        manager.build(dockerfile=f'Dockerfile.{subject["project_name"]}', image_name=f'{subject["project_name"]}_image')

        parallel_run(manager, subject, num_containers=7)

        # manager.create_container(image_tag=f'{subject["project_name"]}_image', container_name=f'{subject["project_name"]}_container_')

        # for i in range(100):
        #     manager.exec_command(message=f"{i}: Hello from the host!")
    finally:
        manager.cleanup()
