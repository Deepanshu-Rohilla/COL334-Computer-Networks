import matplotlib.pyplot as plt
import sys
file = sys.argv[1]
f = open(file,'r')
x = []
y = []
lines = f.readlines()
for line in lines:
	content = list(map(float, line.split('\t')))
	x.append(content[0])
	y.append(content[1])


plt.plot(x, y,c='y')
name = list(file.split('.'))[0]
plt.savefig(name + '.png')
plt.show()

