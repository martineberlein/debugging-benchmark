import docker
import os
from pathlib import Path
from docker.errors import BuildError, ImageNotFound, APIError


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

RUN bash -c "t4p checkout -p {subject["project_name"]} -i {subject["bug_ids"][0]}"
RUN bash -c "t4p build"

RUN bash -c "pip install git+https://github.com/martineberlein/debugging-benchmark@dev"

COPY ./docker_setup.py /tmp/app

RUN bash -c "python3 docker_setup.py {subject["project_name"]} {subject["bug_ids"][0]}"

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
