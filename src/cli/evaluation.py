import argparse
from typing import List

from debugging_benchmark.student_assignments import BenchmarkProgram
from debugging_framework.evaluator import Evaluation
from debugging_framework.tools import (GrammarBasedEvaluationTool,
                                    GrammarBasedEvaluationFuzzer,
                                    InputsFromHellEvaluationFuzzer,
                                    ISLaGrammarEvaluationFuzzer)

#TODO: Man könnte das erweitern mit allen Tools des Frameworks
#Dann entweder für jede Möglichkeit eine File und ein Keyword
#oder ein Keyword mit unterschiedlichen Optionen
#Aktuell nur Evaluation mit keyword evaluation

def main():
	parser = argparse.ArgumentParser(prog = "evaluation",
                                  	description= "Test test test")
	
	parser.add_argument("subjects",
						help = "use the command subjects to create subjects with the cl",
						type=List[BenchmarkProgram])
    parser.add_argument("-t", "--tool",
                     	help= "choose a specific tool\n"
                              "default is all\n"
                              "1 = GrammarBased\n"
                              "2 = GrammarBasedFuzzer\n"
                              "3 = InputsFromHellFuzzer\n"
                              "4 = ISLAGrammarFuzzer",
                        default=0,
                        type=int)
      
	parser.add_argument("-r", "--repetitions",
                     	help="Repititions of the Evaluation Tool. Default is 1.",
                        default=1,
                    	type=int)
      
	parser.add_argument("-t", "--timeout",
                     	help="Terminate if not finished after 3600 seconds",
                        default=3600,
                    	type=int)
	
	
      
	args = parser.parse_args()
      
	match args.tool:
        case 1:
        	tools = [GrammarBasedEvaluationTool]
        case 2:
            tools = [GrammarBasedEvaluationFuzzer]
        case 3:
            tools = [InputsFromHellEvaluationFuzzer]
        case 4:
            tools = [ISLaGrammarEvaluationFuzzer]
        case 0:
            tools = [GrammarBasedEvaluationTool,
                    GrammarBasedEvaluationFuzzer,
                    InputsFromHellEvaluationFuzzer,
                    ISLaGrammarEvaluationFuzzer]

    
	evaluation = Evaluation(tools, args.subjects, args.repitions, args.timeout)
	




if __name__ == "__main__":
    exit(main())