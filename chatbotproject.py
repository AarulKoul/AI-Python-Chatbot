from flask import Flask
import re
import time
from flask_pymongo import PyMongo
from flask import request
from datetime import datetime
from flask_cors import CORS, cross_origin
import spacy

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/chatbot'
mongo = PyMongo(app)

nlp = spacy.load('en_core_web_sm')

user_data = {}  # Dictionary to store user-specific data

questions = [nlp("Give me information about FirstName LastName"), 
             nlp("Give me information about PRN"), 
             nlp("Give me cgpa of FirstName LastName"),
             nlp("Give me cgpa of PRN")]

def process_user_input(user_message):
    time.sleep(0.5)
    global user_data
    # print(user_data)

    if user_message.lower() == 'exit':
        user_data = {}
        return "Please enter a student's full name to get started."

    if not 'name' in user_data:

        user = mongo.db.student.find_one({'name': {'$regex': f'^{re.escape(user_message)}$', '$options': 'i'}})
        if not user:
            return 'User not found. Please enter a valid name.'
        user_data = user.copy()
        # user_data['name'] = user.get('name')
        # user_data['prn'] = user.get('prn')
        return f'What information would you like about {user_data["name"]} (PRN: {user_data["prn"]})?\nTo switch student, enter "exit"'
        # return f"Information about {user_data['name']} with PRN {user_data['prn']}: <Your logic here>"

    doc = nlp(user_message)

    if any(token.text.lower() in ["cgpa", "gpa", "marks"] for token in doc):
        if user_data["cgpa"] > 9:
            return f'CGPA of {user_data["name"]} (PRN: {user_data["prn"]}) is {user_data["cgpa"]} 🤯. So smart!!'
        else:
            return f'CGPA of {user_data["name"]} (PRN: {user_data["prn"]}) is {user_data["cgpa"]}'

    if any(token.text.lower() in ["bye", "thank", "thanks"] for token in doc):
        user_data = {}
        return "I'm always happy to help 😊. Enter a student's full name to get more info."

    if any(token.text.lower() in ["age", "old"] for token in doc):
        return f'Age of {user_data["name"]} is: {user_data["age"]}\n'

    if any(token.text.lower() in ["birthday", "born", "birth-day", "bday", "b-day", "dob", "birth"] for token in doc):
        return f'Birthday of {user_data["name"]} is: {user_data["birthday"]}\n'
    

    if any(token.text.lower() in ["branch", "major", "school"] for token in doc):
        return f'{user_data["name"]} is in Branch: {user_data["branch"]}\n'

    if any(token.text.lower() in ["panel", "division", "class"] for token in doc):
        return f'{user_data["name"]} is in Panel: {user_data["panel"]}\n'

    if any(token.text.lower() in ["roll"] for token in doc):
        return f'Roll No of {user_data["name"]} is: {user_data["roll_number"]}\n'

    if any(token.text.lower() in ["current", "year"] for token in doc):
        return f'{user_data["name"]} is in year: {user_data["current_year"]}\n'

    if any(token.text.lower() in ["sem", "semester"] for token in doc):
        return f'{user_data["name"]} is in Semester: {user_data["semester"]}\n'

    if any(token.text.lower() in ["passing", "graduating", "graduation", "graduate", "passout"] for token in doc):
        return f'{user_data["name"]} is graduating in year: {user_data["graduation_year"]}\n'
    
    if any(token.text.lower() in ["courses", "subjects"] for token in doc):
        subjects = '\n'.join(user_data["currently_enrolled_courses"])
        return f'{user_data["name"]} (PRN: {user_data["prn"]}) is currently enrolled in courses with the following codes: \n{subjects}'
    
    if any(token.text.lower() in ["details", "info"] for token in doc):
        return f'Student details of {user_data["name"]}: \nName: {user_data["name"]}\nPRN: {user_data["prn"]} \nAge: {user_data["age"]} \nBirthday: {user_data["birthday"]} \nBranch: {user_data["branch"]} \nPanel: {user_data["panel"]} \nRoll No: {user_data["roll_number"]} \nYear: {user_data["current_year"]} \nSemester: {user_data["semester"]} \nGraduation Year: {user_data["graduation_year"]}'
    
    if any(token.text.lower() in ["contact", "email", "phone", "mobile"] for token in doc):
        return f'Contact details of {user_data["name"]}: \nEmail: {user_data["email"]} \nPhone: {user_data["phone_number"]}'


    # Default response for unrecognized input
    return "I'm sorry, I didn't understand that 😓. Can you please provide more details or ask a different question?"

@app.route('/send_message', methods=['POST'])
@cross_origin()
def send_message():
    user_message = request.get_json().get('input')
    print(user_message)
    bot_response = process_user_input(user_message)
    return {'bot_response': bot_response}

@app.route('/reset', methods=['POST'])
@cross_origin()
def reset():
    global user_data
    user_data = {}
    return {'response': 'success'}


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
