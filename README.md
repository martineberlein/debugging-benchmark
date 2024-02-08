[![Test](https://github.com/martineberlein/debugging-benchmark/actions/workflows/tests.yml/badge.svg)](https://github.com/martineberlein/debugging-benchmark/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/martineberlein/debugging-benchmark/badge.svg?branch=main)](https://coveralls.io/github/martineberlein/debugging-benchmark?branch=main)

# debugging-benchmark

Welcome to the debugging benchmark toolkit!
This guide will walk you through using our benchmarks to test and evaluate your research prototypes efficiently.

## Quickstart 

### Initializing the Calculator Benchmark

Let's start by initializing the CalculatorBenchmarkRepository from our benchmark collection.
This repository contains different subjects for the calculator benchmark, each designed to test various aspects of calculator implementations.
```python 
from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository

calculator_repo = CalculatorBenchmarkRepository()
calculator_subjects = calculator_repo.build()

print(f"Initialized Calculator Benchmark with {len(calculator_subjects)} subjects.")
``` 

### Fuzzing the Calculator Benchmark

Next, we'll fuzz each calculator subject to generate passing and failing inputs.
The GrammarBasedEvaluationFuzzer is utilized here to create inputs based on the grammar and rules defined in the calculator benchmark.

```python
from debugging_framework.tools import GrammarBasedEvaluationFuzzer

print(f"Fuzzing the calculator repository...")

for calculator_subject in calculator_subjects:
    print(f"Fuzzing the calculator subject ({calculator_subject})...")
    param = calculator_subject.to_dict()
    
    fuzzer = GrammarBasedEvaluationFuzzer(**param)
    failing_inputs = fuzzer.run().get_all_failing_inputs()

    if failing_inputs:
        print(f"Found the following failing inputs:")
        for failing_input in failing_inputs:
            print(failing_input)
    else:
        print("No failing inputs found.")
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