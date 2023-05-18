from flask import Flask, render_template, jsonify, request, redirect, url_for
# from code import savings_account

app = Flask(__name__)
app.config['SECRET_KEY'] = 'E8E7210201393474C554BF92'

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
        return str(final_money)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("savings.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/budgeting", methods=["POST", "GET"])
def budgeting():
    return render_template("budgeting.html")

# Investment Selection Page
@app.route('/investment_search',  methods=["GET", "POST"])
def calculate_value():
    """Get stock quote."""
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return "must provide stock symbol!"

        if not request.form.get("quantity"):
            return "must provide quantity!"

        else:
            data = temp(request.form.get("symbol"))
            if data:
                return render_template("investment_result.html", name=data["name"], symbol=data["symbol"], price=data["price"])
            else:
                return "invalid symbol!"

        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("investment_search.html")


# Display result of investment search
@app.route('/investment_result')
def display_results():
    return render_template("investment_result.html")

if __name__ == "__main__":
    app.run(debug=True)

