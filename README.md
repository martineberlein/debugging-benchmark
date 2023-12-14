[![Test](https://github.com/martineberlein/debugging-benchmark/actions/workflows/tests.yml/badge.svg)](https://github.com/martineberlein/debugging-benchmark/actions/workflows/tests.yml)
[![Coverage](https://github.com/martineberlein/debugging-benchmark/actions/workflows/coverage.yml/badge.svg)](https://github.com/martineberlein/debugging-benchmark/actions/workflows/coverage.yml)
[![Coverage Status](https://coveralls.io/repos/github/martineberlein/debugging-benchmark/badge.svg?branch=actions)](https://coveralls.io/github/martineberlein/debugging-benchmark?branch=actions)

# debugging-benchmark

## Quickstart 

Generating Passing and Failing Inputs:

```python 
from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_framework.tools import GrammarBasedEvaluationFuzzer

calc = CalculatorBenchmarkRepository().build()
param = calc.to_dict()
fuzzer = GrammarBasedEvaluationFuzzer(**param)
fuzzer.run()
gen_inps = fuzzer.get_generated_inputs()
``` 

Evaluation:

```python 
from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_framework.evaluator import Evaluation
from debugging_framework.tools import InputsFromHellEvaluationFuzzer

tools = [InputsFromHellEvaluationFuzzer]

subjects = SieveOfEratosthenesStudentAssignmentBenchmarkRepository().build()

result = Evaluation(
        tools=tools, 
        subjects=subjects[0:1],
        repetitions=1, 
        timeout=3600
        ).run()
``` 


## Deeper Look into the Class Structure

Check out the Class Diagram for a first overview. Further down in this section we take a look at some key functions of interest.

#### Class Diagram
![StudenAssignmentClassDiagram](https://github.com/martineberlein/debugging-benchmark/assets/82182021/2e5fb169-02b1-444d-9c2e-ba6793f97535)


`BenchmarkRepository` and `BenchmarkProgram` can be found in `debugging_framework/benchmark.py`

`StudentAssignmentBenchmarkProgram`,`StudentAssignmentRepository` and `GCDStudentAssignmentBenchmarkRepository` can be found in `debugging_benchmark/student_assignments.py`

The faulty programs can be found at `debugging_benchmark/student_assignments/problem_1_GCD` and the correct implementation at `debugging_benchmark/student_assignments/reference1.py`

#### build()

Returns a List of BenchmarkPrograms. Calls internally _construct_test_program(). This function is our interface.

#### _construct_test_program()

Returns a BenchmarkProgram. Calls internally construct_oracle() to construct a oracle for our program.

#### construct_oracle()

Where the magic happens.
Returns a Functions which loads the faulty and correct implementation, executes both with the input and checks if they are the same or not. If they are the same return OracleResult.PASSING, if not return OracleResult.FAILING 

#### to_dict()

PLACEHOLDER

## Install, Development, Testing
### Install

If all external dependencies are available, a simple pip install PLACEHOLDER suffices.
We recommend installing PLACEHOLDER inside a virtual environment (virtualenv):

```
python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install PLACEHOLDER
```

### Development and Testing

For development and testing, we recommend using PLACEHOLDER inside a virtual environment (virtualenv).
By doing the following steps in a standard shell (bash), one can run the PLACEHOLDER tests:

```
git clone https://github.com/martineberlein/debugging-benchmark
cd debugging-benchmark

python3.10 -m venv venv
source venv/bin/activate

pip install --upgrade pip

# Run tests
pip install -e .[dev]
python3 -m pytest
```