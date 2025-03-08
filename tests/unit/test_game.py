from tic_tac.core import game, board
import pytest


@pytest.fixture
def game_instance():
    number_of_players = 2
    width, height = 7, 5
    win_length = 3
    board_inst = board.Board(width=width, height=height, win_length=win_length)

    return game.Game(
        board=board_inst,
        number_of_players=number_of_players,
    )


def test_game_basic_run(game_instance: game.Game):
    positions = [(0, 0), (0, 1), (0, 2)]
    player = game_instance.players[0]

    for position in positions:
        game_instance.board.step(position=position, player=player)

    status = game_instance.board.check_solution(
        current_position=positions[-1],
        player=player,
    )
    assert status == board.BoardStatus.ENDED


def test_predict_next_step(game_instance: game.Game):
    # TODO add more test cases
    positions = [(0, 0), (1, 1)]
    player = game_instance.players[0]

    for position in positions:
        game_instance.board.step(position=position, player=player)

    next_position = game_instance.board.predict_next_position(
        current_player=player,
    )
    assert next_position == (2, 2)
