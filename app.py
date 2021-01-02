from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcom to my 'Home' page!"

    if __name__ == "__main__":
        app.run(debug=True)