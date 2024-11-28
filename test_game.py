from game.types.enums import Phase

def test_phase_advancement(game):
    assert game.current_phase == Phase.INVOCATION
    game._advance_phase()
    assert game.current_phase == Phase.PREPARATION

def test_card_playing(game):
    player = game.players[0]
    initial_hand_size = len(player.hand)
    initial_skp = player.current_skp
    
    card = player.hand[0]
    result = game._attempt_play_card(card)
    
    assert result == True
    assert len(player.hand) == initial_hand_size - 1
    assert player.current_skp == initial_skp - card.skp_cost

def test_game_initialization():
    game = TestamentDuelGame()
    assert game.players[0].name == "Player 1"
    assert game.players[1].name == "Player 2"
    assert len(game.players[0].deck) == 20  # Assuming starting deck size
    assert len(game.players[1].deck) == 20

def test_game_winner():
    game = TestamentDuelGame()
    game.start()
    assert game.winner is not None