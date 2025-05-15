import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Creiamo un DataFrame per sfruttare relplot
import pandas as pd
t = np.linspace(0, 2*np.pi, 200)
df = pd.DataFrame({
    "t": np.concatenate([t, t]),
    "valore": np.concatenate([np.sin(t), np.cos(t)]),
    "funzione": ["seno"]*len(t) + ["coseno"]*len(t)
})

# relplot genera automaticamente sottotrame se dividiamo per "funzione"
sns.set_theme(style="ticks")

g = sns.relplot(
    data=df,
    x="t", y="valore",
    kind="line",
    col="funzione",            # una colonna per ogni funzione
    height=4, aspect=1.5,       # dimensioni di ciascuna subplot
    facet_kws={"sharex": True}
)
g.set_axis_labels("Angolo (rad)", "Valore")
g.set_titles("{col_name}")
plt.show()