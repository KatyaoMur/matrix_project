import math
n = int(input("строк:"))
m = int(input("столбцов:"))
count = 0
print("\nМатрица:")
for i in range(1, n+1):
    row = []
    for j in range(1, m+1):
        x=math.sin(i+j/2)
        row.append(x)
        if x > 0:
            count += 1
    print([round(x, 2) for x in row])
print(f"\nКоличество положительных элементов: {count}")
