import os
import csv
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
# from tensorflow.keras.optimizers import SGD
import matplotlib.pyplot as plt


# --------------------------------------------------------- FUNCTION DEFINITIONS ---------------------------------------------------------


def save_words_to_txt_files(oneDimensionalArray, saveToPath):
    # Delete file if it exists
    if os.path.exists(saveToPath):
        os.remove(saveToPath)

    # Save oneDimensionalArray to the specified file
    with open(saveToPath, 'w') as file:
        for element in oneDimensionalArray:
            file.write(element + '\n')

    # Verify the contents of the saved file
    with open(saveToPath, 'r') as file:
        saved_elements = [line.strip() for line in file]

    # print("Saved elements:", saved_elements)

# --------------------------------------------------------- EXTRACT AND SAVE WORDS FOROM .JSON FILE ---------------------------------------------------------
parentDictionary = json.loads(open('questionsAnswersAndCatergoriesDatabase.json').read())

tagWords=[]
patternsSentences=[]

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
with open("dynamicDatabase/tagWords.pkl", 'wb') as file:
    pickle.dump(tagWords, file)

with open("dynamicDatabase/patternsBagOfWords.pkl", 'wb') as file:
    pickle.dump(patternsBagOfWords, file)

with open("dynamicDatabase/tagWords.pkl", 'rb') as file:
    tagWords = pickle.load(file)

with open("dynamicDatabase/patternsBagOfWords.pkl", 'rb') as file:
    patternsBagOfWords = pickle.load(file)

# Specify file paths
tagWords_file_path = "dynamicDatabase/tagWords.txt"
patternsBagOfWords_file_path = "dynamicDatabase/patternsBagOfWords.txt"

# Call the function with your existing variables and file paths
save_words_to_txt_files(tagWords, tagWords_file_path)
save_words_to_txt_files(patternsBagOfWords, patternsBagOfWords_file_path)

print("")
print("tagWords",tagWords)
print("")
print("patternsBagOfWords",patternsBagOfWords)
# patternsBagOfWords=[]

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

# PRINTS KEY AND VALUES TOGETHER AND SAVE THEM IN A .TXT FILE
for tagWord, tagToken in zip(token_vocabulary,token_values):
    print(tagWord,"-",tagToken)

# Specify the file path
vocabularyAndValuesPairs_patterns_file_path = "dynamicDatabase/vocabularyAndValuesPairs_patterns.txt"

# Delete the file if it already exists
if os.path.exists(vocabularyAndValuesPairs_patterns_file_path):
    os.remove(vocabularyAndValuesPairs_patterns_file_path)

# Create and write tagWord-token pairs to the text file
with open(vocabularyAndValuesPairs_patterns_file_path, 'w') as file:
    for tagWord, tagToken in zip(token_vocabulary, token_values):
        file.write(f"{tagWord} - {tagToken}\n")

print(f"TagWord-Token pairs written to {vocabularyAndValuesPairs_patterns_file_path}")




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

# PRINTS KEY AND VALUES TOGETHER AND SAVE THEM IN A .TXT FILE
for patternsWord, patternsToken in zip(token_vocabulary,token_values):
    print(patternsWord,"-",patternsToken)

# Specify the file path
vocabularyAndValuesPairs_responses_file_path = "dynamicDatabase/vocabularyAndValuesPairs_responses.txt"

# Delete the file if it already exists
if os.path.exists(vocabularyAndValuesPairs_responses_file_path):
    os.remove(vocabularyAndValuesPairs_responses_file_path)

# Create and write tagWord-token pairs to the text file
with open(vocabularyAndValuesPairs_responses_file_path, 'w') as file:
    for tagWord, tagToken in zip(token_vocabulary, token_values):
        file.write(f"{tagWord} - {tagToken}\n")

print(f"TagWord-Token pairs written to {vocabularyAndValuesPairs_responses_file_path}")


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

    # PREVIOUS WAY
    train_x.extend(patternsVectorizer.transform(i[0]).toarray())
    train_y.extend(tagVectorizer.transform(i[1]).toarray())


print("train_x before conversion to np.array",train_x)
print("train_y before conversion to np.array",train_y)
train_x=np.array(train_x)
train_y=np.array(train_y)

print("\n")
print("train_x after conversion to np.array",train_x)
print("train_y after conversion to np.array",train_y)
print("train_x.shape",train_x.shape)
print("train_y.shape",train_y.shape)

#  SINGLE EXAMPLE COMPARISON BEFORE AND AFTER CONVERSION TO np.array
wantedIndex=10
print("train_x before conversion to np.array",train_x[wantedIndex])
print("train_x after conversion to np.array",train_x[wantedIndex])
print("train_y before conversion to np.array",train_y[wantedIndex])
print("train_y after conversion to np.array",train_y[wantedIndex])

counter = 0

for i in fullDatasetWorsdForm:
    if counter == wantedIndex:
        print(i[0])
        print(i[1])
        break  # Break out of the loop once the tenth occurrence is printed
    counter += 1


# MAKE ADDITIONALLY FULL .CSV DATASET


# Specify the CSV file path
csv_file_path = "dynamicDatabase/training_dataset.csv"

# Combine train_x and train_y into a single list
combined_data = list(zip(train_x, train_y))

# Write the combined_data to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header row (assuming train_x and train_y have the same number of features)
    header_row = ["train_x_feature_" + str(i) for i in range(train_x.shape[1])] + ["train_y_feature_" + str(i) for i in range(train_y.shape[1])]
    csv_writer.writerow(header_row)

    # Write data rows
    for example in combined_data:
        csv_writer.writerow(list(example[0]) + list(example[1]))

print(f"Training dataset written to {csv_file_path}")

# CREATE TRAINING AND VALIDATION DATASETS
X_train, X_val, y_train, y_val = train_test_split(train_x, train_y, test_size=0.2, random_state=42)


sgd=tf.keras.optimizers.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)


model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len (train_y[0]), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


# Train the model and store the training history
history = model.fit(X_train, y_train, epochs=20, batch_size=5, validation_data=(X_val, y_val), verbose=1)

# Save the trained model
model.save('chatbot_model.h5',history)

# Plot the training and validation accuracy over epochs
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Training', 'Validation'], loc='lower right')
plt.show()

print("Done")