import matplotlib.pyplot as plt
import numpy as np

# Dati
x = np.linspace(0, 2*np.pi, 50)
y = np.sin(x)

plt.figure(figsize=(6,4))
plt.plot(x, y, label='sin(x)')

# Punto di massimo
max_idx = np.argmax(y)
x_max, y_max = x[max_idx], y[max_idx]
plt.scatter([x_max], [y_max], color='red')  # evidenziamo il punto
plt.annotate("Massimo locale",
             xy=(x_max, y_max),              # coordinate del punto
             xytext=(x_max+0.5, y_max-0.3),  # posizione del testo
             arrowprops=dict(arrowstyle="->", lw=1.5))  # freccia

plt.title("Annotazione di un punto critico")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.legend()
plt.grid(True)
plt.show()