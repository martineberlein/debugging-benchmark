from typing import List, Optional, Union, Any
import logging
from pathlib import Path

import pandas as pd

from debugging_framework.evaluation.results import initialize_dataframe
from debugging_framework.evaluation.tools import Tool
from debugging_framework.benchmark.program import BenchmarkProgram
from debugging_framework.execution.report import Report, MultipleFailureReport


VLOGGER = logging.getLogger("evaluation")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s :: %(levelname)-8s :: %(message)s",
)

OUT_FILE = "results.pkl"


class Evaluation:
    """
    Evaluates Subjects on a single Tool. Returns a pd.dataframe with the collected information.
    """
    def __init__(
        self,
        tool,
        subjects,
        repetitions,
        #timeout,
        out_file: Optional[Union[str, Path]] = None,
        tool_param=None,
    ):
        self.tool: Tool = tool
        self.subjects: List[BenchmarkProgram] = subjects
        self.repetitions: int = repetitions
        #self.timeout: int = timeout
        self.out_file = self.resolve_path(out_file) if out_file else out_file
        self.tool_param = tool_param if tool_param else {}
    
    #TODO: why static?
    @staticmethod
    def resolve_path(out_file: Union[str, Path]) -> Path:
        """
        Turns an relative path into an absolute path
        """
        #So oder so sollten wir resolve callen -> check hier unnötig??
        #vorher war hier return out_file in Zeile 51
        if isinstance(out_file, Path):
            return out_file.resolve()

        return Path(out_file).resolve()

    def initialize_result_dataframe(self) -> pd.DataFrame:
        """
        initializes an empty results dataframe

                                        Result
        Run | Approach | Subject ID
         1      Fuzzer      1           UnexpectedResult
                            2           UnexpecredResult
        
         2      Fuzzer      1           TimeoutResult
                            2           UnexpectedResult
        """

        subject_names = [str(sub) for sub in self.subjects]
        tool_name = self.tool.name
        return initialize_dataframe(subject_names, [tool_name], self.repetitions)

    #TODO: why static?? das nervt mich so das mein intelli run() hier nicht erkennt, gleiche bei repos und build        
    @staticmethod
    def run_tool(tool: Tool, param: Any) -> Report:
        """
        Runs the tool with the parameters and catches thrown exceptions.
        Tool could be EvoGFuzz or EvoGGen for example
        """
        try:
            report = tool(**param).run()
        except Exception as e:
            VLOGGER.info(f"Tool {tool.name} did not finish: {e}")
            report = MultipleFailureReport(name=tool.name)
        return report

    def run(self) -> pd.DataFrame:
        """
        Runs the tool for all the subjects.
        Saves the Results in a DataFrame.
        """
        df_results = self.initialize_result_dataframe()

        for subject in self.subjects:
            VLOGGER.info(f"Evaluating Subject {str(subject)}")
            param = {**subject.to_dict(), **self.tool_param}

            #repetition = run later in tabular
            for i in range(1, self.repetitions + 1):
                report = self.run_tool(self.tool, param)
                df_results.at[
                    (i, self.tool.name, str(subject)), ("Result")
                ] = report.to_dict()

        if self.out_file:
            VLOGGER.info(f"Saving results to {self.out_file}")
            df_results.to_pickle(self.out_file)

        return df_results


    def export_to_latex(
        self, df: pd.DataFrame, out_file: Optional[Union[str, Path]] = None
    ):
        """
        Exports the DataFrame to Latex
        """
        if out_file:
            df.to_latex(out_file)
        else:
            return df.to_latex()

    def export_to_latex_custom(
            self, df: pd.DataFrame, out_file: Union[str, Path] 
        ):
        """
        Exports the DataFrame to Latex but for a specific look
        """
        with open(out_file, "a") as f:
            f.write("\\begin{tabular}{llllllllllll}\n")
            f.write("\\toprule\n")
            f.write()

