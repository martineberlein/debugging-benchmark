from debugging_benchmark.calculator.calculator import CalculatorBenchmarkRepository
from debugging_benchmark.database import DatabaseHelper
from debugging_framework.tools import GrammarBasedEvaluationFuzzer
from debugging_framework.oracle import OracleResult

def main():
    calc = CalculatorBenchmarkRepository().build()
    param = calc.to_dict()
    fuzzer = GrammarBasedEvaluationFuzzer(**param)
    fuzzer.run()
    gen_inps = fuzzer.get_generated_inputs()
    oracle = calc.get_oracle()
    db = DatabaseHelper.instance()
    prog_id = db.insert_program(calc)
    """ for inp in gen_inps:
        if db.get_count_inputs(prog_id)[0] >= 5 and db.get_count_inputs(prog_id)[1] >= 5:
            break
        db.insert_input(prog_id, inp, oracle) """
    db.delete_program(calc)
    prog_id = db.insert_program(calc)
    db.insert_many_inputs(prog_id, gen_inps,oracle)
    



if __name__ == "__main__":
    main()