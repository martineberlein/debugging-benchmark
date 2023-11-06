#User function Template for python3


#Complete this function
class Solution:
    def floorSqrt(self, x): 
        low, high = 1, x + 1
        while low < high:
            mid = (low+high) // 2
            if mid*mid == x:
                return mid
            elif mid*mid < x:
                low = mid + 1
            else:
                high = mid
        
        return high - 1


#{ 
 # Driver Code Starts
#Initial Template for Python 3

import math



def main():
        T=int(input())
        while(T>0):
            
            x=int(input())
            
            print(Solution().floorSqrt(x))
            
            T-=1


if __name__ == "__main__":
    main()
# } Driver Code Ends