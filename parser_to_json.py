import re
import json

# open the file
with open('linux-acedemy-final1.html', 'r', encoding='utf8') as raw_data:
    data = raw_data.readlines()

"""
%%%%%%%% structure %%%%%%%%
in linux academy test the id of the question is with the question itself.
Correct Answers is according the alphabetical order  


#############################################################
change #end_statement to the correct indicator that the last item of the list joined
change #isAnswer to the correct indicator that this is an answer item
"""

# regex patterns
number_pat = "results-question-number-.*?\">(.*?)\."
context_pat = "<p>(.*)"
correct_pat = "Correct Answer:\s(.*?)\s"
answer_pat = "<p>(.*?)<\/p>"

# indicators
end_statement = "</head>"
isAnswer = "results-question-choice-text"
pattern_to_remove = '</p>'

# reseting the list
qustions_list = []
question = {}
last_index = 0

# translate from a letter of the correct to a list of indexes
def translator(letter):
    switcher = {
        "A": [1],
        "B": [2],
        "C": [3],
        "D": [4],
        "E": [5],
        "F": [6],
        "AB": [1, 2],
        "AC": [1, 3],
        "AD": [1, 4],
        "AE": [1, 5],
        "AF": [1, 6],
        "BC": [2, 3],
        "BD": [2, 4],
        "BE": [2, 5],
        "BF": [2, 6],
        "CD": [3, 4],
        "CE": [3, 5],
        "CF": [3, 6],
        "DE": [4, 5],
        "DF": [4, 6],
        "EF": [5, 6],
        "ABC": [1, 2, 3],
        "ABD": [1, 2, 4],
        "ABE": [1, 2, 5],
        "ABF": [1, 2, 6],
        "ACD": [1, 3, 4],
        "ACE": [1, 3, 5],
        "ACF": [1, 3, 6],
        "ADE": [1, 4, 5],
        "ADF": [1, 4, 6],
        "AEF": [1, 5, 6],
    }
    return switcher.get(letter)


# returns the correct answer form the answers list and the correct letter index
def get_correct_answer(correct_letter, answers):
    corrects_indexes = translator(correct_letter)
    correct_answers = []
    for index in corrects_indexes:
        correct_answers.append(answers[index - 1])
    return correct_answers


# removes pattern that could not be removed with regex
def remove_unused_parts_of_question(part, q):
    if part in q:
        return ''.join(q.split(part))
    return q


# go over the file and parse the question
for i in data:

    # if this there is a new number of question
    if re.search(number_pat, i):
        number_question = re.findall(number_pat, i, 0)[0]
        number_question = int(number_question)
        # if this is a new question - according to the id
        if number_question > last_index:
            # add the current question and reset the var
            qustions_list.append(question)
            question = {}
            question["answers"] = []
            last_index += 1
        question["Question"] = remove_unused_parts_of_question(pattern_to_remove, re.findall(context_pat, i, 0)[0])
        question["id"] = number_question - 1

    if isAnswer in i:
        question["answers"].append(re.findall(answer_pat, i, 0)[0])

    if re.search(correct_pat, i):
        question["Correct"] = get_correct_answer(re.findall(correct_pat, i, 0)[0], question["answers"])

    if end_statement in i:
        qustions_list.append(question)
        question = {}

# outputs the data
with open('res2.json', 'w') as output:
    json.dump(qustions_list, output, indent=4)