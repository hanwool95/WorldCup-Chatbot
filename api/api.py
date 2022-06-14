from typing import Union
from pydantic import BaseModel
from transformers import RealmRetriever, RealmTokenizer, RealmForOpenQA
from fastapi import FastAPI

retriever = RealmRetriever.from_pretrained("google/realm-orqa-nq-openqa")
tokenizer = RealmTokenizer.from_pretrained("google/realm-orqa-nq-openqa")
#model = RealmForOpenQA.from_pretrained("google/realm-orqa-nq-openqa", retriever=retriever)
model = RealmForOpenQA.from_pretrained("../train/output/1", retriever=retriever)

app = FastAPI()


class User(BaseModel):
    query: str


@app.get("/")
def read_bot():
    return {"Hello": "World"}


@app.post("/")
def post_bot(user: User):
    question = user.query
    print(question)
    try:
        question_ids = tokenizer([question], return_tensors="pt")

        reader_output, predicted_answer_ids = model(**question_ids, return_dict=False)
        predicted_answer = tokenizer.decode(predicted_answer_ids)
        result_dict = {"result": predicted_answer}
    except:
        result_dict = {"result": "Sorry, we couldn't find the answer you were looking for."}
    # result_dict = {"result": question}
    return result_dict



