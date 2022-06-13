from bs4 import BeautifulSoup
import urllib.request
import csv

from wiki import Craw


class Team_Craw(Craw):
    def __init__(self, team_name: str):
        super().__init__()
        self.team_name = team_name
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

    def insert_information_from_rows(self, rows: list):
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

    def insert_players_dict_from_rows(self, rows: list):
        for player_row in rows:
            player = player_row.find('th').find('a')
            link = player['href']
            player_name = player.text
            self.players_dict[player_name] = link


class WorldCup_Team:
    def __init__(self):
        self.world_cup_url = "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup"
        self.teams_dict = {}
        self.teams_information = []
        self.players_information_dict = {}
        self.matches_dict = {}

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
            team_crawler = Team_Craw(team_name)
            team_crawler.set_target(url)
            team_crawler.find_information()
            self.teams_information.append(team_crawler)

    def find_match_list(self):
        with urllib.request.urlopen(self.world_cup_url) as url:
            doc = url.read()
            soup = BeautifulSoup(doc, "html.parser")
            matches = soup.find_all('div', 'footballbox')

            teams_dict = {}

            for match in matches:
                time_div = match.find('div', 'fleft')
                date = time_div.find('div', 'fdate').text.replace("\xa0", " ")
                time = time_div.find('div', 'ftime').text
                date_time = date + " " + time
                home_team_name = match.find('th', 'fhome').text.replace("\xa0", "")
                away_team_name = match.find('th', 'faway').text.replace("\xa0", "")

                if home_team_name not in teams_dict.keys():
                    teams_dict[home_team_name] = []
                teams_dict[home_team_name].append([date_time, away_team_name])

                if away_team_name not in teams_dict.keys():
                    teams_dict[away_team_name] = []
                teams_dict[away_team_name].append([date_time, home_team_name])
            self.matches_dict = teams_dict

    def write_team_to_csv(self):
        with open('team.csv', 'w') as file:
            writer = csv.writer(file)
            print("writing team to csv")
            print(self.teams_information)
            for team_information in self.teams_information:
                result = [team_information.team_name, team_information.confederation,
                          team_information.head_coach, team_information.captain, team_information.fifa_code,
                          team_information.ranking, team_information.appearances, team_information.best_record]

                writer.writerow(result)

                self.players_information_dict[team_information.team_name] = team_information.players_dict

    def write_matches_to_csv(self):
        with open('match.csv', 'w') as file:
            writer = csv.writer(file)
            print("writing match to csv")
            for country, matches in self.matches_dict.items():

                for i, match in enumerate(matches):
                    order = i + 1
                    date = match[0]
                    opp = match[1]
                    result = [country, order, date, opp]

                    writer.writerow(result)

    def get_player_dict(self) -> dict:
        return self.players_information_dict


class WorldCup_Player:
    def __init__(self, players_information_dict: dict):
        self.players_information_dict = players_information_dict

    def write_players_dict_to_csv(self):
        with open('player.csv', 'w') as file:
            print("writing player to csv")
            print(self.players_information_dict)
            writer = csv.writer(file)
            for team_name, players_dict in self.players_information_dict.items():
                for player_name, player_url in players_dict.items():
                    result = [team_name, player_name, player_url]
                    writer.writerow(result)


if __name__ == "__main__":
    crawler = WorldCup_Team()
    crawler.find_team_list()
    crawler.search_all_teams()
    crawler.write_team_to_csv()
    player = WorldCup_Player(crawler.get_player_dict())
    player.write_players_dict_to_csv()
    crawler.find_match_list()
    crawler.write_matches_to_csv()
