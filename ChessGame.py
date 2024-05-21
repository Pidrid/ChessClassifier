def get_opening_from_opening_code(opening_code: str):
    if (len(opening_code) != 3
            or not opening_code[1].isdecimal()
            or not opening_code[2].isdecimal()):
        return 'Unknown'

    label = opening_code[0]
    number = int(opening_code[1]) * 10 + int(opening_code[2])

    if label == 'A':
        return get_opening_from_opening_code_a(number)
    elif label == 'B':
        return get_opening_from_opening_code_b(number)
    elif label == 'C':
        return get_opening_from_opening_code_c(number)
    elif label == 'D':
        return get_opening_from_opening_code_d(number)
    elif label == 'E':
        return get_opening_from_opening_code_e(number)
    else:
        return 'Unknown'


def get_opening_from_opening_code_a(number: int):
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
    else:
        return 'Unknown'


def get_opening_from_opening_code_b(number: int):
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
    else:
        return 'Unknown'


def get_opening_from_opening_code_c(number: int):
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
    else:
        return 'Unknown'


def get_opening_from_opening_code_d(number: int):
    if number <= 5:
        return 'D00–D05'
    elif number <= 69:
        return 'Queen’s Gambit'
    elif number <= 79:
        return 'Neo-Grünfeld'
    elif number <= 99:
        return 'Grünfeld'
    else:
        return 'Unknown'


def get_opening_from_opening_code_e(number: int):
    if number <= 9:
        return 'E00–E09'
    elif number <= 59:
        return 'Indian systems with ...e6'
    elif number <= 99:
        return 'King’s Indian'
    else:
        return 'Unknown'


class ChessGame:
    def __init__(self, white_player: str, black_player: str, opening_code: str, result: str):
        self.white_player = white_player
        self.__white_player_elo = 0
        self.black_player = black_player
        self.__black_player_elo = 0
        self.opening_code = opening_code
        self.__result = result

    def __str__(self):
        return (f'{self.white_player} {self.__white_player_elo} {self.black_player} {self.__black_player_elo} '
                f'{self.opening_code} {self.opening} {self.__result}')

    @property
    def opening(self):
        return get_opening_from_opening_code(self.opening_code)

    def get_white_player_elo(self):
        return self.__white_player_elo

    def set_white_player_elo(self, value: int):
        if value >= 0:
            self.__white_player_elo = value

    def get_black_player_elo(self):
        return self.__black_player_elo

    def set_black_player_elo(self, value: int):
        if value >= 0:
            self.__black_player_elo = value

    def get_result(self):
        return self.__result

    def set_result(self, value: str):
        if value in ['1-0', '0-1', '½-½']:
            self.__result = value

    def validate(self):
        if (self.white_player == ''
                or self.black_player == ''
                or self.white_player == self.black_player
                or self.__white_player_elo <= 0
                or self.__black_player_elo <= 0
                or self.opening == 'Unknown'
                or self.__result not in ['1-0', '0-1', '½-½']):
            return False
        return True

    def change_players_links_to_players_names(self):
        self.white_player = self.white_player.split('/')[-1]
        self.black_player = self.black_player.split('/')[-1]

    def to_list(self):
        return [self.white_player, self.__white_player_elo, self.black_player, self.__black_player_elo,
                self.opening_code,
                self.opening, self.__result]
