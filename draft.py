import os
import requests

from matplotlib import pyplot as plt

import numpy as np

CURRENT_DIR = os.getcwd()
RESULTS_DIR_PATH = os.path.join(CURRENT_DIR, 'results')
BASE_URL = "https://draft.premierleague.com/api/"


class DraftData():
    """
    Retrieves the draft data from the draft league API and filters data
    to return player names and their gameweek points.
    """

    def __init__(self, league_id):
        self.league_id = league_id

    @property
    def player_ids(self):
        try:
            return self._player_ids
        except AttributeError:
            self._player_ids = self.get_player_ids()
            return self._player_ids

    def get_api_data(self, BASE_URL=BASE_URL, url=''):
        """Makes a call to the API and returns the result as json."""
        response = requests.get(BASE_URL + url)

        response.raise_for_status()

        if response.status_code == 200:
            return response.json()

    def get_player_ids(self):
        """
        retrieves league details and returns a dictionary of all players
        and their league IDs.
        """
        league_details = self.get_api_data(
            url=f"league/{self.league_id}/details"
        )
        result = dict()

        for player in league_details['league_entries']:
            result[player['player_first_name']] = player['entry_id']

        return result

    def get_player_history(self, player_name):
        """ Retrieves and returns the player's history. """
        return self.get_api_data(
            url=f"entry/{self.player_ids[player_name]}/history"
        )

    def get_points_per_gameweek(self, src):
        """
        Returns a list of points from every gameweek filtered from the
        player's history.
        """
        return [points['points'] for points in src['history']]

    def get_players_points(self, *players, format_type="dict"):
        """
        returns a dictionary of players and their gameweek score points.
        specify format_type (by default a dictionary) of either
        a list or dictionary to change the gameweek points as either a
        dictionary of gameweek number and points or a list of just the
        points.
        """
        result = dict()
        for player_name in players:
            data = self.get_player_history(player_name)
            points = self.get_points_per_gameweek(data)
            if format_type == "dict":
                result[player_name] = dict(enumerate(points, start=1))
            elif format_type == "list":
                result[player_name] = list(points)
        return result


class HeadToHead(DraftData):
    """
    Takes the gameweek data of 2 specified players and plots line and
    barcharts if players went head to head.
    """

    def __init__(self, league_id, player1, player2):
        super().__init__(league_id)
        self.player1 = player1
        self.player2 = player2
        self.players_scores = self.get_players_points(
            self.player1, self.player2)

    def headtohead_score(self):
        """
        Compares the scores of each gameweek if players went
        head to head and returns a dict of how many wins each and draws
        (if any).
        """
        p1_win = 0
        p2_win = 0
        draw = 0
        for score in list(
            zip(
                self.players_scores[self.player1].values(),
                self.players_scores[self.player2].values()
            )
        ):
            if score[0] > score[1]:
                p1_win += 1
            elif score[1] > score[0]:
                p2_win += 1
            elif score[0] == score[1]:
                draw += 1
        return {self.player1: p1_win, self.player2: p2_win, "draw": draw}

    def plot_linechart(self):
        """
        Plots the points and gameweeks for player 1 and 2 on a line chart
        and saves the chart to the results folder.
        """
        plt.style.use('ggplot')
        fig, ax = plt.subplots()

        plt.minorticks_on()

        plt.plot(self.players_scores[self.player1].keys(
        ), self.players_scores[self.player1].values())
        plt.plot(self.players_scores[self.player2].keys(
        ), self.players_scores[self.player2].values())

        plt.xlabel('gameweeks')
        plt.ylabel('points')
        plt.legend([self.player1, self.player2])

        fig.set_size_inches(18.5, 10.5, forward=True)

        # plt.show()

        try:
            os.mkdir(RESULTS_DIR_PATH)
        except FileExistsError:
            pass

        file_name = f'{self.player1}_{self.player2}_line.jpg'
        file_path = os.path.join(RESULTS_DIR_PATH, file_name)

        plt.savefig(file_path, orientation='landscape')
        plt.close()

    def plot_barchart(self):
        """
        Plots points and gameweeks for both players as a bar chart and
        saves the bar chart with the total head to head score as a
        label.
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
            x + width / 2, self.players_scores[self.player2].values(),
            width, label=self.player2
        )

        ax.set_ylabel('Points')
        ax.set_title('Head to Head By Gameweek')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        bbox_args = dict(boxstyle="round", fc="0.8")

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
            """
            Attach a text label above each bar in *rects*,
            displaying its height.
            """
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)

        fig.set_size_inches(18.5, 10.5, forward=True)

        plt.savefig(
            f'{os.getcwd()}/results/{self.player1}_{self.player2}_bar.jpg',
            orientation='landscape'
        )
        plt.close()


class LeagueStats(DraftData):
    """
    Returns the highest, lowest and average gameweek score of each
    player in barcharts and also as a boxplot.
    """

    def __init__(self, league_id):
        super().__init__(league_id)
        self.all_player_scores = self.get_players_points(
            *self.player_ids, format_type='list'
        )
        print(self.all_player_scores)

    def calc_average(self, lst):
        try:
            return sum(lst) // len(lst)
        except ZeroDivisionError:
            print("Cannot divide by zero")

    def get_gameweek_statistic(self, func):
        """
        Returns a gameweek statistic from the player scores based on the
        function given to the func argument.
        """
        return {
            player: func(self.all_player_scores[player])
            for player in self.all_player_scores
        }

    def barchart(self, scores, title):
        """
        Plots a barchart of single bars that are annotated with values.
        """

        labels = list(scores.keys())

        plt.style.use('bmh')

        x = np.arange(len(labels))  # the label locations
        width = 0.4  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x, scores.values(), width)

        ax.set_ylabel('Points')
        ax.set_xlabel('players')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)

        def autolabel(rects):
            """
            Attach a text label above each bar in *rects*, displaying
            its height.
            """
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)

        fig.tight_layout()
        fig.set_size_inches(18.5, 10.5, forward=True)

        plt.savefig(
            f'{os.getcwd()}/results/{title}.jpg',
            orientation='landscape'
        )
        plt.close()

    def plot_boxplot(self):
        """
        Saves a boxplot of all the players' scores.
        """
        plt.style.use('bmh')
        plt.minorticks_on()
        plt.xlabel('Players')
        plt.ylabel('Points')
        plt.boxplot(
            self.all_player_scores.values(),
            labels=(list(self.all_player_scores.keys()))
        )
        plt.savefig(
            f'{os.getcwd()}/results/boxplot.jpg', orientation='landscape'
        )
        plt.close()

    def plot_highest_scores(self):
        """
        Saves a barchart of all the players and their highest gameweek
        score.
        """
        return self.barchart(
            self.get_gameweek_statistic(max),
            'Highest Gameweek Scores Per Player'
        )

    def plot_lowest_scores(self):
        """
        Saves a barchart of all the players and their lowest gameweek
        score.
        """
        return self.barchart(
            self.get_gameweek_statistic(min),
            'Lowest Gameweek Scores Per Player'
        )

    def plot_average_scores(self):
        """
        Saves a barchart of all the players and their average gameweek
        score.
        """
        return self.barchart(
            self.get_gameweek_statistic(self.calc_average),
            'Average Gameweek Scores Per Player'
        )
