from transformers import RealmRetriever, RealmTokenizer, RealmForOpenQA

retriever = RealmRetriever.from_pretrained("google/realm-orqa-nq-openqa")
tokenizer = RealmTokenizer.from_pretrained("google/realm-orqa-nq-openqa")
model = RealmForOpenQA.from_pretrained("google/realm-orqa-nq-openqa", retriever=retriever)

question = "Who is the pioneer in modern computer science?"
question_ids = tokenizer([question], return_tensors="pt")
answer_ids = tokenizer(
    ["alan mathison turing"],
    add_special_tokens=False,
    return_token_type_ids=False,
    return_attention_mask=False,
).input_ids

reader_output, predicted_answer_ids = model(**question_ids, answer_ids=answer_ids, return_dict=False)
predicted_answer = tokenizer.decode(predicted_answer_ids)
loss = reader_output.loss