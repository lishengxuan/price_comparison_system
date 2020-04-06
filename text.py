
str1 = "k:1|k1:2|k2:3|k3:4"
def str_to_dict(str):
    _dict = {}
    for iterms in str.split("|"):
        key, value = iterms.split(":")
        _dict[key] = int(value)
    print(_dict)

if __name__ == '__main__':
    str_to_dict(str1)
a = [1,2,3,4,5]
print(a[5:])