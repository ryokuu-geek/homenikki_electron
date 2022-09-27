from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_login import login_fresh
from importlib_metadata import method_cache
from lib.speaker import Speaker
from lib.recognize import Recognizer

app = Flask(__name__)

data = {
        'diarys':[
            {'summary':'たこ焼きを食べた', 'date':'2022-5-13', 'detail':'安かったのでたこ焼きを買った。美味かった。', 'comment':'ええーっ！？たこ焼きを食べたなんて、あなたはなんて素晴らしい人だ！'},
            {'summary':'木を切り倒した', 'date':'2022-5-12', 'detail':'庭の木を切り倒した。虫が出てきた', 'comment':'ええーっ！？木を切り倒したなんて、あなたはなんて素晴らしい人だ！'}
        ],
        'add_flag':False
    }

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    return render_template('diary.html', data=data)

@app.route('/insert', methods=['POST'])
def insert():
    summary = request.form['summary']
    r = Recognizer()
    speaks = r.fill_template(r.recognize(summary))
    s = Speaker()
    s.speak(speaks)
    data['add_flag'] = True
    return redirect(url_for('diary'))

@app.route('/speech/<path:filename>', methods=['GET'])
def praise(filename):
    return send_from_directory('audio/', filename)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if(request.method == 'GET'):
        return render_template('signup.html')
    elif(request.method == 'POST'):
        return '<h1>登録完了</h1>'

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if(request.method == 'GET'):
        return render_template('signin.html')
    elif(request.method == 'POST'):
        return 'abc'
        #return redirect(url_for('diary'))


if(__name__ == '__main__'):
    app.run()