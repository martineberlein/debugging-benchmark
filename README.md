[![Test](https://github.com/martineberlein/debugging-benchmark/actions/workflows/tests.yml/badge.svg)](https://github.com/martineberlein/debugging-benchmark/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/martineberlein/debugging-benchmark/badge.svg?branch=main)](https://coveralls.io/github/martineberlein/debugging-benchmark?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/martineberlein/debugging-benchmark/badge.svg?branch=actions)](https://coveralls.io/github/martineberlein/debugging-benchmark?branch=actions)

# debugging-benchmark

## Quickstart 

Generating Passing and Failing Inputs:

```python 
from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_framework.tools import GrammarBasedEvaluationFuzzer

calc = CalculatorBenchmarkRepository().build()

#Param is a Dict with the keys grammar, oracle and initial_inputs
param = calc.to_dict()

fuzzer = GrammarBasedEvaluationFuzzer(**param)
fuzzer.run()
gen_inps = fuzzer.get_generated_inputs()
#sin(18)
#cos(-9.5)
#sqrt(330)
#sqrt(-12)
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
![Repo+Program](https://github.com/martineberlein/debugging-benchmark/assets/82182021/e8fe1725-38c9-493b-8e72-c8cfe961c180)

#### build()

Returns a List of BenchmarkPrograms. Calls internally _construct_test_program(). This function is our interface.

#### to_dict()

Returns a dict with the keys grammar, oracle and initial_inputs. These Parameter can be used for fuzzing new inputs.

## Example use of the abstract Classes

![Example Class Diagram](https://github.com/martineberlein/debugging-benchmark/assets/82182021/2fe7f9aa-020c-44eb-b47a-bdbd2f920570)

The implementation of these classes can be found in `debugging_benchmark/student_assignments.py`

The faulty programs can be found at `debugging_benchmark/student_assignments/problem_1_GCD` and the correct implementation at `debugging_benchmark/student_assignments/reference1.py`

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