import draft
from itertools import combinations
from config import LEAGUE_ID


def get_head_to_head_results():
    """
    Generates line and bar charts of all combinations of players going
    head to head and saves them to the results folder.
    """
    draft_data = draft.DraftData(LEAGUE_ID)

    players = draft_data.get_player_ids()

    player_combos = tuple(combinations(players, 2))

    for name1, name2 in player_combos:
        h2h = draft.HeadToHead(LEAGUE_ID, name1, name2)
        h2h.plot_linechart()
        h2h.plot_barchart()


def get_league_stats():
    """
    Generates barcharts of the highest, lowest and average score of all
    the players in the league. Generates a boxplot based on all gameweek
    scores. Both are saved to the results folder.
    """
    ls = draft.LeagueStats(LEAGUE_ID)
    ls.plot_highest_scores()
    ls.plot_lowest_scores()
    ls.plot_average_scores()
    ls.plot_boxplot()


if __name__ == '__main__':
    get_head_to_head_results()
    get_league_stats()
