# This script is possible to increase and reset counter with the good looking web page and javascript

from flask import Flask, redirect, render_template, request, session, jsonify, send_from_directory

app = Flask(__name__)
app.secret_key = '123456789'


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        userInput = request.form["nm"]
        print(userInput)

        # Add the userInput value to the user_inputs list in the session
        user_inputs = session.get('user_inputs',[])
        user_inputs.append(userInput)
        session['user_inputs'] = user_inputs
        print(session['user_inputs'])

        counter = session.get('counter', 0)
        counter += 1
        session['counter'] = counter
        print(f'Counter: {counter}')

        # Instead of returning a page directly, issue a redirect to avoid POST refresh issues
        return redirect('/')

    counter = session.get('counter', 0)
    return render_template("3.0_index.html", counter=counter,inputMessagesArray=session['user_inputs'])

@app.route("/reset_counter", methods=["POST"])
def reset_counter():
    # Reset the counter to 0
    session['user_inputs'] = []
    return jsonify({"user_inputs": []})

# Serve static files from the "static" directory
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
