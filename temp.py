import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(figsize=(10, 5))
N = 2000
values, bins, patches = axs.hist(np.random.randn(N), bins=10, rwidth=0.8, color='dodgerblue', edgecolor='white')
for val, b0, b1 in zip(values, bins[:-1], bins[1:]):
    print(f'Bin {b0:.3f},{b1:.3f}: {val:.0f} entries ({val / N * 100:.2f} %)')
    axs.axvspan(b0, b1, alpha=0.1, zorder=0)
axs.margins(x=0)
plt.show()