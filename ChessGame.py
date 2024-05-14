def get_opening_from_opening_code(opening_code: str):
    if len(opening_code) != 3:
        return 'Unknown'
    label = opening_code[0]
    if opening_code[1].isdecimal() == False or opening_code[2].isdecimal() == False:
        return 'Unknown'
    number = int(opening_code[1])*10 + int(opening_code[2])
    if label == 'A':
        if number == 0:
            return 'A00'
        elif number == 1:
            return 'Larsen Opening'
        elif number <= 3:
            return 'Bird Opening'
        elif number <= 9:
            return 'Réti Opening'
        elif number <= 39:
            return 'English Opening'
        elif number <= 42:
            return 'A40–A42'
        elif number <= 44:
            return 'Old Benoni Defence'
        elif number <= 49:
            return 'A45–A49'
        elif number <= 79:
            return 'Atypical Indian systems'
        elif number <= 99:
            return 'Dutch Defence'
    elif label == 'B':
        if number == 0:
            return 'B00'
        elif number == 1:
            return 'Scandinavian Defence'
        elif number <= 5:
            return 'Alekhine Defence'
        elif number == 6:
            return 'Modern Defence'
        elif number <= 9:
            return 'Pirc Defence'
        elif number <= 19:
            return 'Caro-Kann Defence'
        elif number <= 99:
            return 'Sicilian Defence'
    elif label == 'C':
        if number <= 19:
            return 'French Defence'
        elif number <= 24:
            return 'C20-C24'
        elif number <= 29:
            return 'Vienna Game'
        elif number <= 39:
            return 'King’s gambit'
        elif number == 40:
            return 'C40'
        elif number == 41:
            return 'Philidor Defence'
        elif number <= 43:
            return 'Petrov’s Defence'
        elif number == 44:
            return 'C44'
        elif number == 45:
            return 'Scotch Game'
        elif number <= 49:
            return 'C46–C49'
        elif number <= 59:
            return 'Italian Game'
        elif number <= 99:
            return 'Ruy Lopez'

    elif label == 'D':
        if number <= 5:
            return 'D00–D05'
        elif number <= 69:
            return 'Queen’s Gambit'
        elif number <= 79:
            return 'Neo-Grünfeld'
        elif number <= 99:
            return 'Grünfeld'

    elif label == 'E':
        if number <= 59:
            return 'Indian systems with ...e6'
        elif number <= 99:
            return 'King’s Indian'
    else:
        return 'Unknown'


class ChessGame:
    def __init__(self, white_player: str, black_player: str, opening_code: str, result: str):
        self.white_player = white_player
        self._white_player_elo = 0
        self.black_player = black_player
        self._black_player_elo = 0
        self.opening_code = opening_code
        self.result = result
        self._opening = get_opening_from_opening_code(self.opening_code)

    def __str__(self):
        return (f'{self.white_player} {self._white_player_elo} {self.black_player} {self._black_player_elo} '
                f'{self.opening_code} {self._opening} {self.result}')

    def get_white_player_elo(self):
        return self._white_player_elo

    def set_white_player_elo(self, value):
        self._white_player_elo = value

    def get_black_player_elo(self):
        return self._black_player_elo

    def set_black_player_elo(self, value):
        self._black_player_elo = value

    def get_opening(self):
        return self._opening

    def validate(self):
        if (self.white_player == ''
                or self.black_player == ''
                or self.opening_code == ''
                or self._opening == ''
                or self._white_player_elo == 0
                or self._black_player_elo == 0
                or self._opening == 'Unknown'
                or self.result not in ['1-0', '0-1', '½-½']
                or self.white_player == self.black_player):
            return False
        return True

    def change_players_links_to_players_names(self):
        self.white_player = self.white_player.split('/')[-1]
        self.black_player = self.black_player.split('/')[-1]

    def to_list(self):
        return [self.white_player, self._white_player_elo, self.black_player, self._black_player_elo, self.opening_code,
                self._opening, self.result]
