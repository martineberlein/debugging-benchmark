import argparse
from typing import List


from debugging_framework.tools import (GrammarBasedEvaluationTool,
                                    GrammarBasedEvaluationFuzzer,
                                    InputsFromHellEvaluationFuzzer,
                                    ISLaGrammarEvaluationFuzzer,
                                    Tool)

def main() -> List[Tool]:
    parser = argparse.ArgumentParser(prog = "tool",
                                    description= "With this Command you can choose a tool for Evaluation",
                                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-t", "--tool",
                     	help= "choose a specific tool\n"
                              "default is all\n"
                              "1 = GrammarBasedFuzzer\n"
                              "2 = InputsFromHellFuzzer\n"
                              "3 = ISLAGrammarFuzzer",
                        default=0,
                        type=int)

    args = parser.parse_args()

    match args.tool:
          case 1:
            return [GrammarBasedEvaluationFuzzer]
          case 2:
            return [InputsFromHellEvaluationFuzzer]
          case 3:
            return [ISLaGrammarEvaluationFuzzer]
          case 0:
            return [GrammarBasedEvaluationTool,
                    GrammarBasedEvaluationFuzzer,
                    InputsFromHellEvaluationFuzzer,
                    ISLaGrammarEvaluationFuzzer]

if __name__ == "__main__":
    exit(main())