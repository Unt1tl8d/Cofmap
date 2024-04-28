a = [1, 3, 4, 5]
b = [4, 5, 6, 7]
n = []
for i in a:
    for f in b:
        if i == f:
            b.remove(i)
print(b)

for i in b:
    if i not in a:
        n.append(i)
print(n)
