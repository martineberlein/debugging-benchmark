from typing import List, Type
import logging

from debugging_framework.results import initialize_dataframe
from debugging_framework.tools import Tool
from debugging_framework.subjects import TestSubject


VLOGGER = logging.getLogger("evaluation")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s :: %(levelname)-8s :: %(message)s",
)

OUT_FILE = "evo_results.pkl"


class Evaluation:
    def __init__(self, tools, subjects, repetitions, timeout):
        self.tools: List[Type[Tool]] = tools
        self.subjects: List[TestSubject] = subjects
        self.repetitions: int = repetitions
        self.timeout: int = timeout

    def run(self):
        subject_names = [(sub.name, sub.id) for sub in self.subjects]
        tool_names = [tool.name for tool in self.tools]
        df_results = initialize_dataframe(subject_names, tool_names, self.repetitions)

        for subject in self.subjects:
            VLOGGER.info(
                f"Evaluating Subject {subject.__class__.__name__}_{subject.id}"
            )

            param = subject.to_dict()
            for tool in self.tools:
                for i in range(1, self.repetitions + 1):
                    report = tool(**param).run()
                    df_results.at[
                        (i, tool.name), (subject.name, subject.id)
                    ] = report.to_dict()

        VLOGGER.info(f"Saving results to {OUT_FILE}")
        df_results.to_pickle(OUT_FILE)
