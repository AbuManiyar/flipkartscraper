from flask import Flask, render_template, request,jsonify
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO,)


application = Flask(__name__)
app = application

@app.route('/')
def home():
    return render_template("home.html")

if __name__=="__main__":
    app.run(debug=True)
    