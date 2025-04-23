import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)

plt.figure()
plt.hist(data, bins=30)
plt.title('Istogramma')
plt.xlabel('Valori')
plt.ylabel('Frequenza')
plt.show()