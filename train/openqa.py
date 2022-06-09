from transformers import RealmForOpenQA
from retriever import Retriever


model = RealmForOpenQA.from_pretrained("google/realm-orqa-nq-openqa", retriever=Retriever)

