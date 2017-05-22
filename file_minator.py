import csv
import config
import base64
import time
import datetime
import sys
import calendar


# Read section
def read_file(file_name):
    """Gives back a list from the csv file"""
    with open(file_name, "r") as rfile:
        reader = list(csv.reader(rfile))
        return reader


# Write section
def question_or_answer_to_delete(q_or_a, id_to_delete):
    """Overwrites the given data"""
    if q_or_a == "answer":
        old_data = read_file(file_name)
        remover(old_data, id_to_delete)
    elif q_or_a == "question":
        questions = read_file(config.questions)
        answers = read_file(config.answers)
        remover(answers, id_to_delete, questions)


def remover(loaded_answers, id_to_delete, loaded_question=None):
    if loaded_question is None:
        with open(config.answers, "w") as wfile:
            writer = csv.writer(wfile)
            for line in loaded_data:
                if int(id_to_delete) != loaded_data[0]:
                    writer.writerow(line)
    else:
        with open(config.answers, "w") as wfile:
            writer = csv.writer(wfile)
            for line in loaded_data:
                if int(id_to_delete) != loaded_data[3]:
                    writer.writerow(line)
        with open(config.questions, "w") as wfile:
            writer = csv.writer(wfile)
            for line in loaded_data:
                if int(id_to_delete) != loaded_data[0]:
                    writer.writerow(line)


def update_file(file_name, data, id_to_update):
    """Updates the file"""
    old_data = read_file(file_name)
    with open(file_name, "w") as wfile:
        writer = csv.writer(wfile)
        writer.writerow("\n")
        for line in old_data:
            if int(id_to_update) != int(line[0]):
                writer.writerow(line)
        writer.writerow(data)


# c = base64.b64encode(a.encode('ascii'))
#    print(c)
#    d = base64.b64decode(c).decode("utf-8", "ignore")
# Generators, preparators
def new_answer_handler(question_id, message, vote_number, image=None, title=None, view_number=None):
    """It does something"""
    converted_message = base64.b64encode(message.encode("ascii"))
    if image is not None:
        converted_image = base64.b64decode(image.encode("ascii"))
    else:
        image = "lol"
        converted_image = base64.b64encode(image.encode("ascii"))
    ready_list = preparator(question_id, converted_message, vote_number, converted_image)
    return ready_list
    #update_file(config.answers, ready_list, question_id)


def preparator(question_id, message, vote_number, image, title=None, view_number=None):
    """You are not prepared!...yet"""
    current_time = datetime.datetime.utcnow()
    new_time = calendar.timegm(current_time.utctimetuple())
    if title is None:
        new_id = int(max(all_the_answers()))+1
        converted_list = [new_id, new_time, vote_number, question_id, message, image]
    else:
        converted_list = [new_id, new_time, view_number, vote_number, title, message, image]
    return converted_list


# Section for the dictionary generators
def all_the_answers():
    answers = read_file(config.answers)
    dictionary = {}
    for i in range(len(answers)):
        dictionary.update({
            answers[i][0]: {
                "answer_submission_time": datetime.datetime.fromtimestamp(int(answers[i][1])),
                "answer_vote_number": answers[i][2],
                "answer_question_id": answers[i][3],
                "answer_message": base64.b64decode(answers[i][4]).decode("utf-8", "ignore"),
                "answer_image": base64.b64decode(answers[i][5]).decode("utf-8", "ignore")
            }})
    return dictionary


def all_the_questions():
    questions = read_file(config.questions)
    dictionary = {}
    for i in range(len(questions)):
        dictionary.update({
            questions[i][0]: {
                "question_id": questions[i][0],
                "question_submission_time": datetime.datetime.fromtimestamp(int(questions[i][1])),
                "question_view_number": questions[i][2],
                "question_vote_number": questions[i][3],
                "question_title": base64.b64decode(questions[i][4]).decode("utf-8", "ignore"),
                "question_message": base64.b64decode(questions[i][5]).decode("utf-8", "ignore"),
                "question_image": base64.b64decode(questions[i][6]).decode("utf-8", "ignore")
            }})
    return dictionary


def single_question(question_id):
    """Returns a dictionary abotut the required question"""
    questions = all_the_questions()
    question = questions[str(question_id)]
    return question


def single_answer(answer_id):
    """Returns a dictionary about the required answer"""
    answers = all_the_answers()
    answer = answers[answer_id]
    return answer


def answer_for_question(question_id):
    """Answers for the question"""
    question = single_question(question_id)
    answers = all_the_answers()
    answer_dict = {}
    for key, value in answers.items():
        if int(value["answer_question_id"]) == int(question_id):
            answer_dict.update({key: answers[key]})
    if answer_dict == {}:
        answer_dict.update({0: {
                "answer_submission_time": "There is no answer yet", "answer_vote_number": "There is no answer yet",
                "answer_question_id": "There is no answer yet",
                "answer_message":  "There is no answer yet",
                "answer_image":  "There is no answer yet"}})
    answered = {}
    answered.update({"question": question, "answers": answer_dict})
    return answered


###################



def main():
    new_answer_handler()

if __name__ == '__main__':
    main()