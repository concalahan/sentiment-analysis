#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import abort, redirect, url_for
from flask import jsonify

from analyzer import Analyzer
import sys
import os
import json
from nltk.tokenize import TweetTokenizer

from textblob import TextBlob

app = Flask(__name__)

# global variable
max_word_tokenize = 5

@app.route('/')
def index():
    return 'Index Page'

@app.route('/analyze-text', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the data
        desription = request.get_json().get("description")
        
        # perform sentiment analysis
        obj = check(desription)

        return jsonify(obj)
    else:
        abort(400)
        return 'ONLY ACCPET POST REQUEST'    

def is_digit(n):
    try:
        int(n)
        return True
    except ValueError:
        return  False

def get_afinn_word_in_five_words(wordArray, afinn):
    return_words = []
    
    if(len(wordArray) == 0):
        return None

    # 5 words check
    word = ' '.join(wordArray)
    if word in afinn:
        return_words.append(word)

    # 4 words check
    word = ' '.join(wordArray[:-1]) 
    if word in afinn:
        return_words.append(word)

    word = ' '.join(wordArray[1:]) 
    if word in afinn:
        return_words.append(word)

    # 3 words check 01 34 04
    # keep 1 2 3
    word = ' '.join(wordArray[1:4])
    if word in afinn:
        return_words.append(word)

    # keep 0 1 2
    word = ' '.join(wordArray[2:5])
    if word in afinn:
        return_words.append(word)

    # keep 2 3 4
    word = ' '.join(wordArray[0:3])
    if word in afinn:
        return_words.append(word)    

    # 2 words check
    # keep 0 1
    word = ' '.join(wordArray[0:2])
    if word in afinn:
        return_words.append(word)

    # keep 1 2
    word = ' '.join(wordArray[1:3])
    if word in afinn:
        return_words.append(word)

    # keep 2 3
    word = ' '.join(wordArray[2:4])
    if word in afinn:
        return_words.append(word)

    # keep 3 4
    word = ' '.join(wordArray[3:5])
    if word in afinn:
        return_words.append(word)

    for word in wordArray:
        if word in afinn:
            return_words.append(word)

    print(return_words)

    return return_words

def check(descripton):
    # positive/ negative
    verdict = ""
    positive = []
    negative = []

    # overall score
    score = 0

    # overall score/ length of total string
    comparative = 0

    # afinn dictionary
    afinn = {}

    # load afinn dictionary
    with open("AFINN-111-new.txt") as f:
        lines = f.readlines()

        for line in lines:
            new_line = line.replace("\n", "")
            split_line = new_line.split('\t')

            afinn[split_line[0]] = split_line[1]

    #print(afinn["vô tình"])

    # polarity means emotions expressed in a sentence
    # how to calculate polarity? famous method is using bag of words.
    words = descripton.split()

    if descripton == None:
        sys.exit("Error")

    temp_count = 0
    temp_word_array = []
    for word in words:
        word = word.lower()
        temp_word_array.append(word)
        temp_count += 1

        # start perform sentiment analysis every 5 words
        if(temp_count == max_word_tokenize):
            print("Checking... " + str(temp_word_array))
            
            afinn_word = get_afinn_word_in_five_words(temp_word_array, afinn)

            if afinn_word is not None:
                for word in afinn_word:
                    print("hohoho " + word)

                    if(int(afinn[word]) > 0):
                        positive.append(word)
                    elif(int(afinn[word]) < 0):
                        negative.append(word)

                    score += int(afinn[word])

            # set value again
            temp_count = 0
            temp_word_array = []

    comparative = score / len(words)

    if(comparative > 0):
        verdict = "POSITIVE"
    elif(comparative < 0):
        verdict = "NEGATIVE"
    else:
        verdict = "NEUTRAL"

    returnObj = {
        "verdict": verdict,
        "score": score,
        "comparative": comparative,
        "positive": positive,
        "negative": negative
    }

    return returnObj