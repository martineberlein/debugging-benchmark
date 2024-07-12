import importlib.resources as pkg_resources


def get_base_dockerfile():
    return pkg_resources.path('debugging_framework.resources', 'Dockerfile.base')


def get_docker_runner_files():
    return [
        pkg_resources.path('debugging_framework.resources', 'docker_setup.py'),
        pkg_resources.path('debugging_framework.resources', 'docker_runner.py')
    ]

