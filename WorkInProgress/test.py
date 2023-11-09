import json

with open("../ques.json", "r") as file:
    questions = json.load(file)
    idx = list(questions.keys())[0]
    question = questions[idx]["q"]
    link = questions[idx]["l"]
    questions.pop(idx)
    print(question)