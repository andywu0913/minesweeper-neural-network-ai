import numpy as np
import matplotlib.pyplot as plt

step = 1000

file = str(input()).replace(' ', '')
opened_counter = np.load(file)

opened_counter_avg = []

for i in range(len(opened_counter)):
	if i > 0 and i % step == 0:
		opened_counter_avg.append(np.mean(opened_counter[i-step:i]))

fig, ax1 = plt.subplots()
plt.title('Numbers of blocks NN opened per Game')
plt.xlabel('Game')
ax2 = ax1.twinx()

color = 'tab:blue'
ax1.set_ylabel('Opened Blocks', color=color)
ax1.plot(range(0, len(opened_counter)), opened_counter, color=color, alpha=0.75)
ax1.tick_params(axis='y', labelcolor=color)

color = 'black'
ax2.set_ylabel('Opened Blocks (Avg of {0} Games)'.format(step), color=color)
ax2.plot([ step * (i + 1) for i in range(len(opened_counter_avg))], opened_counter_avg, color=color, alpha=1)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.show()
