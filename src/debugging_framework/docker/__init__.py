import importlib.resources as pkg_resources


def get_base_dockerfile():
    with pkg_resources.path('debugging_framework.resources', 'Dockerfile.base') as dockerfile_path:
        return dockerfile_path


def get_docker_runner_files():
    docker_files = []
    with pkg_resources.path('debugging_framework.resources', 'docker_setup.py') as setup_path:
        docker_files.append(setup_path)
    with pkg_resources.path('debugging_framework.resources', 'docker_runner.py') as runner_path:
        docker_files.append(runner_path)
    with pkg_resources.path('debugging_framework.resources', 'docker_runner_inputs.py') as runner_path:
        docker_files.append(runner_path)
    return docker_files

