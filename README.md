[![Test](https://github.com/martineberlein/debugging-benchmark/actions/workflows/tests.yml/badge.svg)](https://github.com/martineberlein/debugging-benchmark/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/martineberlein/debugging-benchmark/badge.svg?branch=main)](https://coveralls.io/github/martineberlein/debugging-benchmark?branch=main)

# Debugging Benchmark

Welcome to the **Debugging Benchmark**!

This guide will walk you through using our benchmarks to test and evaluate your research prototypes efficiently.

## Quickstart 

### Initializing the Calculator Benchmark

Let's start by constructing the Calculator Subject from our benchmark collection. We initialize the Calculator Benchmark Repository, which contains the Subject and automatically builds it for us.
_Note that repositories can contain multiple subjects, i.e., when they have more than one version or bug._


```python
from typing import List
from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.benchmark.repository import BenchmarkRepository
from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository

# Initialize the repository containing the calculator benchmarks
calculator_repo: BenchmarkRepository = CalculatorBenchmarkRepository()

# Build the subjects from the repository
calculator_subjects: List[BenchmarkProgram] = calculator_repo.build()

print(f"Initialized Calculator Repository with {len(calculator_subjects)} subject(s).")
```

    Output: Initialized Calculator Repository with 1 subject(s).


#### Accessing a Subject

We access the first subject from the list of built calculator subjects to work with it. This subject represents a specific version or instance of the calculator program that we will test and evaluate.


```python
calculator = next(iter(calculator_subjects))
calculator
```

    Output: BenchmarkProgram(calculator)

### Fuzzing the Calculator Benchmark

Next, we'll fuzz each calculator subject to generate passing and failing inputs.
The `GrammarFuzzer` is utilized here to create inputs based on the grammar and rules defined in the calculator subject.

```python
from debugging_framework.fuzzingbook.fuzzer import GrammarFuzzer

# Retrieve the grammar defined for the calculator
grammar = calculator.get_grammar()

# Retrieve the oracle for the calculator, which determines if the output is correct
program_oracle = calculator.get_oracle()

# Create a fuzzer instance with the retrieved grammar
fuzzer = GrammarFuzzer(grammar=grammar)

# Generate and print 10 fuzzed inputs along with their oracle results
for _ in range(10):
    inp = fuzzer.fuzz()
    print(inp.ljust(30), program_oracle(inp))
``` 

    Output:

    cos(6)                         (<OracleResult.PASSING: 'PASSING'>, None)
    sqrt(453.3)                    (<OracleResult.PASSING: 'PASSING'>, None)
    sqrt(-507)                     (<OracleResult.FAILING: 'FAILING'>, ValueError())
    cos(-7)                        (<OracleResult.PASSING: 'PASSING'>, None)
    cos(23810174.37)               (<OracleResult.PASSING: 'PASSING'>, None)
    sin(-7)                        (<OracleResult.PASSING: 'PASSING'>, None)
    tan(46.79)                     (<OracleResult.PASSING: 'PASSING'>, None)
    tan(-8780.3)                   (<OracleResult.PASSING: 'PASSING'>, None)
    sqrt(2681)                     (<OracleResult.PASSING: 'PASSING'>, None)
    sin(23)                        (<OracleResult.PASSING: 'PASSING'>, None)

### Displaying the Grammar

We can display the grammar used by the calculator benchmark. The grammar defines the structure of valid inputs for the calculator, which the fuzzer uses to generate test cases.


```python
from pprint import pprint

# Retrieve and print the grammar for the calculator
grammar = calculator.get_grammar()
pprint(grammar)
```
    Output:

    {'<arith_expr>': ['<function>(<number>)'],
     '<digit>': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
     '<digits>': ['<digit>', '<digit><digits>'],
     '<function>': ['sqrt', 'sin', 'cos', 'tan'],
     '<maybe_digits>': ['', '<digits>'],
     '<maybe_frac>': ['', '.<digits>'],
     '<maybe_minus>': ['', '-'],
     '<number>': ['<maybe_minus><one_nine><maybe_digits><maybe_frac>'],
     '<one_nine>': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
     '<start>': ['<arith_expr>']}


### Program Oracle Explanation

**Program Oracle**: All subjects in the Debugging Benchmark come with a program oracle, which indicates whether a bug in the program occurred.
This can be an unexpected Exception or Result.
The oracle returns an `OracleResult`, which can be either `PASSING`, `FAILING`, or `UNDEFINED`.

We initialize the program oracle, a function that takes an input string and returns a tuple containing the `OracleResult` and any `Exception` encountered.


```python
from typing import Callable, Tuple, Union
from debugging_framework.input.oracle import OracleResult

# Initialize the program oracle for the calculator
program_oracle: Callable[[str], Tuple[OracleResult, Union[Exception, None]]] = calculator.get_oracle()
```

**Testing the Program Oracle with Valid Input**: We test the program oracle with a valid input to see how it evaluates the result. Here, we use a trigonometric function `cos(10)`.

```python
# Test the program oracle with a valid input
program_oracle("cos(10)")
```

    Output: (<OracleResult.PASSING: 'PASSING'>, None)

**Testing the Program Oracle with failing Inputs**:
We test the program oracle with a failure inducing input to observe its behavior when encountering errors.
Here, we use the square root of a negative number `sqrt(-900)`, which should trigger an exception.

```python
# Test the program oracle with a failing input
program_oracle("sqrt(-900)")
```

    Output: (<OracleResult.FAILING: 'FAILING'>, ValueError())

### Initial Inputs

**Initial Inputs:** Each Subject comes with a set of initial inputs (_passing_ and _failing_).
These inputs help us understand the basic behavior of the program before further testing.

We print each initial input along with its oracle result.

```python
# Print each initial input and its oracle result
for inp in calculator.get_initial_inputs():
    print(inp.ljust(30), program_oracle(inp))
```

    cos(10)                        (<OracleResult.PASSING: 'PASSING'>, None)
    sqrt(-900)                     (<OracleResult.FAILING: 'FAILING'>, ValueError())


The initial inputs can also be accessed using the functions `get_passing_inputs()` and `get_failing_inputs()`, which return only passing or failing inputs, respectively.

### Dictionary Representation of Parameters

**Dictionary**: For convenience, each subject also implements the function `to_dict()` which returns a dictionary of all parameters, making them easily accessible.

We retrieve the dictionary representation of the parameters with only passing inputs.

```python
# Retrieve the dictionary representation of parameters with only passing inputs
calculator_param = calculator.to_dict(only_passing=True)
```

We display the dictionary representation of the calculator parameters to examine the details.

```python
from pprint import pprint

# Print the dictionary of parameters
pprint(calculator_param)
```
    
    Output:

    {'grammar': {'<arith_expr>': ['<function>(<number>)'],
                 '<digit>': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                 '<digits>': ['<digit>', '<digit><digits>'],
                 '<function>': ['sqrt', 'sin', 'cos', 'tan'],
                 '<maybe_digits>': ['', '<digits>'],
                 '<maybe_frac>': ['', '.<digits>'],
                 '<maybe_minus>': ['', '-'],
                 '<number>': ['<maybe_minus><one_nine><maybe_digits><maybe_frac>'],
                 '<one_nine>': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                 '<start>': ['<arith_expr>']},
     'initial_inputs': ['cos(10)'],
     'oracle': <function calculator_oracle at 0x111e679c0>}



```python
# Parameters can be accessed directly
calculator_param["initial_inputs"]
```

    Output: ['cos(10)']

## Install, Development, Testing

For development and testing, we recommend installing _debugging benchmark_ inside a virtual environment (virtualenv).
By doing the following steps in a standard shell (bash), one can run the tests:

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