import sys

while True:
    height = input("Height: ")
    if height.isnumeric() == True:
        height = int(height)
        if height >= 1 and height <= 8:
            break

for i in range(1, height + 1):
    for j in range(1, height + 1):
        if i > height - j:
            sys.stdout.write("#")
        else:
            sys.stdout.write(" ")
    sys.stdout.write("\n")
