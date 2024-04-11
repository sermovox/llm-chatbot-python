from flask import Flask
# from https://reintech.io/blog/create-web-service-python
from flask import Flask, jsonify, request
from agent import generate_response

# Import necessary libraries
from flask import  render_template,  redirect
import os
import time

import uuid


template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'llm-chatbot-neo4j')
template_dir = os.path.join(template_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/hello')
def hello_world():
    return template_dir

tasks = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruits',
        'completed': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Learn Python',
        'description': 'Learn how to create a web service with Python',
        'completed': True
    }
]

# @app.route('/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = {
        'id': uuid.uuid4().hex,
        'title': request.json['title'],
        'description': request.json['description'],
        'completed': request.json.get('completed', False)
    }
    tasks.append(new_task)
    return jsonify({'task': new_task})

@app.route('/bot', methods=['POST'])
def respond_bot():
    new_resp=generate_response(request.json['user'])

    return jsonify({'answer': new_resp})


# from vv https://github.com/batuhantoker/Flask-OpenAI-Chatbot/blob/main/app.py :

# Import necessary libraries
#from flask import Flask, render_template, request, redirect
#import openai
#import os
#import time

# Set the OpenAI API key
#openai.api_key = "OPENAI_API"

# Define the name of the bot
name = 'BOT'

# Define the role of the bot
role = 'customer service'

# Define the impersonated role with instructions
impersonated_role = f"""
    From now on, you are going to act as {name}. Your role is {role}.
    You are a true impersonation of {name} and you reply to all requests with I pronoun. You never give unknown information.
    Forward them to the website for more information.
    YOU ARE NOT AN AI MODEL!
"""

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initialize chat history
chat_history = ''

# Create a Flask web application
#app = Flask(__name__)

# Function to complete chat input using OpenAI's GPT-3.5 Turbo
def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):

    chatgpt_output=generate_response(user_input)
    return chatgpt_output

# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chatgpt_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
    chatgpt_output = f'{name}: {chatgpt_raw_output}'
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output

# Function to get a response from the chatbot
def get_response(userText):
    return chat(userText)

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
#if __name__ == "__main__":
#    app.run()

# end vv



if __name__ == '__main__':
    app.run(debug=True)
