#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import abort, redirect, url_for

from analyzer import Analyzer
import sys
import os
from nltk.tokenize import TweetTokenizer

from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/analyze-text', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get the data
        desription = request.get_json().get("description")
        
        # perform sentiment analysis
        comparative = check(desription)

        return "hllo"
    else:
        abort(400)
        return 'ONLY ACCPET POST REQUEST'    

def is_digit(n):
    try:
        int(n)
        return True
    except ValueError:
        return  False

def check(descripton):
    afinn = {}

    # overall score
    score = 0

    # overall score/ length of total string
    comparative = 0

    # load afinn dictionary
    with open("AFINN-111-new.txt") as f:
        lines = f.readlines()

        for line in lines:
            new_line = line.replace("\n", "")
            split_line = new_line.split('\t')

            afinn[split_line[0]] = split_line[1]

    print(afinn["rút tiền"])

    # polarity means emotions expressed in a sentence
    # how to calculate polarity? famous method is using bag of words.
    words = descripton.split()

    if descripton == None:
        sys.exit("Error")
    for word in words:
        word = word.lower()

        if word in afinn:
            print("AAA:" + str(afinn[word]))

            score += int(afinn[word])
            print("Has word: " + word)

    comparative = score / len(words)

    print("The score is: " + str(score))
    print("The comparative is: " + str(comparative))

    return comparative