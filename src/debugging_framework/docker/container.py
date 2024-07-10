import docker
import os


class DockerManager:
    def __init__(self, image_tag="my_python_app", container_name="my_python_app_container"):
        self.client = docker.from_env()
        self.image_tag = image_tag
        self.container_name = container_name
        self.container = None
        self.image = None
        self.dockerfile_path = None


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

    def _image_exists(self):
        try:
            self.image = self.client.images.get(self.image_tag)
            return True
        except docker.errors.ImageNotFound:
            return False

    def build(self):
        if self._image_exists():
            print(f"Image {self.image_tag} already exists. Skipping build.")
            return
        self._write_files()
        try:
            self.image, build_logs = self.client.images.build(path=".", tag=self.image_tag, rm=True)
            print(self.image)
            for chunk in build_logs:
                if 'stream' in chunk:
                    print(chunk['stream'].strip())
        except docker.errors.BuildError as e:
            print(f"Build failed: {e}")
            self.cleanup()
            raise

    def run(self, message="Hello from inside the container!"):
        if not self._image_exists():
            raise RuntimeError("Image has not been built. Call build() first.")
        try:
            cmd = ["python3", "/app/script.py", message]
            # command = f'python /app/script.py "{message}"'
            self.container = self.client.containers.run(
                self.image.id,
                name=self.container_name,
                detach=True,
                # tty=True,
                stdin_open=True,
                command=cmd,
            )
            logs = self.container.logs(stream=True)
            for log in logs:
                print(log.strip().decode('utf-8'))
        except Exception as e:
            print(f"Error running container: {e}")
            self.cleanup()
            raise

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

    def create_container(self):
        if not self._image_exists():
            raise RuntimeError("Image has not been built. Call build() first.")
        try:
            self.container = self.client.containers.create(
                self.image.id,
                name=self.container_name,
                detach=True,
                tty=True,
                stdin_open=True,
            )
            self.container.start()
        except docker.errors.APIError as e:
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


if __name__ == "__main__":
    manager = DockerManager()
    try:
        manager.build()
        manager.create_container()

        for i in range(100):
            manager.exec_command(message=f"{i}: Hello from the host!")
    finally:
        manager.cleanup()
