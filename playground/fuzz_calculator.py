from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_benchmark.database import DatabaseHelper
from debugging_framework.tools import GrammarBasedEvaluationFuzzer

def main():
    calc = CalculatorBenchmarkRepository().build()
    param = calc.to_dict()
    fuzzer = GrammarBasedEvaluationFuzzer(**param)
    fuzzer.run()
    gen_inps = fuzzer.get_generated_inputs()
    oracle = calc.get_oracle()
    db = DatabaseHelper.instance()
    prog_id = db.insert_program(calc)
    db.insert_many_inputs(prog_id, gen_inps,oracle)
    



if __name__ == "__main__":
    main()