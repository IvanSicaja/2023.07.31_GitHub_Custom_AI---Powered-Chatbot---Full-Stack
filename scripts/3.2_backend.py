# This script is possible to increase and reset counter with the good looking web page and javascript
import tensorflow as tf
from flask import Flask, redirect, render_template, request, session, jsonify, send_from_directory
from chatbot import vectorizeInputSntence, decodeVectorizedTag, getResponse

# LOAD TRAINED MODEL
model = tf.keras.models.load_model('chatbot_model.h5')

# Initialize 'inputMessageList' and 'outputMessageList' in the session
app = Flask(__name__)
app.secret_key = '123456789'


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":

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
        print(session['inputMessageList'])

        # Add the userInput value to the inputMessage list in the session
        outputMessageList = session.get('outputMessageList', [])
        outputMessageList.append(response)
        session['outputMessageList'] = outputMessageList
        print(session['outputMessageList'])


        # Instead of returning a page directly, issue a redirect to avoid POST refresh issues
        return redirect('/')

    return render_template("3.2_index.html",inputMessagesArray=session['inputMessageList'], outputMessagesArray=session['outputMessageList'])

@app.route("/reset_counter", methods=["POST"])
def reset_counter():
    # Clear both the outputMessageList and inputMessageList in the session
    session['outputMessageList'] = []
    session['inputMessageList'] = []
    return jsonify({"outputMessageList": [], "inputMessageList": []})

# Serve static files from the "static" directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
