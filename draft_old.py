from matplotlib import pyplot as plt
import requests
import player_ids
import numpy as np

# print(f"the id for Miguel is {player_ids.PLAYERS['Miguel']}")

# response = requests.get(
#     f"https://draft.premierleague.com/api/entry/{player_ids.PLAYERS['Miguel']}/history")

# data = response.json()


# def get_points_per_gameweek(src):
#     return [points['points'] for points in src['history']]


# gameweek_points = get_points_per_gameweek(data)

# gameweeks = list(range(1, len(gameweek_points) + 1))

# plt.plot(gameweeks, gameweek_points)
# plt.title('Ant\'s gameweek history')
# plt.xlabel('gameweeks')
# plt.ylabel('points')
# plt.show()

a2 = [43, 38, 47, 43, 24, 48, 49, 29, 42, 32, 49, 39,
      40, 45, 30, 61, 57, 17, 107, 36, 41, 44, 46, 55, 63]

m2 = [74, 86, 42, 67, 46, 52, 69, 43, 64, 54, 60, 36,
      49, 64, 33, 34, 36, 26, 99, 50, 47, 55, 56, 71, 55]


labels = list(range(1, len(a2) + 1))

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, a2, width, label='Ant')
rects2 = ax.bar(x + width / 2, m2, width, label='Mig')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Points')
ax.set_title('Head to Head By Gameweek')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.show()
