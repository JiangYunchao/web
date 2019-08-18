from flask import url_for, Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import click
from flask_login import LoginManager
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
login_manager = LoginManager(app)  # 实例化扩展类

f = open('/home/jiang/web/static/test_posi_20190816')
oft_list = f.readlines()
for n, oft in enumerate(oft_list):
    oft = oft.strip()
    oft = oft.split(',')
    oft_list[n] = oft
oft_list_copy = oft_list


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
    # img_list = ['/static/1.jpg', '/static/2.jpg', '/static/3.jpg']
    # imgName = '/static/' + random.choice(img_list)

    ofts = random.sample(oft_list_copy, 12)
    oft_dict = []
    #  添加判断剩余outfit数目是否小于可显示数目的code
    for n, oft in enumerate(ofts):
        # oft = oft.strip()
        # oft = oft.split(',')
        oft[1] = '/static/top/' + oft[1]
        oft[2] = '/static/bottom/' + oft[2]
        oft[3] = '/static/shoe/' + oft[3]
        id = int(oft[-1])

        oft_dict.append({"user":oft[0], "id":oft[4], "top":oft[1],
                         "bottom":oft[2], "shoe":oft[3]})

    if request.method == "POST":
        if request.form['submit_button'] == "Confirm":
            # print(imgName)
            # value = imgName.split('/')[-1]
            value = request.values.get("img")

            return redirect(url_for('after_confirm_exist', id=value))

        elif request.form['submit_button'] == "New":

            # return render_template('exist.html', imgName=imgName)
            # flash("Change New Item.")
            return redirect(url_for('exist_user'))


    return render_template('exist.html', oft_list=oft_dict)


@app.route('/new', methods=['GET', 'POST'])
def new_user():
    ofts = random.sample(oft_list_copy, 12)
    oft_dict = []
    #  添加判断剩余outfit数目是否小于可显示数目的code
    for n, oft in enumerate(ofts):
        oft[1] = '/static/top/' + oft[1]
        oft[2] = '/static/bottom/' + oft[2]
        oft[3] = '/static/shoe/' + oft[3]
        id = int(oft[-1])

        oft_dict.append({"user":oft[0], "id":oft[4], "top":oft[1],
                         "bottom":oft[2], "shoe":oft[3]})

    if request.method == "POST":
        if request.form['submit_button'] == "Confirm":
            s_option = request.values.getlist("img")
            value = ""
            for s in s_option:
                temp = "-" + s
                value += temp
            return redirect(url_for('after_confirm_new', id=value))

        elif request.form['submit_button'] == "New":

            # return render_template('exist.html', imgName=imgName)
            # flash("Change New Item.")
            return redirect(url_for('new_user'))

    return render_template('new.html', oft_list=oft_dict)

@app.route('/after_confirm_exist/<id>', methods=['GET', 'POST'])
def after_confirm_exist(id):
    if request.method == "POST":
        if request.form['submit_button'] == "Top-n Recommendation":
            return redirect(url_for('topn_exist', id=id))
        else:
            return redirect(url_for('cate_choose', id=id))

    return render_template('after_confirm.html')


@app.route('/after_confirm_new/<id>', methods=['GET', 'POST'])
def after_confirm_new(id):
    if request.method == "POST":
        if request.form['submit_button'] == "Top-n Recommendation":
            return redirect(url_for('topn_new', id=id))
        else:
            return redirect(url_for('cate_choose', id=id))

    return render_template('after_confirm.html')


@app.route('/topn_exist/<id>')
def topn_exist(id):
    result_list = []
    result_list.append(oft_list[int(id)])
    return render_template("topn.html", id_list=result_list)

@app.route('/itemRec_exist/<id>', methods=['POST', 'GET'])
def cate_choose(id):
    if request.method == "POST":
        cate = request.form['category']
        value = id + '-' + cate
        return redirect(url_for('item_show', value=value))
    # result_list = []
    # result_list.append(oft_list[int(id)])
    return render_template('itemRec.html', id_list=id)

@app.route('/item_show/<value>')
def item_show(value):
    id = value.split('-')[:-1]
    if len(id) > 1:
        id = id[1:]
    cate = value.split('-')[-1]
    return render_template('itemShow.html', id=id, cate=cate)



@app.route('/topn_new/<id>')
def topn_new(id):
    rcv = id.split('-')
    id_list = rcv[1:]
    result_list = []
    for i in id_list:
        result_list.append(oft_list[int(i)])
    return render_template("topn.html", id_list=result_list)

# @app.route('/itemRec_new/<id>')
# def itemRec_new(id):
#     rcv = id.split('-')
#     id_list = rcv[1:]
#     print(id_list)
#     result_list = []
#     for i in id_list:
#         result_list.append(oft_list[int(i)])
#     return render_template('itemRec.html', id_list=result_list)