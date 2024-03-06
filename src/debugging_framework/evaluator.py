from typing import List, Type, Optional, Union, Dict
import logging
import pandas as pd
from pathlib import Path

from debugging_framework.results import initialize_dataframe
from debugging_framework.tools import Tool
from debugging_framework.benchmark import BenchmarkProgram
from debugging_framework.report import Report, MultipleFailureReport


VLOGGER = logging.getLogger("evaluation")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s :: %(levelname)-8s :: %(message)s",
)

OUT_FILE = "results.pkl"


class Evaluation:
    def __init__(
        self,
        tools,
        subjects,
        repetitions,
        timeout,
        out_file: Optional[Union[str, Path]] = None,
        tool_param=None,
    ):
        self.tools: List[Type[Tool]] = tools
        self.subjects: List[BenchmarkProgram] = subjects
        self.repetitions: int = repetitions
        self.timeout: int = timeout
        self.out_file = self.resolve_path(out_file) if out_file else out_file
        self.tool_param = tool_param if tool_param else {}

    @staticmethod
    def resolve_path(out_file: Union[str, Path]) -> Path:
        if isinstance(out_file, Path):
            return out_file

        return Path(out_file).resolve()

    def initialize_result_dataframe(self) -> pd.DataFrame:
        subject_names = [(sub.name, sub.bug_id) for sub in self.subjects]
        tool_names = [tool.name for tool in self.tools]
        return initialize_dataframe(subject_names, tool_names, self.repetitions)

    @staticmethod
    def run_tool(tool, param) -> Report:
        try:
            report = tool(**param).run()
        except Exception as e:
            VLOGGER.info(f"Tool {tool.name} did not finish: {e}")
            report = MultipleFailureReport(name=tool.name)
        return report

    def run(self) -> pd.DataFrame:
        df_results = self.initialize_result_dataframe()

        for subject in self.subjects:
            VLOGGER.info(f"Evaluating Subject {subject.name}_{subject.bug_id}")
            param = {**subject.to_dict(), **self.tool_param}
            #param = subject.to_dict()

            for tool in self.tools:
                report = self.run_tool(tool, param)

                for i in range(1, self.repetitions + 1):
                    report = self.run_tool(tool, param)
                    df_results.at[
                        (i, tool.name), (subject.name, subject.bug_id)
                    ] = report.to_dict()

        if self.out_file:
            VLOGGER.info(f"Saving results to {self.out_file}")
            df_results.to_pickle(self.out_file)

        return df_results

    # könnten das df aus run() als membervar speichern
    def export_to_latex(
        self, df: pd.DataFrame, out_file: Optional[Union[str, Path]] = None
    ):
        if out_file:
            df.to_latex(out_file)
        else:
            return df.to_latex()
