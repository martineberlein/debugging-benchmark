#User function Template for python3

class Solution:
    def nPr(self, n, r):
        fact,fact1 = 1,1
        for i in range(1,n+1):
            fact = fact*i
           # print(fact)
        for j in range(1,n-r+1):
            fact1=fact1*j
            #print(fact1)
        return fact//fact1


#{ 
 # Driver Code Starts
#Initial Template for Python 3

if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        n, r = [int(x) for x in input().split()]
        
        ob = Solution()
        print(ob.nPr(n, r))
# } Driver Code Ends