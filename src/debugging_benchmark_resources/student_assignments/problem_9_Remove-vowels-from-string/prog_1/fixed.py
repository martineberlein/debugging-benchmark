# User function Template for python3
class Solution:
    def removeVowels(self, S):
        # code here
        vol = "AEIOUaeiou"
        news = ""
        for i in S:
            if i in vol:
                continue
            else:
                news += i
        return news


# {
# Driver Code Starts
# Initial Template for Python 3

if __name__ == "__main__":
    T = int(input())
    for i in range(T):
        s = input()

        ob = Solution()
        answer = ob.removeVowels(s)

        print(answer)


# } Driver Code Ends
