import json

f = open('out.txt', 'r')
arr = f.read()
li = json.loads(arr)
print(li, type(li))