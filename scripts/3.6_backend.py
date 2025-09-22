# Entyre interaction work   s like expected
# UI, BACKEND, JS WORKS
import tensorflow as tf
from flask import Flask, redirect, render_template, request, session, jsonify, send_from_directory
from chatbot import vectorizeInputSntence, decodeVectorizedTag, getResponse, extractMediaContent

# LOAD TRAINED MODEL
model = tf.keras.models.load_model('chatbot_model.h5')

# Initialize 'inputMessageList' and 'outputMessageList' in the session
app = Flask(__name__)
app.secret_key = '123456789'

# Initialize 'messages' for both "GET" and "POST" requests
messages = []

@app.route("/", methods=["POST", "GET"])
def home():

    global messages  # Make 'messages' a global variable

    if request.method == "POST":

        inputMessage = request.form["nm"]
        inputBoWArray = vectorizeInputSntence(inputMessage)
        predictions = model.predict(inputBoWArray)
        predictedTag = decodeVectorizedTag(predictions)
        response = getResponse(predictedTag)
        print(response)

        mediaContent=extractMediaContent(response)

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

        # Add the userInput value to the inputMessage list in the session
        outputMessageMediaList = session.get('outputMessageMediaList', [])
        outputMessageMediaList.append(mediaContent)
        session['outputMessageMediaList'] = outputMessageMediaList
        print("session['outputMessageMediaList']",session['outputMessageMediaList'])

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

    return render_template("3.6_index.html", messages=messages)

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
    app.run(debug=True)
