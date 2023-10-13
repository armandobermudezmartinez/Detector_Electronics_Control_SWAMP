import numpy as np
import matplotlib.pyplot as plt


def func(q, a=0.118, Q=10):
    return np.exp(-np.log((Q/q)**2)**2)


q = np.linspace(10, 90)


print(func(q))

plt.plot(q, func(q))
plt.show()
