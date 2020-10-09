
a = 0
b = 0 
length = 0
res = 0
i = 1

a = int(input())
b = int(input())

if a > b:
	length = b
else:
	length = a

while i <= length:

	if a % i == 0 and b % i == 0:
		res = i
	i = i + 1

print(res)
