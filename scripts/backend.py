# Entire interaction work   s like expected
# UI, BACKEND, JS WORKS
import re
import os
import tensorflow as tf
from googleapiclient.discovery import build
from chatbot import vectorizeInputSntence, decodeVectorizedTag, getResponse, extractMediaContent
from flask import Flask, redirect, render_template, request, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np

# LOAD TRAINED MODEL
model = tf.keras.models.load_model('chatbot_model.h5')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = '123456789'

# Initialize 'messages' for both "GET" and "POST" requests
messages = []

api_key = 'AIzaSyBNq7Ho2FLkTEkpu-aKUIq0K0xewv3NEPw'  # Replace with your actual YouTube API key
youtube = build('youtube', 'v3', developerKey=api_key)

# Add the following configuration after initializing the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#If you're unsure about the exact location, you can print out the database URI in your Flask application to see where it's pointing.
print("app.config['SQLALCHEMY_DATABASE_URI']",app.config['SQLALCHEMY_DATABASE_URI'])

# Initialize the database
db = SQLAlchemy(app)


# FUNCTIONS INITIALIZATION
def get_youtube_video_id(video_url):

    # Extract video ID from the YouTube URL
    video_id = video_url.split('v=')[-1]

    # Call the YouTube API to get details about the video
    video_details = youtube.videos().list(part='snippet', id=video_id).execute()

    # Check if the 'items' list is not empty
    if 'items' in video_details and video_details['items']:
        # Extract video ID from the API response
        video_id = video_details['items'][0]['id']
        return video_id
    else:
        # Handle the case where the video details are not available
        print("Error: Video details not found.")
        return None

def extract_shorts_video_id(shorts_link):
    # Example YouTube shorts link
    # shorts_link = "https://www.youtube.com/shorts/68GgsSn8T1g"

    # Use regular expression to extract the video ID from the shorts link
    match = re.search(r'/shorts/([^/]+)$', shorts_link)

    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None

class ChatMessage(db.Model):
    # Define database structure
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    input_message = db.Column(db.String(500), nullable=False)
    output_message = db.Column(db.String(500), nullable=False)
    predicted_tag = db.Column(db.String(100), nullable=False)
    predicted_tag_probability = db.Column(db.Float, nullable=False)
    output_media_type = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<ChatMessage {self.id}>'


@app.route("/", methods=["POST", "GET"])
def home():

    global messages  # Make 'messages' a global variable

    if request.method == "POST":

        # Send the form input to the backed and get the corresponding response form the backend trained model
        inputMessage = request.form["nm"]
        inputBoWArray = vectorizeInputSntence(inputMessage)
        predictions = model.predict(inputBoWArray)
        predictedTag = decodeVectorizedTag(predictions)
        response = getResponse(predictedTag)
        print(response)

        # Add the userInput value to the inputMessage list in the session
        inputMessageList = session.get('inputMessageList', [])
        inputMessageList.append(inputMessage)
        session['inputMessageList'] = inputMessageList
        print("session['inputMessageList']",session['inputMessageList'])

        # Add the chat bot output value to the outputMessageList list in the session
        outputMessageList = session.get('outputMessageList', [])
        outputMessageList.append(response)
        session['outputMessageList'] = outputMessageList
        print("session['outputMessageList']",session['outputMessageList'])

        # Add the outputMessageMediaList in the session
        outputMessageMediaList = session.get('outputMessageMediaList', [])

        # Extract the link or the path from the Chatbot response. The output is a dictionary e.g. {"youTubeVideo": "final_link"}
        mediaLinkOrPath=extractMediaContent(response)
        # Extract Video ID if it exists
        # Example mediaLinkOrPath value
        # Extract the key and value from the single key-value pair
        key, value = next(iter(mediaLinkOrPath.items()), (None, None))

        # Check if the key is "youTubeVideo" or "youTubeShorts"
        if key == "youTubeVideo":
            # Extract video ID from the YouTube video link
            mediaLinkOrPath["youTubeVideo"] = get_youtube_video_id(value)
        elif key == "youTubeShorts":
            # Extract video ID from the YouTube shorts link
            mediaLinkOrPath["youTubeShorts"] = extract_shorts_video_id(value)

        outputMessageMediaList.append(mediaLinkOrPath)
        session['outputMessageMediaList'] = outputMessageMediaList
        print("session['outputMessageMediaList']",session['outputMessageMediaList'])

        # PROCESSING PROBABILITY AND THE KEY ONLY FOR THE DATA BASE USAGE
        # Convert predictions to a NumPy array
        predictions_array = np.array(predictions)

        # Find the maximum value in the array
        max_probability = np.max(predictions_array)
        # Extract the key from mediaLinkOrPath
        key_for_database = next(iter(mediaLinkOrPath))

        new_message = ChatMessage(
            input_message=inputMessage,
            output_message=response,
            predicted_tag=predictedTag,
            predicted_tag_probability = max_probability,
            output_media_type=key_for_database
        )
        # Save the message to the database
        db.session.add(new_message)
        db.session.commit()

        # Zip input and output messages
        # messages = zip(session['inputMessageList'], session['outputMessageList'])
        # Zip input and output messages with unique IDs
        messages = list(enumerate(zip(session['inputMessageList'], session['outputMessageList'], session['outputMessageMediaList'])))

        for index, (input_message, output_message, output_message_media) in messages:
            print(f"Message {index + 1}:")
            print(f"Input Message: {input_message}")
            print(f"Output Message: {output_message}")
            print(f"Output Message Media: {output_message_media}")
            print()

        # print("type(messages)",type(messages))
        # print("messages",messages)
        #
        # # Print the values of 'messages'b
        # for input_message, output_message in messages:
        #     print(f'Input: {input_message}, Output: {output_message}')

        # Instead of returning a page directly, issue a redirect to avoid POST refresh issues
        return redirect('/')

    return render_template("index.html", messages=messages)

@app.route("/reset_counter", methods=["POST"])
def reset_counter():

    global messages  # Access the global variable

    # Clear both the outputMessageList and inputMessageList in the session
    session['inputMessageList'] = []
    session['outputMessageList'] = []
    session['outputMessageMediaList'] = []

    # Clear the 'messages' variable
    messages = []
    return jsonify({"outputMessageList": [], "inputMessageList": [], 'outputMessageMediaList': []})

# Serve static files from the "static" directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    # app.run(debug=True) # NOTE: Used in development
    app.run(host='0.0.0.0', port=5000, debug=False) # NOTE: Used in production
