import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
# from tensorflow.keras.optimizers import SGD

# --------------------------------------------------------- EXTRACT AND SAVE WORDS FOROM .JSON FILE ---------------------------------------------------------
parentDictionary = json.loads(open('intents.json').read())

tagWords=[]
patternsWords=[]

# EXTRACT WORDS
for event in parentDictionary["intents"]:
    print(event)
    tagWords.append(event["tag"])
    patternsWords.extend(event["patterns"])

print("")
print("tagWords",tagWords)
print("")
print("patternsWords",patternsWords)

#SAVE WORDS IN THE PICKLE FILE
with open("tagWords.pkl", 'wb') as file:
    pickle.dump(tagWords, file)

with open("patternsWords.pkl", 'wb') as file:
    pickle.dump(patternsWords, file)

with open("tagWords.pkl", 'rb') as file:
    tagWords = pickle.load(file)

with open("patternsWords.pkl", 'rb') as file:
    patternsWords = pickle.load(file)

print("")
print("tagWords",tagWords)
print("")
print("patternsWords",patternsWords)


# --------------------------------------------------------- TOKENIZE WORDS ---------------------------------------------------------
from sklearn.feature_extraction.text import CountVectorizer

# TAG DATASET PREPROCESSING
tagVectorizer = CountVectorizer(vocabulary=tagWords)
tagSparseMatrix=tagVectorizer.fit(tagWords) # Get entire dataset in shape of sparse matrix NOTE: Used only for the data analyze

# print("\n", "tagVectorizer",tagVectorizer)
# print("\n", "tagSparseMatrix",tagSparseMatrix)
# print("\n", "tagVectorsMatrix", tagVectorsMatrix)

# GET ALL TOKENS TOGETHER WITH ALL TOKENS VALUES
token_vocabulary=list(tagVectorizer.vocabulary_.values())
token_values = list(tagVectorizer.vocabulary_.keys())
# print("\n", "token_vocabulary",token_vocabulary)
# print("\n", "token_values",token_values)

# PRINTS KEY AND VALUES TOGETHER
for tagWord, tagToken in zip(token_vocabulary,token_values):
    print(tagWord,"-",tagToken)

new_sentence = "age name"
new_vector = tagVectorizer.transform([new_sentence]).toarray()
print("new_vector",new_vector)

# CREATE NEW VECTORIZER BASED ON PREVIOUSLY USED BAG OF WORDS
newExampleVectorizer = CountVectorizer(vocabulary=tagWords)
newExampleSparseMatrix=newExampleVectorizer.fit(tagWords) # Get entire dataset in shape of sparse matrix NOTE: Used only for the data analyze

# print("\n", "newExampleVectorizer",newExampleVectorizer)
# print("\n", "newExampleSparseMatrix",newExampleSparseMatrix)
# print("\n", "newExampleVectorsMatrix", newExampleVectorsMatrix)

# GET ALL TOKENS TOGETHER WITH ALL TOKENS VALUES
token_vocabulary=list(newExampleVectorizer.vocabulary_.values())
token_values = list(newExampleVectorizer.vocabulary_.keys())
# print("\n", "token_vocabulary",token_vocabulary)
# print("\n", "token_values",token_values)

# PRINTS KEY AND VALUES TOGETHER
for newExampleWord, newExampleToken in zip(token_vocabulary,token_values):
    print(newExampleWord,"-",newExampleToken)

new_sentence = "age name"
new_vector = newExampleVectorizer.transform([new_sentence]).toarray()
print("new_vector",new_vector)

# CREATE NEW VECTOR TAG BASED ON THE OLD BAG OF WORDS
# # CREATE train_y DATASET
# train_y=[]
#
# for event in parentDictionary["intents"]:
#     if event["tag"] in tagWords:
#         # print("event['tag']",event["tag"])
#         indexForTokenSearch= token_values.index(event["tag"])
#         # print("indexForTokenSearch",indexForTokenSearch)
#         wantedIndex=token_vocabulary[ indexForTokenSearch]
#         # print("wantedIndex",wantedIndex)
#         # Find the row indices where column "wantedIndex" 2 has a non-zero element at index "wantedIndex" 2
#         row_indices = np.where(tagVectorsMatrix[:, wantedIndex] != 0)[0]
#         # Retrieve the rows meeting the condition
#         resulting_rows = tagVectorsMatrix[row_indices]
#         # print("resulting_rows",resulting_rows)
#         train_y.append(resulting_rows)
#
# # PATTERN DATASET PREPROCESSING
# patternsVectorizer = CountVectorizer()
# patternsSparseMatrix=patternsVectorizer.fit_transform(patternsWords) # Get entire dataset in shape of sparse matrix NOTE: Used only for the data analyze
# patternsVectorsMatrix=patternsVectorizer.fit_transform(patternsWords).toarray() # Get entire dataset in shape of array
# print("\n", "patternsVectorizer",patternsVectorizer)
# print("\n", "patternsSparseMatrix",patternsSparseMatrix)
# print("\n", "patternsVectorsMatrix", patternsVectorsMatrix)
#
# # GET ALL TOKENS TOGETHER WITH ALL TOKENS VALUES
# token_vocabulary=list(patternsVectorizer.vocabulary_.values())
# token_values = list(patternsVectorizer.vocabulary_.keys())
# print("\n", "token_vocabulary",token_vocabulary)
# print("\n", "token_values",token_values)
#
# # PRINTS KEY AND VALUES TOGETHER
# for patternsWord, patternsToken in zip(token_vocabulary,token_values):
#     print(patternsWord,"-",patternsToken)
#
# # CREATE train_x DATASET
#
#
# for event in parentDictionary["intents"]:
#     if event["patterns"] in patternsWords:
#         # print("event['patterns']",event["patterns"])
#         indexForTokenSearch= token_values.index(event["patterns"])
#         # print("indexForTokenSearch",indexForTokenSearch)
#         wantedIndex=token_vocabulary[ indexForTokenSearch]
#         # print("wantedIndex",wantedIndex)
#         # Find the row indices where column "wantedIndex" 2 has a non-zero element at index "wantedIndex" 2
#         row_indices = np.where(patternsVectorsMatrix[:, wantedIndex] != 0)[0]
#         # Retrieve the rows meeting the condition
#         resulting_rows = patternsVectorsMatrix[row_indices]
#         print("resulting_rows",resulting_rows)
#


# train_x=np.array(train_x)
# train_y=np.array(train_y)
#
#
# sgd=tf.keras.optimizers.legacy.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
#
# model = Sequential()
# model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(len (train_y[0]), activation='softmax'))
# model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#
# hist=model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
# model.save('chatbot_model.h5',hist)
#
# print("Done")