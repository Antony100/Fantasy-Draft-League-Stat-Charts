import argparse

import draft
from itertools import combinations


def get_head_to_head_results(league_id):
    """
    Generates line and bar charts of all combinations of players going
    head to head and saves them to the results folder.
    """
    draft_data = draft.DraftData(league_id)

    players = draft_data.player_ids

    player_combos = tuple(combinations(players, 2))

    for name1, name2 in player_combos:
        h2h = draft.HeadToHead(league_id, name1, name2)
        print(f'{name1} vs {name2}')
        h2h.plot_linechart()
        h2h.plot_barchart()


def get_league_stats(league_id):
    """
    Generates barcharts of the highest, lowest and average score of all
    the players in the league. Generates a boxplot based on all gameweek
    scores. Both are saved to the results folder.
    """
    ls = draft.LeagueStats(league_id)
    ls.plot_highest_scores()
    ls.plot_lowest_scores()
    ls.plot_average_scores()
    ls.plot_boxplot()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate Fantasy Draft Stats.'
        )
    parser.add_argument(
        '-l', '--league-id', required=True, type=int,
        help='The ID of the League',
    )

    args = parser.parse_args()

    get_head_to_head_results(args.league_id)
    get_league_stats(args.league_id)
