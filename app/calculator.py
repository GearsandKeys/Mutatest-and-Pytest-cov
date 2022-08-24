from functools import reduce
# import numpy as np
import math
from operator import mul

class Calculator():
    def multiply(nums):
        total = 1
        for num in nums:
            total = total*num
        return total

    def multiply_prod(self, *nums):
        total = math.prod(nums)
        return total

    # def multiply_numpy(self, *nums):
    #     total = np.prod(nums)
    #     return total

    def multiply_reduce(self, *nums):
        total = reduce((lambda x, y: x * y), nums)
        return total
    
    def multiply_mul(self, *nums):
        total = 1
        for num in nums:
            total = mul(num, total)
        return total