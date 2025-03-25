from debugging_framework.benchmark.repository import BenchmarkProgram, BenchmarkRepository
from debugging_framework.input.oracle import OracleResult

from .heartbeat import oracle, grammar, failing_inputs, passing_inputs


class CalculatorBenchmarkRepository(BenchmarkRepository):
    def build(
        self,
        err_def: dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
    ) -> list[BenchmarkProgram]:
        return [
            BenchmarkProgram(
                name="heartbleed",
                grammar=grammar,
                oracle=oracle,
                failing_inputs=failing_inputs,
                passing_inputs=passing_inputs,
            )
        ]
