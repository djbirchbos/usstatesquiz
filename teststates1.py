# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 16:03:18 2020

@author: David

Last time I ran this I used anaconda prompt:
    
    set flask_app = test.py
    flask run
    
    Then use browser to hit http://127.0.0.1:5000/form

version works again

"""

import random 
import time 
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

states = []
answers = []

class state():
    __state_name = ''
    __capital = ''
    __latitue = 0.0
    __longitude = 0.0
    
    def __init__(self, state_name, capital, latitude, longitude):
        self.__state_name = state_name
        self.__capital = capital
        self.__latitude = latitude
        self.__longitude = longitude
        
    def __repr__(self):
        return self.__state_name + ' - ' + self.__capital + ' (' + str(self.__latitude) + ' ,' + str(self.__longitude) + ')' + '\n'
        
    def get_state_name(self):
        return self.__state_name
    
    def get_state_name_no_spaces(self):
        return self.__state_name.replace(" ","")
    
    def get_capital(self):
        return self.__capital
    
    def get_latitude(self):
        return self.__latitude
    
    def get_longitude(self):
        return self.__longitude
    
class answer():
    __question = ''
    __correct_answer = ''
    __answer = ''
    __correct = False
    
    def __init__(self, question, correct_answer, answer_entry, correct):
        self.__question = question
        self.__correct_answer = correct_answer
        self.__answer = answer_entry 
        self.__correct = correct
        
    def __repr__(self):
        outputtext = '' 
        
        if self.__correct == True:
            outputtext = 'Correct'
        else:
            outputtext = 'Incorrect'
        return outputtext 
    
    def get_correct(self):
        return self.__correct 
    
    def get_question(self):
        return self.__question
    
    def get_answer(self):
        return self.__answer


@app.route("/form",methods=['GET','POST'])
def main():
    # init variables and lists
    answers = []
    correct = False 
    score = 0
    
    # pd.read_csv returns a numpy.ndarray
    states_and_capitals = pd.read_csv('C:/Users/David/Documents/David Birch/Code Projects/Quiz/states.csv')
        
    # Build a list of facts about states
    for i in range(1, len(states_and_capitals.index)):
        state_name = states_and_capitals['name'][i]
        capital = states_and_capitals['description'][i]
        latitude = states_and_capitals['latitude'][i]
        longitude = states_and_capitals['longitude'][i]
        
        states.append(state(state_name, capital, latitude, longitude))
    
    # shuffle the list so its random each time
    random.shuffle(states)
    
    return render_template('quiz.html', \
                           num_questions = len(states),\
                           questions = states )
    


@app.route('/post_results',methods=['GET','POST'])
def check_results():    
    score = 0
    correct = False
    
    # First lets test the state capitals..
    for us_state in states:
        
        # check answer
        if str(request.form[us_state.get_state_name_no_spaces()]).upper() == us_state.get_capital().upper():
            score = score + 1
            correct = True 
    
        # Add this answer to list of answers
        answers.append(answer(
            us_state.get_state_name(), 
            us_state.get_capital(), 
            request.form[us_state.get_state_name_no_spaces()], 
            correct))
     
    
    # Iterate through the results
    for result in answers:
        if result.get_correct() == False:
            print('The state capital of ' + result.get_question() + ' is not ' + result.get_answer())
        
    return render_template('results.html', \
                           player_name = request.form['playername'], \
                           num_correct = score,
                           time_taken = 10)

    
if __name__ == "__main__":
    main()




        
    
    
    

