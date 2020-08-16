# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import numpy as np
from ReadData import ReadFile
from OrderBook import OrderBook


def quicksort(nums):
    if len(nums) <= 1:
        return nums
    else:
        q = random.choice(nums)
    l_nums = [n for n in nums if n['id'] < q['id']]

    e_nums = [q] * nums.count(q)
    b_nums = [n for n in nums if n['id'] > q['id']]
    return quicksort(l_nums) + e_nums + quicksort(b_nums)


def main_f():
    file_name = input()
    data = ReadFile.input(file_name)
    OrderBook(data)
    a = []
    for i in range(100):
        a.append({'timestamp': 1000, 'id': int(random.random()*1000), 'type': 'E'})

    b = quicksort(a)
    print(a)
    print(b)


if __name__ == '__main__':
    main_f()



