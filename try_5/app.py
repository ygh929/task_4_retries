from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Placeholder data - replace with your startup's info
startup_name = "My Awesome Startup"
startup_description = "Revolutionizing the way people do things!"
startup_tagline = "The future is here."

waitlist = []  # List to store emails and names

@app.route("/")
def index():
    return render_template("index.html", 
                           startup_name=startup_name,
                           startup_description=startup_description,
                           startup_tagline=startup_tagline)


@app.route("/join", methods=["POST"])
def join_waitlist():
    try:
        email = request.form.get("email")
        full_name = request.form.get("fullName")

        if not email or not full_name:
            return jsonify({"message": "Email and full name are required."}), 400

        waitlist.append({"email": email, "fullName": full_name})  # Add to list
        return jsonify({"message": "Thanks for joining the waitlist!"}), 200
    except Exception as e:
        print(str(e)) # Log the error for debugging
        return jsonify({"message": "An error occurred."}), 500



if __name__ == "__main__":
    app.run(debug=True) 