import csv


class Query:
    who_start = "who is "
    what_start = "what is "
    when_start = "when is "
    match_dict = {'1': "first match", '2': "second match", '3': 'third match'}

    def __init__(self):
        self.code_dict = {}
        self.teams_information = []
        self.players_information = []
        self.matches_information = []
        self.matches_dict = {}
        self.queries = []
        self.answers = []

    def insert_query(self, query: str):
        self.queries.append(query)

    def insert_answer(self, answer: str):
        self.answers.append(answer)

    def load_team_data(self):
        with open('../../crawling/team.csv', newline="") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                country_name = row[0]
                fifa_code = row[4]
                self.code_dict[country_name] = fifa_code
                self.teams_information.append(row)

    def load_player_data(self):
        with open('../../crawling/player.csv', newline="") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.players_information.append(row)

    def load_match_data(self):
        with open('../../crawling/match.csv', newline="") as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.matches_information.append(row)

    def make_query_answer(self):
        for information in self.teams_information:
            self.query_answer_from_team_information(information)

        for information in self.matches_information:
            self.query_answer_from_matches_information(information)

        for information in self.players_information:
            self.query_answer_from_players_information(information)

    def query_answer_from_matches_information(self, information: list):
        home = information[0]
        order = information[1]
        date = information[2]
        away = information[3]

        self.insert_when_form_query_answer(home, date, self.match_dict[order])
        self.insert_when_form_query_answer(home, date, "group stage " + self.match_dict[order])
        if home in self.code_dict.keys():
            self.insert_when_form_query_answer(self.code_dict[home], date, self.match_dict[order])
        self.insert_when_form_query_answer(home, date, "match with " + away)
        self.insert_when_form_query_answer(home, date, away + 'match?')

        if home not in self.matches_dict.keys():
            self.matches_dict[home] = []
        self.matches_dict[home].append([date, away])

    def query_answer_from_players_information(self, information: list):
        team = information[0]
        name = information[1]
        position = information[2]
        club = information[3]

        self.insert_preference(name, position)
        self.insert_club(name, club)
        self.insert_national(name, team)

        if team in self.match_dict.keys():
            his_matches = self.match_dict[team]
            for i, match in enumerate(his_matches):
                self.insert_when_form_query_answer(name, match[0], self.match_dict[str(i+1)])
                self.insert_when_form_query_answer(name, match[0], "group stage " + self.match_dict[str(i+1)])
                self.insert_when_form_query_answer(name, match[0], "match with " + match[1])
                self.insert_when_form_query_answer(name, match[0], match[1] + 'match?')

    def insert_what_player_query_answer(self, player: str, answer: str, template: str):
        self.insert_query(self.what_start + " " + player + " " + template)
        self.insert_answer(answer)

    def query_answer_from_team_information(self, information: list):
        country_name = information[0]
        confederation = information[1]
        head_coach = information[2]
        captain = information[3]
        ranking = information[5]
        appearances = information[6]
        best_record = information[7]

        self.insert_fifa_ranking(country_name, ranking)
        self.insert_confederation(country_name, confederation)
        self.insert_head_coach(country_name, head_coach)
        self.insert_captain(country_name, captain)
        self.insert_appearances(country_name, appearances)
        self.insert_best_record(country_name, best_record)

    def insert_when_form_query_answer(self, name: str, answer: str, query_template: str):
        self.insert_query(self.when_start + " "+ name + " " + query_template)
        self.insert_answer(answer)

    def insert_what_form_query_answer(self, country_name: str, answer: str, query_template:str):
        self.insert_query(self.what_start + country_name + " " + query_template)
        self.insert_answer(answer)
        self.insert_query(self.what_start + self.code_dict[country_name] + " " + query_template)
        self.insert_answer(answer)

    def insert_who_in_form_query_answer(self, country_name:str, answer:str, query_template:str):
        self.insert_query(self.who_start + query_template + " in " + country_name)
        self.insert_answer(answer)
        self.insert_query(self.who_start + query_template + " of " + country_name)
        self.insert_answer(answer)
        self.insert_query(self.who_start + country_name + " " + query_template)
        self.insert_answer(answer)

    def insert_preference(self, player: str, position: str):
        self.insert_what_player_query_answer(player, position, "position?")
        self.insert_what_player_query_answer(player, position, "Pos?")
        self.insert_what_player_query_answer(player, position, "preference?")

    def insert_club(self, player: str, club: str):
        self.insert_what_player_query_answer(player, club, "club?")
        self.insert_what_player_query_answer(player, club, "club name?")

    def insert_national(self, player: str, national: str):
        self.insert_what_player_query_answer(player, national, "national?")
        self.insert_what_player_query_answer(player, national, "belong to?")

    def insert_fifa_ranking(self, country_name: str, ranking: str):
        self.insert_what_form_query_answer(country_name, ranking, "'s FIFA ranking?")
        self.insert_what_form_query_answer(country_name, ranking, "'s ranking?")
        self.insert_what_form_query_answer(country_name, ranking, "ranking?")

    def insert_confederation(self, country_name:str, confederation:str):
        self.insert_what_form_query_answer(country_name, confederation, "'s confederation?")
        self.insert_what_form_query_answer(country_name, confederation, "confederation?")
        self.insert_what_form_query_answer(country_name, confederation, "association?")
        self.insert_what_form_query_answer(country_name, confederation, "continent?")

    def insert_head_coach(self, country_name:str, head_coach:str):
        self.insert_who_in_form_query_answer(country_name, head_coach, "head coach")
        self.insert_who_in_form_query_answer(country_name, head_coach, "coach")
        self.insert_who_in_form_query_answer(country_name, head_coach, "head")

    def insert_captain(self, country_name:str, captain:str):
        self.insert_who_in_form_query_answer(country_name, captain, "captain")

    def insert_appearances(self, country_name:str, appearances:str):
        self.insert_what_form_query_answer(country_name, appearances, "'s appearances?")
        self.insert_what_form_query_answer(country_name, appearances, "'s world cup appearances?")
        self.insert_what_form_query_answer(country_name, appearances, "'s number of participant in World Cup?")
        self.insert_what_form_query_answer(country_name, appearances, "'s World Cup participant count?")

    def insert_best_record(self, country_name:str, best_record:str):
        self.insert_what_form_query_answer(country_name, best_record, "'s best record?")
        self.insert_what_form_query_answer(country_name, best_record, "'s best record in world cup?")
        self.insert_what_form_query_answer(country_name, best_record, "best rank in world cup?")
        self.insert_what_form_query_answer(country_name, best_record, "best rank?")

if __name__ == "__main__":
    query = Query()
    query.load_team_data()
    query.load_player_data()
    query.load_match_data()
    query.make_query_answer()

    print(len(query.queries))
    print(len(query.answers))