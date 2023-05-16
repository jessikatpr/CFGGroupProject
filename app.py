from flask import Flask, render_template, jsonify, request, redirect, url_for
# from code import savings_account

app = Flask(__name__)
app.config['SECRET_KEY'] = 'E8E7210201393474C554BF92'

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/savingsinvestments", methods=["POST", "GET"])
def savingsinvestments():
    return render_template("savingsinvestments.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/budgeting", methods=["POST", "GET"])
def budgeting():
    return render_template("budgeting.html")

if __name__ == "__main__":
    app.run(debug=True)

