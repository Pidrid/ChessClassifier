import csv
import time

from ChessGame import ChessGame
from bs4 import BeautifulSoup
import requests


def main():
    url1 = 'https://www.365chess.com/tournaments/bundesliga_2023-24_2023/45995'  # First page
    url2 = 'https://www.365chess.com/tournaments/bundesliga_2023-24_2023/45995/?p=1&start=100'  # Second page
    url3 = 'https://www.365chess.com/tournaments/bundesliga_2023-24_2023/45995/?p=1&start=200'  # Third page

    # Only first page contains Elo ratings of players
    players_dictionary = get_dictionary_of_players(url1)

    # Getting list of games from all pages
    time.sleep(14.4)  # Using sleep to avoid getting banned
    list_of_games = get_list_of_games(url1, players_dictionary)

    time.sleep(11.24)
    list_of_games += get_list_of_games(url2, players_dictionary)

    time.sleep(21.9)
    list_of_games += get_list_of_games(url3, players_dictionary)

    # Changing players' links to players' names
    for game in list_of_games:
        game.change_players_links_to_players_names()

    # Saving games to a CSV file
    csv_file = 'games.csv'
    save_games_to_csv_file(list_of_games, 'games.csv')


def get_player_elo(player_link, players_dictionary):
    if player_link in players_dictionary:
        return players_dictionary[player_link]
    else:
        return 0


def get_dictionary_of_players(url):  # This function returns a dictionary with players and their Elo ratings
    result = requests.get(url)
    document = BeautifulSoup(result.text, 'html.parser')

    players = {}

    rows = document.find_all('tr', class_=['dark', 'light'])  # Finding all rows with class 'dark' or 'light'

    for row in rows:
        links = row.find_all('a')  # Finding all links in the row

        if len(links) == 1:
            # If there is only one link, it means that it is a player with his Elo rating
            link_to_player = links[0]['href']

            # Find Elo rating
            elo_rating = row.find_all('td', align='center')[1].text

            players[link_to_player] = elo_rating

    return players


def get_list_of_games(url, players_dictionary):  # This function returns a list of ChessGame objects from next pages
    result = requests.get(url)
    document = BeautifulSoup(result.text, 'html.parser')

    games = []

    rows = document.find_all('tr', class_=['dark', 'light'])  # Finding all rows with class 'dark' or 'light'

    for row in rows:

        links = row.find_all('a')  # Finding all links in the row

        if len(links) == 6:
            # If there are 6 links, it means that it is a game

            # Find players
            link_to_white_player = links[0]['href']
            link_to_black_player = links[1]['href']

            # Find result
            result = ''
            cells_with_center_align = row.find_all('td', align='center')  # Finding cells with align='center'
            for cell in cells_with_center_align:
                if cell.text.strip() in ['1-0', '0-1', '½-½']:  # If there is a result, it will be one of these three
                    result = cell.text.strip()
                    break

            # Find opening
            opening = row.find('td', id='col-open').a.text.strip()

            # Create a new ChessGame object and adding it to the games list
            game = ChessGame(link_to_white_player, link_to_black_player, opening, result)

            # Adding Elo ratings to the game
            game.white_player_elo = get_player_elo(link_to_white_player, players_dictionary)
            game.black_player_elo = get_player_elo(link_to_black_player, players_dictionary)

            games.append(game)

    return games


def save_games_to_csv_file(games, file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["White Player", "White Player Elo", "Black Player", "Black Player Elo", "Opening", "Result"])

        for game in games:
            writer.writerow(game.to_list())


if __name__ == '__main__':
    main()
