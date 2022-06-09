from transformers import RealmRetriever, RealmConfig, RealmTokenizer
import numpy as np


tokenizer = RealmTokenizer.from_pretrained("google/realm-orqa-nq-openqa")

configuration = RealmConfig()

block_records = np.array(['need block records'])

model = RealmRetriever(block_records, tokenizer)

class Retriever:
    pass



