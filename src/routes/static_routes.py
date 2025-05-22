from flask import Blueprint, render_template

static_bp = Blueprint('static_bp', __name__)

@static_bp.route('/trangchu')
def trangchu():
    return render_template('trangchu.html')

@static_bp.route('/trangweb')
def trangweb():
    return render_template('trangweb.html')

@static_bp.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@static_bp.route('/dsvieclam')
def dsvieclam():
    return render_template('dsvieclam.html')

@static_bp.route("/pvan")
def phong_van():
    return render_template("pvan.html")  
