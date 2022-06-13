from transformers import RealmForOpenQA
from retriever import Retriever
from data.making_data import Query


model = RealmForOpenQA.from_pretrained("google/realm-orqa-nq-openqa", retriever=Retriever)

query = Query()
query.load_team_data()
query.load_player_data()
query.load_match_data()
query.make_query_answer()



