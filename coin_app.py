from flask import Flask, render_template, url_for
import api_call
app = Flask(__name__)

coins = api_call
print(coins)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", coins=coins)

@app.route("/about")
def about():
    return render_template("about.html", title='About')


# Makes application run straight through python
if __name__ == "__main__":
    # Uses debug mode so its not necessary restart app everytime we make changes to be able to see them
    app.run(debug=True)

