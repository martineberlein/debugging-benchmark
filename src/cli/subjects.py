import argparse
from typing import List

from debugging_benchmark.student_assignments import (
    NPrStudentAssignmentBenchmarkRepository,
    SquareRootAssignmentBenchmarkRepository,
    GCDStudentAssignmentBenchmarkRepository,
    SieveOfEratosthenesStudentAssignmentBenchmarkRepository,
    MiddleAssignmentBenchmarkRepository,
    FibonacciStudentAssignmentBenchmarkRepository,
    BubbleSortAssignmentBenchmarkRepository,
    PalindromeAssignmentBenchmarkRepository,
    RemoveVowelAssignmentBenchmarkRepository,
    MergeStringsAssignmentBenchmarkRepository,
    StudentAssignmentBenchmarkProgram
)

def main() -> List[StudentAssignmentBenchmarkProgram]:
	parser = argparse.ArgumentParser(prog = "subject",
                                  	description= "Creates BenchmarkPrograms from a BenchmarkRepository"
									             "and returns them in a List",
                                    formatter_class=argparse.RawTextHelpFormatter)

	
	parser.add_argument("-t", "--type",
                     	help= "choose a specific subject\n"
							  "default is all\n"
                              "1 = NPr\n"
                              "2 = sqrt\n"
                              "3 = GCD\n"
                              "4 = SieveOfEratosthenes\n"
                              "5 = middle\n"
                              "6 = fibonacci\n"
                              "7 = bubble sort\n"
                              "8 = palindorome\n"
                              "9 = remove vowel\n"                              
                              "10 = merge strings",
                        default=0,
                        type=int)
    
	args = parser.parse_args()
	
	match args.type:
		case 1:
			return NPrStudentAssignmentBenchmarkRepository().build()
		case 2:
			return SquareRootAssignmentBenchmarkRepository().build()
		case 3:
			return GCDStudentAssignmentBenchmarkRepository().build()
		case 4:
			return SieveOfEratosthenesStudentAssignmentBenchmarkRepository().build()
		case 5:
			return MiddleAssignmentBenchmarkRepository().build()
		case 6:
			return FibonacciStudentAssignmentBenchmarkRepository().build()
		case 7: 
			return BubbleSortAssignmentBenchmarkRepository().build()
		case 8:
			return PalindromeAssignmentBenchmarkRepository().build()
		case 9:
			return RemoveVowelAssignmentBenchmarkRepository().build()
		case 10:
			return MergeStringsAssignmentBenchmarkRepository().build()
		case 0:
			return [
				NPrStudentAssignmentBenchmarkRepository().build(),
				SquareRootAssignmentBenchmarkRepository().build(),
				GCDStudentAssignmentBenchmarkRepository().build(),
				SieveOfEratosthenesStudentAssignmentBenchmarkRepository().build(),
				MiddleAssignmentBenchmarkRepository().build(),
				FibonacciStudentAssignmentBenchmarkRepository().build(),
				BubbleSortAssignmentBenchmarkRepository().build(),
				PalindromeAssignmentBenchmarkRepository().build(),
				RemoveVowelAssignmentBenchmarkRepository().build(),
				MergeStringsAssignmentBenchmarkRepository().build()
            ]
	
	


if __name__ == "__main__":
    exit(main())