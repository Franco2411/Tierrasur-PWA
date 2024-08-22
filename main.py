from flask import Flask, request, url_for, redirect, render_template

server = Flask(__name__)

@server.route('/')
def index():
    return render_template('index.html')

@server.route('/login')
def login():
    return render_template('login.html')