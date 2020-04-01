from client_moodle import *

input_file = open('best.txt', 'r')
arr = input_file.read()
arr = json.loads(arr)

err = get_errors('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', arr)
print(err)