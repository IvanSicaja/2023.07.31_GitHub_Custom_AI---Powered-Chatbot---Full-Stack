import re
import json
import random
import pickle
import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer


from urllib.parse import urlparse, parse_qs

# --------------------------------------------------------- LOADING TRAINED MODEL AND BOWs ---------------------------------------------------------

# LOAD TRAINED MODEL
model = tf.keras.models.load_model('chatbot_model.h5')

# LOAD PARENT DICTIONARY
parentDictionary = json.loads(open('questionsAnswersAndCatergoriesDatabase.json').read())

#LOAD BAGS OF WORDS IN THE PICKLE FILE
with open("dynamicDatabase/tagWords.pkl", 'rb') as file:
    tagWords = pickle.load(file)

with open("dynamicDatabase/patternsBagOfWords.pkl", 'rb') as file:
    patternsBagOfWords = pickle.load(file)

#print("")
#print("tagWords",tagWords)
#print("")
#print("patternsBagOfWords",patternsBagOfWords)

# --------------------------------------------------------- FUNCTIONS DEFINITION ---------------------------------------------------------

# CONVERT THE INPUT SENTENCE IN THE BAG OF WORD ARRAY SIZE [[]]
def vectorizeInputSntence(string):
    # PATTERNS DATASET PREPROCESSING
    patternsVectorizer = CountVectorizer(vocabulary=patternsBagOfWords)
    patternsSparseMatrix = patternsVectorizer.fit(patternsBagOfWords)  # Get entire dataset in shape of sparse matrix NOTE: Used only for the data analyze

    # #print("\n", "patternsVectorizer",patternsVectorizer)
    # #print("\n", "patternsSparseMatrix",patternsSparseMatrix)
    # #print("\n", "patternsVectorsMatrix", patternsVectorsMatrix)

    # GET ALL TOKENS TOGETHER WITH ALL TOKENS VALUES
    token_vocabulary = list(patternsVectorizer.vocabulary_.values())
    token_values = list(patternsVectorizer.vocabulary_.keys())  # #print("\n", "token_vocabulary",token_vocabulary)  # #print("\n", "token_values",token_values)
    vectorizedInputSntence=patternsVectorizer.transform([string]).toarray()

    return vectorizedInputSntence


def decodeVectorizedTag(predictions):

    highestPredictedIndex = np.argmax(predictions)
    # print("Index of the element with the maximum value:", max_index)

    # Print all indexes and corresponding class probabilities
    for index, probability in enumerate(predictions[0]):
        print(f"Index: {index}, Probability: {probability}")

    # TAG DATASET PREPROCESSING
    tagVectorizer = CountVectorizer(vocabulary=tagWords)
    tagSparseMatrix = tagVectorizer.fit(tagWords)  # Get entire dataset in shape of sparse matrix NOTE: Used only for the data analyze

    #print("\n", "tagVectorizer",tagVectorizer)
    #print("\n", "tagSparseMatrix",tagSparseMatrix)
    # #print("\n", "tagVectorsMatrix", tagVectorsMatrix)

    # GET ALL TOKENS TOGETHER WITH ALL TOKENS VALUES
    token_vocabulary = list(tagVectorizer.vocabulary_.values())
    token_values = list(tagVectorizer.vocabulary_.keys())
    # #print("\n", "token_vocabulary",token_vocabulary)
    # #print("\n", "token_values",token_values)

    tagsDictionary={}

    # PRINTS KEY AND VALUES TOGETHER
    for tagWord, tagToken in zip(token_vocabulary, token_values):
        #print(tagWord, "-", tagToken)
        tagsDictionary[int(tagWord)] = tagToken

    return tagsDictionary[int(highestPredictedIndex)]

def getResponse(targetTag):

    # Find the intent with the target tag
    intent = next((intent for intent in parentDictionary["intents"] if intent["tag"] == targetTag), None)

    if intent:
        # Get a random response from the list of responses
        random_response = random.choice(intent["responses"])
        # print(random_response) # Final print
        return random_response
    else:
        return print("Tag not found in the dataset.") # Final print


def extractMediaContent(response):
    # Use regular expression to find a web link in the response
    link_matches = re.findall(r'https?://\S+', response)

    # Check if the link is from YouTube
    if link_matches:
        # Extract the first link found in the response
        extracted_link = link_matches[0]

        # Check if the response contains the keyword "2cellos"
        if "2cellos" in response.lower():
            # Play from 1 minute 44 seconds
            final_link = extracted_link
            return {"youTubeVideo": final_link}
        else:
            # Play from the beginning
            return {"youTubeShorts": extracted_link}

    # Check if the response contains the specific text for an image using re module
    elif "The example design is shown on the image below" in response:
        print("True")
        return {"image": "static/jersey.png"}

    # Return None if no match is found
    return {"noMedia": "noMedia"}


# CONSOLE CHATBOT REPLACED WITH UI
if __name__ == "__main__":

    # --------------------------------------------------------- MAIN CHATBOT LOOP ---------------------------------------------------------
    print("CHATBOT IS STARTED. TYPE YOUR MESSAGE BELLOW:")  # Final print
    print("_____________________________________________")  # Final print

    while True:
        inputMessage = input("")
        inputBoWArray = vectorizeInputSntence(inputMessage)
        # print("inputBoWArray",inputBoWArray)
        predictions = model.predict(inputBoWArray)
        # print("predictions",predictions)
        predictedTag = decodeVectorizedTag(predictions)
        # print("predictedTag",predictedTag)
        response = getResponse(predictedTag)
        print(response)

        # Example usage:
        result = extractMediaContent(response)

        print(result)


    # Checking does response has a link or the design

    # THIS BLOCK IS ONLY FOR THE CONSOLE DEMONSTRATION
    # # Use regular expression to find a web link in the response
    # link_matches = re.findall(r'https?://\S+', response)
    #
    # # Check if the link is from YouTube
    # if link_matches:
    #     # Extract the first link found in the response
    #     extracted_link = link_matches[0]
    #     print("Extracted link:", extracted_link)
    #
    #     # Check if the response contains the keyword "2cellos"
    #     if "2cellos" in response.lower():
    #         # Play from 1 minute 44 seconds
    #         webbrowser.open(extracted_link + "&t=1m44s")
    #     else:
    #         # Play from the beginning
    #         webbrowser.open(extracted_link)







