from flask import url_for, Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import click
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
login_manager = LoginManager(app)  # 实例化扩展类

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if request.form['submit_button'] == "Existing User":
            return redirect(url_for('exist_user'))
        else:
            return redirect(url_for('new_user'))


    return render_template('index.html')

@app.route('/exist', methods=['GET', 'POST'])
def exist_user():
    if request.method == "POST":
        if request.form['submit_button'] == "Confirm":
            value = 0
            s_option = request.values.getlist("img")
            for s in s_option:
                value += int(s)
            return redirect(url_for('result', value=value))

        elif request.form['submit_button'] == "New":
            flash("Change New Item.")
            return redirect(url_for('exist_user'))


    return render_template('exist.html')


@app.route('/new', methods=['GET', 'POST'])
def new_user():
    if request.method == "POST":
        if request.form['submit_button'] == "Confirm":
            flash("Item Confirmed.")
            return redirect(url_for('new_user'))

        else:
            flash("Go to new page.")
            return redirect(url_for('new_user'))


    return render_template('new.html')

@app.route('/result/<value>')
def result(value):
    return render_template('result.html', value=str(value))

    
