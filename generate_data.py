import datetime
import random


def quicksort(nums):
    if len(nums) <= 1:
        return nums
    else:
        q = random.choice(nums)
    l_nums = [n for n in nums if n['timestamp'] < q['timestamp']]

    e_nums = [q] * nums.count(q)
    b_nums = [n for n in nums if n['timestamp'] > q['timestamp']]
    return quicksort(l_nums) + e_nums + quicksort(b_nums)


name = 'data' + str(datetime.datetime.now())

data = []
for i in range(10000):
    ts = int(random.random() * 100000)
    data.append({'timestamp': ts, 'ID': i+1, 'type': 'I', 'prise': str(random.random() * 1000)})
    data.append({'timestamp': ts + int(random.random() * 10000), 'ID': i+1, 'type': 'E', 'prise': ''})

data = quicksort(data)
f = open(name, 'w')
for i in data:
    f.write(str(i['timestamp']) + ' ' + i['type'] + ' ' + str(i['ID']) + ' ' + i['prise']+'\n')
print("Done")
print(name)
f.close()
