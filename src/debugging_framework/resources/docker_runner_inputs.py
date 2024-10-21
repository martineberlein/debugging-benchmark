#!/usr/bin/env python3

import sys
import os

from debugging_framework.benchmark.program import BenchmarkProgram
from tests4py.api.logging import deactivate, debug
import logging

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 docker_runner_inputs.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]

    # Construct the full path to the input file
    input_path = os.path.join('/app', input_file)
    if not os.path.exists(input_path):
        print(f"Input file {input_file} does not exist in /app.")
        sys.exit(1)

    # Read the input data from the file
    with open(input_path, 'r') as f:
        input_data = f.read()

    # Process the input data using your project code
    # Replace 'process_input' with your actual processing function
    output_data = process_input(input_data)

    # Output the result
    print(str(output_data[0]))

def process_input(inp_string: str):
    """
    Replace this function's content with the actual code that processes the input data.
    This could involve importing your project's modules and calling the appropriate functions.
    """
    benchmark_program: BenchmarkProgram = BenchmarkProgram.load("./benchmark_program.pickle")

    oracle = benchmark_program.get_oracle()
    oracle_result = oracle(inp_string)
    logging.info(f"Input: {inp_string}, Oracle: {oracle_result}")

    return oracle_result

if __name__ == '__main__':
    # Tests4Py logging
    deactivate()

    main()