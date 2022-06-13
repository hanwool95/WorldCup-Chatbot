from bs4 import BeautifulSoup
import urllib.request
import csv

from wiki import Craw


class Team_Craw(Craw):
    def __init__(self):
        super().__init__()
        self.confederation = ""
        self.head_coach = ""
        self.captain = ""
        self.fifa_code = ""
        self.ranking = 0
        self.appearances = 0
        self.best_record = ""
        self.players_dict = {}

    def find_information(self):
        print(self.target_url)
        with urllib.request.urlopen(self.target_url) as url:
            doc = url.read()
            soup = BeautifulSoup(doc, "html.parser")
            infobox = soup.find_all('table', 'infobox')[0]
            team_rows = infobox.find_all('tr')
            self.insert_information_from_rows(team_rows)
            players_rows = soup.find_all('tr', 'nat-fs-player')
            self.insert_players_dict_from_rows(players_rows)
        print(self.players_dict)

    def insert_information_from_rows(self, rows):
        world_cup_info_flag = False
        for row in rows:
            infobox = row.find('th', 'infobox-label')
            if infobox:
                information_type = infobox.text
                value = row.find('td', 'infobox-data').text

                if information_type == "Confederation":
                    self.confederation = value
                    print("Confederation: ", self.confederation)
                elif information_type == "Head coach":
                    self.head_coach = value
                    print("Head Coach: ", self.head_coach)
                elif information_type == "Captain":
                    self.captain = value
                    print("Captain: ", self.captain)
                elif information_type == "FIFA code":
                    self.fifa_code = value
                    print("code: ", self.fifa_code)
                elif information_type == "Current":
                    self.ranking = value.split(" ")[1]
                    print("ranking: ", self.ranking)
                elif information_type == "Appearances":
                    if world_cup_info_flag:
                        self.appearances = value
                        print("appearances: ", self.appearances)
                elif information_type == "Best result":
                    if world_cup_info_flag:
                        self.best_record = value
                        print("best record: ", self.best_record)
            else:
                info_header = row.find('th', 'infobox-header')
                if info_header:
                    information_head = info_header.text
                    if information_head == "World Cup":
                        world_cup_info_flag = True
                    else:
                        world_cup_info_flag = False

    def insert_players_dict_from_rows(self, rows):
        for player_row in rows:
            player = player_row.find('th').find('a')
            link = player['href']
            player_name = player.text
            self.players_dict[player_name] = link


class WordCup_Team:
    def __init__(self):
        self.world_cup_url = "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup"
        self.teams_dict = {}

    def find_team_list(self):
        with urllib.request.urlopen(self.world_cup_url) as url:
            doc = url.read()
            soup = BeautifulSoup(doc, "html.parser")
            Draw_content = soup.find_all('table', 'wikitable')[1]
            participants = Draw_content.find_all('a')
            for participant in participants:
                team_name = participant.text
                if team_name != "[d]":
                    self.teams_dict[team_name] = participant['href']

    def search_all_teams(self):
        for team_name, url in self.teams_dict.items():
            team_crawler = Team_Craw()
            team_crawler.set_target(url)
            team_crawler.find_information()

    def find_match_list(self):
        with urllib.request.urlopen(self.world_cup_url) as url:
            doc = url.read()
            soup = BeautifulSoup(doc, "html.parser")
            matches = soup.find_all('div', 'footballbox')


if __name__ == "__main__":
    crawler = WordCup_Team()
    crawler.find_team_list()
    crawler.search_all_teams()