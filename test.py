# x = (i for i in range(100_000_000_000))

# print(x)
# print(x.__next__())
# print(x.__next__())

def gen():
    for i in range(100_000_000_000):
        yield i + 3

x = gen()

print(x)
print(x.__next__())
print(x.__next__())