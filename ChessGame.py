class ChessGame:
    def __init__(self, white_player: str, black_player: str, opening: str, result: str):
        self.white_player = white_player
        self.white_player_elo = 0
        self.black_player = black_player
        self.black_player_elo = 0
        self.opening = opening
        self.result = result

    def validate(self):
        if (self.white_player == '' or self.black_player == '' or self.opening == '' or self.result == ''
                or self.white_player_elo == 0 or self.black_player_elo == 0):
            return False
        return True

    def change_players_links_to_players_names(self):
        self.white_player = self.white_player.split('/')[-1]
        self.black_player = self.black_player.split('/')[-1]

    def __str__(self):
        return f'{self.white_player} {self.white_player_elo} {self.black_player} {self.black_player_elo} {self.opening} {self.result}'