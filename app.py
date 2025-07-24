from flask import Flask, render_template, request
app=Flask(__name__)
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

@app.route('/', methods=["GET","POST"])
def index_page():
    if request.method == "POST":
        return render_template('register.html')
    else:
        return render_template('index.html')

