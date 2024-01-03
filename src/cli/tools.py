import argparse
from typing import List


from debugging_framework.tools import (GrammarBasedEvaluationTool,
                                    GrammarBasedEvaluationFuzzer,
                                    InputsFromHellEvaluationFuzzer,
                                    ISLaGrammarEvaluationFuzzer,
                                    Tool)

def main() -> List[Tool]:
	parser = argparse.ArgumentParser(prog = "tools",
                                  	description= "Creates BenchmarkPrograms from a BenchmarkRepository"
									             "and returns them in a List",
                                    formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument("-t", "--tool",
                     	help= "choose a specific tool\n"
                              "default is all\n"
                              "1 = GrammarBased\n"
                              "2 = GrammarBasedFuzzer\n"
                              "3 = InputsFromHellFuzzer\n"
                              "4 = ISLAGrammarFuzzer",
                        default=0,
                        type=int)

      
	args = parser.parse_args()
      
	match args.tool:
          case 1:
            return [GrammarBasedEvaluationTool]
          case 2:
            return [GrammarBasedEvaluationFuzzer]
          case 3:
            return [InputsFromHellEvaluationFuzzer]
          case 4:
            return [ISLaGrammarEvaluationFuzzer]
          case 0:
            return [GrammarBasedEvaluationTool,
                    GrammarBasedEvaluationFuzzer,
                    InputsFromHellEvaluationFuzzer,
                    ISLaGrammarEvaluationFuzzer]

if __name__ == "__main__":
    exit(main())