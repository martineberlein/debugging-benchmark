# User function Template for python3
class Solution:
    def removeVowels(self, S):
        output = ""
        for item in S:
            if item != "a" or item != "e" or item != "i" or item != "o" or item != "u":
                output += item
        return output


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
