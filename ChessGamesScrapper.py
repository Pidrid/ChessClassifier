import requests
import random
import time
import csv
from bs4 import BeautifulSoup
from ChessGame import ChessGame


def main(first_page_url, csv_file_name, appending: bool = True):
    # Only first page contains Elo ratings of players
    players_dictionary = get_dictionary_of_players(first_page_url)

    list_of_games = get_list_of_games(first_page_url, players_dictionary)

    # Getting games from next pages

    is_blank_page = False
    url = first_page_url + '/?p=1&start=100'

    while not is_blank_page:
        random_number = random.uniform(5, 20)
        time.sleep(random_number)
        games = get_list_of_games(url, players_dictionary)
        if len(games) == 0:
            is_blank_page = True
        else:
            list_of_games += games
            url = first_page_url + '/?p=1&start=' + str(int(url.split('=')[-1]) + 100)

    save_games_to_csv_file(list_of_games, csv_file_name, appending)


def get_player_elo(player, players_dictionary):
    if player in players_dictionary:
        return players_dictionary[player]
    else:
        return 0


def convert_player_link_to_player_name(player_link):
    return player_link.split('/')[-1]


def get_dictionary_of_players(url):  # This function returns a dictionary with players and their Elo ratings
    result = requests.get(url)
    document = BeautifulSoup(result.text, 'html.parser')

    players = {}

    rows = document.find_all('tr', class_=['dark', 'light'])  # Finding all rows with class 'dark' or 'light'

    for row in rows:
        links = row.find_all('a')  # Finding all links in the row

        if len(links) == 1:
            # If there is only one link, it means that it is a player with his Elo rating
            player = convert_player_link_to_player_name(links[0]['href'])

            # Finding Elo rating
            elo_rating = row.find_all('td', align='center')[1].text

            if elo_rating.isdecimal():
                elo_rating = int(elo_rating)

            # Adding player and his Elo rating to the dictionary
            players[player] = elo_rating

    return players


def get_list_of_games(url, players_dictionary):
    result = requests.get(url)
    document = BeautifulSoup(result.text, 'html.parser')

    games = []

    rows = document.find_all('tr', class_=['dark', 'light'])  # Finding all rows with class 'dark' or 'light'

    for row in rows:

        links = row.find_all('a')  # Finding all links in the row

        if len(links) == 6:
            # If there are 6 links, it means that it is a game

            # Finding players
            white_player = convert_player_link_to_player_name(links[0]['href'])
            black_player = convert_player_link_to_player_name(links[1]['href'])

            # Finding result
            result = ''
            cells_with_center_align = row.find_all('td', align='center')  # Finding cells with align='center'
            for cell in cells_with_center_align:
                if cell.text.strip() in ['1-0', '0-1', '½-½']:  # If there is a result, it will be one of these three
                    result = cell.text.strip()
                    break

            # Finding opening
            opening = row.find('td', id='col-open').a.text.strip()

            # Creating a new ChessGame object and adding it to the games list
            game = ChessGame(white_player, black_player, opening, result)

            # Adding Elo ratings to the game
            game.set_white_player_elo(get_player_elo(white_player, players_dictionary))
            game.set_black_player_elo(get_player_elo(black_player, players_dictionary))

            games.append(game)

    return games


def save_games_to_csv_file(list_of_games, csv_file_name: str, appending: bool = True):
    if appending:
        with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for game in list_of_games:
                if game.validate():
                    writer.writerow(game.to_list())

    else:
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Writing header
            writer.writerow(['White player', 'White player Elo', 'Black player', 'Black player Elo', 'Opening Code',
                             'Opening', 'Result'])

            for game in list_of_games:
                if game.validate():
                    writer.writerow(game.to_list())


if __name__ == '__main__':
    # Example of usage
    # main('https://www.365chess.com/tournaments/World_Rapid_2018_2018/43111', 'World_Rapid_2018.csv', False)

    first_page = input('Enter the URL of the first page of the tournament: ')
    file_name = input('Enter the name of the file: ')
    write_or_append = input('Do you want to write or append to the file? (write/append): ')

    if write_or_append == 'write':
        main(first_page, file_name, True)
    else:
        main(first_page, file_name, False)
