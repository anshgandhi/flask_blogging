from flask import render_template
from fl_blog.main import main

@main.route('/')
def index():
    return render_template('index.html')