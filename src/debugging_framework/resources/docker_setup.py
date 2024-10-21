import sys

from tests4py.api import get_projects

from debugging_benchmark.tests4py_benchmark.repository import Tests4PyBenchmarkRepository
from debugging_benchmark.tests4py_benchmark import project as project_module

if __name__ == "__main__":
    project_name = sys.argv[1]
    bug_id = int(sys.argv[2])

    project = get_projects(project_name, bug_id)

    class_name = project_name.capitalize() + str(bug_id) + 'Tests4PyProject'
    module = project_module

    # Get the class from the module
    cls = getattr(module, class_name)

    # Now you can instantiate the class or use it as needed
    instance = cls()

    subjects = Tests4PyBenchmarkRepository(
        projects=[instance],
    ).build()

    benchmark_program = next(iter(subjects))
    print(benchmark_program)
    benchmark_program.dump("./benchmark_program.pickle")
