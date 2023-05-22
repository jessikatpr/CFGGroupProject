import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_investment import investment_lookup
from werkzeug.utils import secure_filename
# from code import savings_account

# set an upload folder
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'csv'}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'E8E7210201393474C554BF92'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/savings", methods=["POST", "GET"])
def savings():
    # User reached rout via POST (submitting info in the form)
    if request.method == "POST":
        # Ensure all fields were filled in
        if not request.form.get("money"):
            return "must fill in all fields!"
        if not request.form.get("years"):
            return "must fill in all fields!"
        if not request.form.get("interest"):
            return "must fill in all fields!"
        money = float(request.form.get("money"))
        years = float(request.form.get("years"))
        interest = float(request.form.get("interest"))
        final_money = money * ((1 + interest / 100) ** years)
        output = str(f"You said you would save £{money} over {years} years with an interest rate of {interest}%. You will earn £{final_money} over {years} years.")
        return render_template("savings_result.html", final_money=final_money, output=output)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("savings.html")

@app.route("/savings_result", methods=["POST", "GET"])
def savings_result():
    return render_template("savings_result.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/budgeting", methods=["POST", "GET"])
def budgeting():
    payslip_file = url_for('static', filename="Payslip test file.pdf")
    expense_file = url_for('static', filename='Expense test file.csv')
    return render_template("budgeting.html", payslip_file=payslip_file, expense_file=expense_file)

@app.route("/get_summary", methods=["POST"])
def get_summary():
    if request.method == "POST":
        return render_template("get_summary.html")

# Investment Selection Page
@app.route("/investment_search",  methods=["GET", "POST"])
def calculate_value():
    """Get stock quote."""
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return render_template('error.html')

        if not request.form.get("quantity"):
            return render_template('error.html')

        else:
            data = investment_lookup(request.form.get("symbol"), request.form.get("quantity"))
            if data:
                return render_template("investment_result.html", name=data["name"], symbol=data["symbol"], price=data["price"], value=data["value"], quantity=data["quantity"])
            else:
                return render_template('error.html')

        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("investment_search.html")


# Display result of investment search
@app.route('/investment_result')
def display_results():
    return render_template("investment_result.html")

if __name__ == "__main__":
    app.run(debug=True)

