from matplotlib import pyplot as plt
import numpy as np
import requests
import player_ids
import player_ids_lg2


class DraftData():

    def __init__(self, player_ids):
        self.player_ids = player_ids

    def get_data(self, player_name):
        # make line fit
        player = requests.get(
            f"https://draft.premierleague.com/api/entry/{self.player_ids[player_name]}/history"
        )
        player_data = player.json()
        return player_data

    def get_points_per_gameweek(self, src):
        return [points['points'] for points in src['history']]

#     def get_gameweeks(self, src):
#         return list(range(1, len(src) + 1))

#     def get_gameweeks_points(self, player_name):
#         data = self.get_data(player_name)
#         points = self.get_points_per_gameweek(data)
# #         gameweeks = self.get_gameweeks(points)
#         return dict(enumerate(points, start=1))

#     def get_gameweeks_points(self, player_name):
#         data = self.get_data(player_name)
#         points = self.get_points_per_gameweek(data)
#         return {player_name: dict(enumerate(points, start=1))}

#     one-liner
#     def get_gameweeks_points(self, *players):
#         return {player_name: dict(enumerate(self.get_points_per_gameweek(self.get_data(player_name)), start=1)) for player_name in players}

    def get_gameweeks_points(self, *players):
        result = dict()
        for player_name in players:
            data = self.get_data(player_name)
            points = self.get_points_per_gameweek(data)
            result[player_name] = dict(enumerate(points, start=1))
        return result


class HeadToHead(DraftData):

    def __init__(self, player_ids, player1, player2):
        super().__init__(player_ids)
        self.player1 = player1
        self.player2 = player2
        self.players_scores = self.get_gameweeks_points(
            self.player1, self.player2)
#         self.p1_points = self.get_gameweeks_points(self.player1)
#         self.p2_points = self.get_gameweeks_points(self.player2)
        print(self.players_scores)

    def get_id(self, player_name):
        return self.player_ids[player_name]

    def plot_linechart(self):
        """
        plots the points and gameweeks for player 1 and 2 on a line chart
        and returns the chart
        """
        plt.style.use('ggplot')

        plt.minorticks_on()

        plt.plot(self.players_scores[self.player1].keys(
        ), self.players_scores[self.player1].values())
        plt.plot(self.players_scores[self.player2].keys(
        ), self.players_scores[self.player2].values())

        plt.xlabel('gameweeks')
        plt.ylabel('points')
        plt.legend([self.player1, self.player2])

        plt.show()

    def headtohead_score(self):
        """
        Compares the scores of each gameweek if players went head to head and returns
        a dict of how many wins each and draws (if any).

        """
        p1_win = 0
        p2_win = 0
        draw = 0
        for score in list(zip(self.players_scores[self.player1].values(), self.players_scores[self.player2].values())):
            if score[0] > score[1]:
                p1_win += 1
            elif score[1] > score[0]:
                p2_win += 1
            elif score[0] == score[1]:
                draw += 1
        return {self.player1: p1_win, self.player2: p2_win, "draw": draw}

    def plot_barchart(self):
        """
        Plots points and gameweeks for both players as a bar chart and returns
        bar chart with the total head to head score.

        """

        labels = list(self.players_scores[self.player1].keys())

        x = np.arange(len(labels))  # the label locations
        width = 0.4  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(
            x - width / 2,
            self.players_scores[self.player1].values(),
            width,
            label=self.player1
        )
        rects2 = ax.bar(
            x + width / 2, self.players_scores[self.player2].values(), width, label=self.player2)

        ax.set_ylabel('Points')
        ax.set_title('Head to Head By Gameweek')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        bbox_args = dict(boxstyle="round", fc="0.8")

#         ax.annotate(f'{self.player1}: {self.headtohead_score()[self.player1]}\n{self.player2}: {self.headtohead_score()[self.player2]}\n draw: {self.headtohead_score()["draw"]}', xy=(1, 1), xycoords='figure fraction',
#                      xytext=(-20, -20), textcoords='offset points',
#                      ha="right", va="top",
#                      bbox=bbox_args,

        ax.annotate(
            f'{self.player1}: {self.headtohead_score()[self.player1]}\n \
            {self.player2}: {self.headtohead_score()[self.player2]}\n \
            draw: {self.headtohead_score()["draw"]}',
            xy=(1, 1), xycoords='figure fraction',
            xytext=(-20, -20), textcoords='offset points',
            ha="right", va="top",
            bbox=bbox_args,
        )

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


class LeagueStats(DraftData):

    def __init__(self):
        pass

    def get_lowest_gameweek_score(self):
        pass

    def get_highest_gameweek_score(self):
        pass

    def plot_boxplot(self):
        pass

    def plot_averages_barchart(self):
        pass




# h = HeadToHead(player_ids.PLAYERS, 'Manesh', 'Llukman')


# h.show_graph()

lg2 = HeadToHead(player_ids_lg2.PLAYERS_LG2, 'Antony', 'Geno')

lg2.plot_barchart()
