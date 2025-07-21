from flask import Flask, render_template, request
app=Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index_page():
    if request.method == "POST":
        return render_template('register.html')
    else:
        return render_template('index.html')

