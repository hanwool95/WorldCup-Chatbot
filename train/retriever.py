from transformers import RealmRetriever, RealmTokenizer
import numpy as np
import urllib
from bs4 import BeautifulSoup
import csv
import pickle


class WorldCup_Retriever:
    def __init__(self):
        self.texts = []
        self.block_records = None

    def making_blocks_from_csv(self, path: str):
        with open(path, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.append_texts_from_link(row[0])
        self.make_block_from_texts()

    def append_texts_from_link(self, link: str):
        try:
            with urllib.request.urlopen(link) as url:
                print("append url: ", link)
                doc = url.read()
                soup = BeautifulSoup(doc, "html.parser")
                Draw_content = soup.find('div', id='bodyContent').text
                self.texts.append(bytes(Draw_content, 'utf-8'))
        except:
            print("error url: ", link)

    def make_block_from_texts(self):
        print("transform start")
        self.block_records = np.array(self.texts)

if __name__ == "__main__":
    world_cup_retreiver = WorldCup_Retriever()
    world_cup_retreiver.making_blocks_from_csv("../crawling/2022_FIFA_World_Cup.csv")
    tokenizer = RealmTokenizer.from_pretrained("google/realm-orqa-nq-openqa")
    retriever = RealmRetriever(world_cup_retreiver.block_records, tokenizer)
    with open('retriever.p', 'wb') as file:
        pickle.dump(retriever, file)