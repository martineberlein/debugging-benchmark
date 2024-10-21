import docker
import os
from pathlib import Path
import concurrent.futures
from docker.errors import BuildError, ImageNotFound, APIError
from docker.models.images import Image
from docker.models.containers import Container
import tempfile
import shutil
from typing import List
from tests4py.projects import Project

from debugging_framework.docker import get_base_dockerfile, get_docker_runner_files
from debugging_framework.input.oracle import OracleResult

import threading
import queue
import tarfile
import io

BASE_IMAGE_TAG = 'base_image'

def copy_files_to_temp(src_files, temp_dir):
    for file in src_files:
        shutil.copy(file, temp_dir)

class DockerManagerNew:

    def __init__(self, project: Project):
        self.base_image = None
        self.image = None
        self.docker_socket = self._configure_docker_socket()
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
        # Build base image
        base_dockerfile = get_base_dockerfile()
        base_dockerfile_name = str(base_dockerfile.name)
        base_dockerfile_path = str(base_dockerfile.parent)

        base_image = self.build_image(
            path_to_docker_dir=base_dockerfile_path,
            image_tag=BASE_IMAGE_TAG,
            dockerfile=base_dockerfile_name
        )
        self.base_image = base_image

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            print("Temporary directory created at:", temp_dir)

            # Build subject image
            subject_image_tag = f'{self.project.get_identifier()}_image'
            subject_dockerfile_name = f'Dockerfile.{self.project.get_identifier()}'

            dockerfile_file_location = temp_dir + "/" + subject_dockerfile_name
            self._create_subject_dockerfile(dockerfile_file_location)

            # Copy files to the temporary directory
            copy_files_to_temp(get_docker_runner_files(), temp_dir)
            print(f"Files {get_docker_runner_files()} copied to temporary directory.")

            # Perform build operations
            self.image = self.build_image(
                path_to_docker_dir=temp_dir,
                image_tag=subject_image_tag,
                dockerfile=subject_dockerfile_name
            )

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

    def _run_input_in_container(self, container, input_str) -> str:
        try:
            # Create a tar archive in memory containing the input file
            tarstream = io.BytesIO()
            with tarfile.open(fileobj=tarstream, mode='w') as tar:
                tarinfo = tarfile.TarInfo(name="input.txt")
                input_bytes = input_str.encode('utf-8')
                tarinfo.size = len(input_bytes)
                tar.addfile(tarinfo, io.BytesIO(input_bytes))
            tarstream.seek(0)

            # Copy the input file into the container at /app/input.txt
            container.put_archive(path="/app", data=tarstream)

            # Now run the project, assuming it reads from 'input.txt'
            command = ["python3", "docker_runner_inputs.py", "input.txt"]
            exec_result = container.exec_run(cmd=command, workdir="/app", tty=False, demux=True)
            stdout, stderr = exec_result.output
            output = stdout.decode('utf-8')
            # print(stderr.decode('utf-8'))
            return output
        except Exception as e:
            print(f"Error executing command in container: {e}")
            self.cleanup()
            raise

    def run_inputs(self, inputs: List[str]) -> List[str]:
        outputs = dict()
        outputs_lock = threading.Lock()
        input_queue = queue.Queue()
        for input_str in inputs:
            input_queue.put(input_str)

        def process_input(container):
            while not input_queue.empty():
                try:
                    input_str = input_queue.get_nowait()
                except queue.Empty:
                    break
                output = self._run_input_in_container(container, input_str)
                oracle_result = self._parse_output_to_oracle_result(output)
                with outputs_lock:
                    outputs[hash(input_str)] = oracle_result
                    # outputs.append((hash(input_str) ,oracle_result))
                input_queue.task_done()

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.container)) as executor:
            futures = [executor.submit(process_input, container) for container in self.container]
            # Wait for all tasks to be done
            input_queue.join()
        return outputs

    def _parse_output_to_oracle_result(self, output_str: str) -> OracleResult:
        output_str = output_str.strip()
        try:
            oracle_result = OracleResult(output_str)
        except ValueError:
            oracle_result = OracleResult.UNDEFINED
        return oracle_result

    def _create_subject_dockerfile(self, file_location: str):
        dockerfile = f'''FROM {BASE_IMAGE_TAG}

# Install python using pyenv
RUN bash -c "source ~/.bashrc && pyenv install {self.project.python_version}"

COPY ./docker_setup.py /app
COPY ./docker_runner.py /app
COPY ./docker_runner_inputs.py /app

RUN bash -c "python3 docker_setup.py {self.project.project_name} {self.project.bug_id}"

# Set the working directory
WORKDIR /app

# Set the command to keep the container running
CMD ["tail", "-f", "/dev/null"]
'''
        with open(file_location, 'w') as file:
            file.write(dockerfile)