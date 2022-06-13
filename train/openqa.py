from transformers import RealmRetriever, RealmTokenizer, RealmForOpenQA, AdamW
from data.making_data import Query

import tqdm
import torch

version_name = "1"
epoch_num = 5
lr = 1e-6
batch_size = 8
num_workers = 5

cuda_condition = torch.cuda.is_available()
device = torch.device("cuda:0" if cuda_condition else "cpu")

retriever = RealmRetriever.from_pretrained("google/realm-orqa-nq-openqa").to(device)
tokenizer = RealmTokenizer.from_pretrained("google/realm-orqa-nq-openqa")
model = RealmForOpenQA.from_pretrained("google/realm-orqa-nq-openqa", retriever=retriever).to(device)

query = Query()
query.load_team_data('../crawling/team.csv')
query.load_player_data('../crawling/player.csv')
query.load_match_data('../crawling/match.csv')
query.make_query_answer()

# set optimizer
param_optim = list(model.named_parameters())
no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']

optimizer_grouped_parameters = [{
            'params': [
                p for n, p in param_optim
                if not any(nd in n for nd in no_decay)
            ],
            'weight_decay':
            0.01
        }, {
            'params':
            [p for n, p in param_optim if any(nd in n for nd in no_decay)],
            'weight_decay':
            0.0
        }]

optim = AdamW(model.parameters(), lr=lr)
torch.cuda.empty_cache()

for epoch in range(epoch_num):
    train_iter = tqdm.tqdm(enumerate(query.queries),
                           desc=str(epoch),
                           total=len(query.queries))
    for i, question in train_iter:
        model.train()
        optim.zero_grad()

        question_ids = tokenizer([question], return_tensors='pt')
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

model.save_pretrained('output/'+version_name)
