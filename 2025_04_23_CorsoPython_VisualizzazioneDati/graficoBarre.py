import matplotlib.pyplot as plt

categories = ['A','B','C','D','E']
values = [6,7,22,56,10]

plt.figure()
plt.bar(categories,values)
plt.title('Grafico a Barre')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.show()