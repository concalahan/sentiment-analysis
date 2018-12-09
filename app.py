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
    # working
    if(len(wordArray) == 0):
        print("return cmnr")
        return None

    word = ' '.join(wordArray)

    print("hihihi " + str(word))

    if word in afinn:
        print("hohohoho " + str(word))
        return word
    else:
        get_afinn_word_in_five_words(wordArray[:-1], afinn)

        print("AAAAAAAAAAAAAAAAAAA")

        get_afinn_word_in_five_words(wordArray[1:], afinn)

        print("BBBBBBBBBBBBBBBBBBB")

    # found = False

    # # execute until found
    # while(not found):
    #     word = ' '.join(wordArray)

    #     # check current
    #     if word in afinn:
    #         return word

    #     word = ' '.join(wordArray[:-1])

    #     # check exclude last index (rightest)
    #     if word in afinn:
    #         return word

    #     word = ' '.join(wordArray[1:])

    #     # check exclude first index (leftest)
    #     if word in afinn:
    #         return word


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

    print(afinn["vô tình"])

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

            print("afinn_word " + str(afinn_word))

            if afinn_word is not None:
                if(int(afinn[afinn_word]) > 0):
                    positive.append(afinn_word)
                elif(int(afinn[afinn_word]) < 0):
                    negative.append(afinn_word)

                score += int(afinn[afinn_word])

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