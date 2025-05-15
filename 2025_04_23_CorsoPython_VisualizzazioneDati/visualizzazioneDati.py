import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style='darkgrid')

data = np.random.normal(size=100)

sns.histplot(data, kde=True)
plt.title('Distribuzione dei dati')
# plt.show()

# Crea una figura
fig = plt.figure()

ax = fig.add_subplot(111)

plt.show()