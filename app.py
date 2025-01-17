from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def ekemai():
    return render_template('home.html')


@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/pricing")
def pricing():
    return render_template('pricing.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)