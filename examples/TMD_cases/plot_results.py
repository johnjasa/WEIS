import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


data = np.loadtxt('results.txt', delimiter=',')

mass = data[:, 0]
diameters = data[:, 1:4]
thickness = data[:, 4:7]
tower_damage = data[:, 7]
freqs = data[:, 8]

plt.figure()
plt.scatter(mass, tower_damage)
ax = plt.gca()
ax.set_yscale('log')
plt.axhline(y=1.0, color='r', linestyle='-')
plt.xlabel('Tower mass, kg')
plt.ylabel('Tower base damage')
plt.savefig('damage.png', dpi=300)

plt.figure()
plt.scatter(mass, freqs)
ax = plt.gca()
plt.xlabel('Tower mass, kg')
plt.ylabel('Tower fund. freq, Hz')
plt.savefig('freqs.png', dpi=300)

plt.figure()
plt.scatter(freqs, tower_damage)
ax = plt.gca()
ax.set_yscale('log')
plt.axhline(y=1.0, color='r', linestyle='-')
plt.xlabel('Tower fund. freq, Hz')
plt.ylabel('Tower base damage')
plt.savefig('damage_vs_freqs.png', dpi=300)


fig, axarr = plt.subplots(3, 1, sharex=True, figsize=(6, 10))
for idx in range(3):
    axarr[idx].scatter(thickness[:, idx], tower_damage)
    axarr[idx].set_yscale('log')
    axarr[idx].axhline(y=1.0, color='r', linestyle='-')
    axarr[idx].set_xlabel(f'Thickness point {idx}, m')
    axarr[idx].set_ylabel('Tower base damage')

    # # create a linear regression model
    # model = LinearRegression()
    # model.fit(thickness[:, idx].reshape(-1, 1), tower_damage)
    # 
    # # predict y from the data
    # x_new = np.linspace(0, 0.2, 100)
    # y_new = model.predict(x_new[:, np.newaxis])
    # 
    # axarr[idx].plot(x_new, y_new, color='k', lw=2)

plt.savefig('thickness.png', dpi=300)


fig, axarr = plt.subplots(3, 1, sharex=True, figsize=(6, 10))
for idx in range(3):
    axarr[idx].scatter(diameters[:, idx], tower_damage)
    axarr[idx].set_yscale('log')
    axarr[idx].axhline(y=1.0, color='r', linestyle='-')
    axarr[idx].set_xlabel(f'Diameter point {idx}, m')
    axarr[idx].set_ylabel('Tower base damage')

    # # create a linear regression model
    # model = LinearRegression()
    # model.fit(diameters[:, idx].reshape(-1, 1), tower_damage)
    # 
    # # predict y from the data
    # x_new = np.linspace(3.75, 8., 100)
    # y_new = model.predict(x_new[:, np.newaxis])
    # 
    # axarr[idx].plot(x_new, y_new, color='k', lw=2)

plt.savefig('diameters.png', dpi=300)