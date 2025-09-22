import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
# from tensorflow.keras.optimizers import SGD

# --------------------------------------------------------- EXTRACT AND SAVE WORDS FOROM .JSON FILE ---------------------------------------------------------
parentDictionary = json.loads(open('intents.json').read())

tagWords=[]
patternsSentences=[]
patternsBagOfWords=[]

# EXTRACT WORDS AND SENTENCES
for event in parentDictionary["intents"]:
    print(event)
    tagWords.append(event["tag"])
    patternsSentences.extend(event["patterns"])

print("")
print("tagWords",tagWords)
print("")
print("patternsSentences",patternsSentences)

# GET BAG OF WORDS FOR THE PATTERNS SENTENCES
# Initialize CountVectorizer
patternsBagOfWordsVectorizer = CountVectorizer()
# Fit the CountVectorizer on the list of patterns
patternsBagOfWordsVectorizer.fit(patternsSentences)
# Get the feature names (words) corresponding to each column in the bag of words
patternsBagOfWords = patternsBagOfWordsVectorizer.get_feature_names_out()
print("\n patternsBagOfWords",patternsBagOfWords)


#SAVE BAGS OF WORDS IN THE PICKLE FILE
with open("tagWords.pkl", 'wb') as file:
    pickle.dump(tagWords, file)

with open("patternsBagOfWords.pkl", 'wb') as file:
    pickle.dump(patternsBagOfWords, file)

with open("tagWords.pkl", 'rb') as file:
    tagWords = pickle.load(file)

with open("patternsBagOfWords.pkl", 'rb') as file:
    patternsBagOfWords = pickle.load(file)

print("")
print("tagWords",tagWords)
print("")
print("patternsBagOfWords",patternsBagOfWords)

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


# # CREATE NEW VECTORIZER BASED ON PREVIOUSLY USED BAG OF WORDS - NOTE: USED IN CHATBOT SCRIPT
# newExampleVectorizer = CountVectorizer(vocabulary=tagWords)
# newExampleSparseMatrix=newExampleVectorizer.fit(tagWords) # Get entire dataset in shape of sparse matrix NOTE: Used only for the data analyze
#
# # print("\n", "newExampleVectorizer",newExampleVectorizer)
# # print("\n", "newExampleSparseMatrix",newExampleSparseMatrix)
# # print("\n", "newExampleVectorsMatrix", newExampleVectorsMatrix)
#
# # GET ALL TOKENS TOGETHER WITH ALL TOKENS VALUES
# token_vocabulary=list(newExampleVectorizer.vocabulary_.values())
# token_values = list(newExampleVectorizer.vocabulary_.keys())
# # print("\n", "token_vocabulary",token_vocabulary)
# # print("\n", "token_values",token_values)
#
# # PRINTS KEY AND VALUES TOGETHER
# for newExampleWord, newExampleToken in zip(token_vocabulary,token_values):
#     print(newExampleWord,"-",newExampleToken)
#
# new_sentence = "age name"
# new_vector = newExampleVectorizer.transform([new_sentence]).toarray()
# print("new_vector",new_vector)

# PATTERNS DATASET PREPROCESSING
patternsVectorizer = CountVectorizer(vocabulary=patternsBagOfWords)
patternsSparseMatrix=patternsVectorizer.fit(patternsBagOfWords) # Get entire dataset in shape of sparse matrix NOTE: Used only for the data analyze

# print("\n", "patternsVectorizer",patternsVectorizer)
# print("\n", "patternsSparseMatrix",patternsSparseMatrix)
# print("\n", "patternsVectorsMatrix", patternsVectorsMatrix)

# GET ALL TOKENS TOGETHER WITH ALL TOKENS VALUES
token_vocabulary=list(patternsVectorizer.vocabulary_.values())
token_values = list(patternsVectorizer.vocabulary_.keys())
# print("\n", "token_vocabulary",token_vocabulary)
# print("\n", "token_values",token_values)

# PRINTS KEY AND VALUES TOGETHER
for patternsWord, patternsToken in zip(token_vocabulary,token_values):
    print(patternsWord,"-",patternsToken)


# TODO: IMPLEMENT IT DOWN--------------------------------------------------------- CREATE TRAINING DATASET ---------------------------------------------------------
train_x=[]
train_y=[]

# Flatten the list of patterns and tags into a single list
fullDatasetWorsdForm = [[[pattern], [intent["tag"]]] for intent in parentDictionary["intents"] for pattern in intent["patterns"]]
# Print the two-dimensional list
print("\n fullDatasetWorsdForm",fullDatasetWorsdForm)

# Convert the list to a NumPy array
fullDatasetWorsdForm = np.array(fullDatasetWorsdForm)
print("\n fullDatasetWorsdForm.shape",fullDatasetWorsdForm.shape)

for i in fullDatasetWorsdForm:
    print(i[0])
    print(i[1])
    train_x.extend(patternsVectorizer.transform(i[0]).toarray())
    train_y.extend(tagVectorizer.transform(i[1]).toarray())

print(train_x)
print(train_y)
train_x=np.array(train_x)
train_y=np.array(train_y)

print("\n")
print(train_x)
print(train_y)
print("train_x.shape",train_x.shape)
print("train_y.shape",train_y.shape)


    sgd=tf.keras.optimizers.legacy.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len (train_y[0]), activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist=model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5',hist)

print("Done")