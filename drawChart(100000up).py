import numpy as np
import matplotlib.pyplot as plt
import more_itertools as mit

step = 500

file = str(input()).replace(' ', '')
opened_counter = np.load(file)
file = str(input()).replace(' ', '')
win_counter = np.load(file)

temp = []
opened_counter_avg = []
win_counter_avg = []

win_counter_consecutives = []
for i in range(1, len(win_counter)):
	if win_counter[i] - 1 == win_counter[i - 1]:
		win_counter_consecutives.append(i)
win_counter = np.delete(win_counter, win_counter_consecutives)

# print(np.array([list(group) for group in mit.consecutive_groups(win_counter)]))

for i in range(100000, len(opened_counter[100000:]) + 100000, step):
	count = 0
	for j in range(0, len(win_counter)):
		if i <= win_counter[j] < (i + step):
			count += 1
	win_counter_avg.append(count)
win_counter_avg.pop(len(win_counter_avg) - 1)

for i in range(100000, len(opened_counter[100000:]) + 100000):
	temp.append(opened_counter[i] if opened_counter[i] > 1 else np.nan)
	if i > 0 and i % step == 0:
		opened_counter_avg.append(np.nanmean(temp[i-100000-step:i-100000]))

fig, ax1 = plt.subplots()
plt.title('NN Training Records in 8x8 Board')
plt.xlabel('Game')
ax2 = ax1.twinx()

color = 'tab:blue'
ax1.set_ylabel('Opened Blocks per Game', color=color)
ax1.plot(range(100000, len(temp) + 100000), temp, color=color, alpha=0.75)
ax1.tick_params(axis='y', labelcolor=color)

color = 'black'
ax2.set_ylabel('Number of Wins in every {0} Games'.format(step), color=color)
ax2.plot(range(100000, len(opened_counter[100000:-step]) + 100000, step), win_counter_avg, color=color, alpha=1)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 50)

fig.tight_layout()
plt.show()
