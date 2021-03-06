from transformers import RealmTokenizer, RealmForOpenQA, RealmConfig, AdamW, RealmRetriever
from data.making_data import Query
import numpy as np

import tqdm
import torch
import pickle

version_name = "3"
epoch_num = 5
lr = 1e-6
batch_size = 8
num_workers = 5

cuda_condition = torch.cuda.is_available()
device = torch.device("cuda" if cuda_condition else "cpu")

with open('retriever.p', 'rb') as file:    # james.p 파일을 바이너리 읽기 모드(rb)로 열기
    Docs_Retriever = pickle.load(file)

# config = RealmConfig()
# config.num_block_records = len(Docs_Retriever.block_records)
# config.searcher_beam_size = 2
# model = RealmForOpenQA(config, retriever=Docs_Retriever).to(device)

retriever = RealmRetriever.from_pretrained("google/realm-orqa-nq-openqa")
retriever.block_records = np.append(retriever.block_records, Docs_Retriever.block_records)

tokenizer = RealmTokenizer.from_pretrained("google/realm-orqa-nq-openqa")
# model = RealmForOpenQA.from_pretrained("google/realm-orqa-nq-openqa", retriever=retriever).to(device)
model = RealmForOpenQA.from_pretrained("output/1", retriever=retriever).to(device)

query = Query()
query.load_team_data('../crawling/team.csv')
query.load_player_data('../crawling/player.csv')
query.load_match_data('../crawling/match.csv')
query.make_query_answer()

optim = AdamW(model.parameters(), lr=lr)

import gc
gc.collect()
torch.cuda.empty_cache()

for epoch in range(epoch_num):
    train_iter = tqdm.tqdm(enumerate(query.queries),
                           desc=str(epoch),
                           total=len(query.queries))
    for i, question in train_iter:
        optim.zero_grad()

        question_ids = tokenizer([question], return_tensors='pt').to(device)
        answer_ids = tokenizer(
            [query.answers[i]],
            add_special_tokens=False,
            return_token_type_ids=False,
            return_attention_mask=False,
        ).input_ids

        reader_output, predicted_answer_ids = model(**question_ids, answer_ids=answer_ids, return_dict=False)
        predicted_answer_ids = tokenizer.decode(predicted_answer_ids)
        loss = reader_output.loss

        loss.backward()
        optim.step()
        model.train()

model.save_pretrained('output/'+version_name)
