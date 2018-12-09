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

    # polarity means emotions expressed in a sentence
    # how to calculate polarity? famous method is using bag of words.
    words = descripton.split()

    if descripton == None:
        sys.exit("Error")
    for word in words:
        word = word.lower()

        if word in afinn:
            if(int(afinn[word]) > 0):
                positive.append(word)
            elif(int(afinn[word]) < 0):
                negative.append(word)

            score += int(afinn[word])

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