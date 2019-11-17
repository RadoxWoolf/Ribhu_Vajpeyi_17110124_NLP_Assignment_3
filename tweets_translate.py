#!/usr/bin/env python

import pandas as pd
import re
########################################################################
from three_step_decoding import *
tsd = ThreeStepDecoding('lid_models/hinglish', htrans='nmt_models/rom2hin.pt', etrans='nmt_models/eng2eng.pt')
#########################################################################
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"My First Project-99790c176cbd.json"
# Imports the Google Cloud client library
import google.cloud.translate_v2 as translate
# Instantiates a client
translate_client = translate.Client()
##########################################################################
count=1
f = open("X_train.txt", "r")
X_train=[]
for line in f:
  line = line.strip()
  if len(line.split("\t"))>1:
    X_train.append(line.split("\t")[-1])
    if count == 4761:
      print(line.split("\t")[-1])
    count+=1

tweets = X_train
#########################################################################

count = 1
en_transliterated_tweets = []
for tweet in tweets:
  try:
    tweet_list = tweet.split()
    if len(tweet_list) > 1:
      csnli = [''.join(x[1]) for x in tsd.tag_sent(tweet)]
      en_transliterated_tweets.append(" ".join(csnli))
    else :
      en_transliterated_tweets.append(tweet)
  except:
    en_transliterated_tweets.append("!!!!csnli didn't work")
  print(count)
  count = count + 1
print("######################")
with open("X_train_csnli.txt", "w") as f:
  for i in range(len(en_transliterated_tweets)):
    f.write(tweets[i]+"\n")
    f.write(en_transliterated_tweets[i]+"\n")
    f.write("\n")

english = []
for i in range(len(en_transliterated_tweets)):
  translation = translate_client.translate(en_transliterated_tweets[i],target_language="en",source_language="hi",model='nmt')
  english.append(translation['translatedText'])
  print(i)

#hindi = []
#for i in range(len(en_transliterated_tweets)):
#  translation = translate_client.translate(en_transliterated_tweets[i],target_language="hi",source_language="en",model='nmt')
#  trans = translation['translatedText'].split()
#  tran =[]
#  for j in range(len(trans)):
#    if not trans[j].isalnum():
#       tran.append(trans[j])
#  hindi.append(" ".join(tran))
#  print(i)


with open("X_train_translated.txt", "w") as f:
  for i in range(len(en_transliterated_tweets)):
    f.write(tweets[i]+"\n")
    f.write(en_transliterated_tweets[i]+"\n")
    f.write(english[i]+"\n")
    #f.write(hindi[i]+"\n")
    f.write("\n")

