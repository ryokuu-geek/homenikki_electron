from curses.ascii import SP
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from lib.recognize import Recognizer
from lib.speaker import Speaker

app = Flask(__name__)
# データベースの設定(sqliteファイルのパスを指定)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homenikki.sqlite'
db = SQLAlchemy(app)


class Homenikki(db.Model):
    __tablename__ = 'homenikkis'
    # ID
    id = db.Column(db.Integer, primary_key=True)
    # 要約
    summary = db.Column(db.String(20), nullable=False)
    # 詳細
    detail = db.Column(db.String(200), nullable=True)
    # ほめ文
    praise = db.Column(db.String(50), nullable=True)
    # 作成日
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


# ルートにアクセスされたらインデックページを開く
@app.route('/', methods=['POST', 'GET'])
def index():
    # POSTメソッドで要求されたら
    if request.method == 'POST':
        # コンテンツを取得
        task_summary = request.form['summary']
        task_detail = request.form['detail']

        # 音声合成
        rc = Recognizer()
        task_home = rc.fill_template(rc.recognize(task_summary))
        sp = Speaker()
        sp.speak(task_home)

        # 新しいタスクを作成
        new_task = Homenikki(summary=task_summary, detail=task_detail, praise=task_home)

        try:
            # データベースに新しいタスクを登録しトップページにリダイレクト
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "フォームの送信中に問題が発生しました"
    # 要求がない場合は、タスクリストを日付順に並べて表示
    else:
        tasks = Homenikki.query.order_by(Homenikki.date_created.desc()).all()
        
        return render_template('diary.html', tasks=tasks)

"""

app.route('/delete/<int:id>')
def delete(id):
    # 削除するタスクのIDを取得
    task_to_delete = Homenikki.query.get_or_404(id)

    try:
        # 削除対象のタスクをDBから削除しトップページにリダイレクト
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return '削除中に問題が発生しました'

"""

# 編集画面
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def update(id):
    # 編集するタスクのIDを取得
    task_to_edit = Homenikki.query.get_or_404(id)
    # POSTメソッドがきたら編集対象のIDのコンテンツを更新
    if request.method == 'POST':
        task_to_edit.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "タスクの編集中に問題が発生しました"
    else:
        return render_template('edit.html', task=task_to_edit)


if __name__ == "__main__":
    # モデルからテーブルを作成(データベースファイルを最初に作るときだけ実行)
    db.create_all()
    
    # アプリを起動(データベースファイルを最初に作るときはコメントアウトして実行しない)
    app.run(host="127.0.0.1", port=8080)