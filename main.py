import os
import File
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from speech import speech_en, speech_fr
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diary.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploaded"
db = SQLAlchemy(app)



class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(1000), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Card {self.id}>"


@app.route("/")
def index():
    try:
        cards = Card.query.order_by(Card.id).all()
    except:
        db.drop_all()  # Caution: This will delete all data
        db.create_all()
        cards = Card.query.order_by(Card.id).all()
    return render_template("index.html", cards=cards)


@app.route("/card/<int:id>")
def card(id):
    card = Card.query.get(id)
    return render_template("card.html", card=card)


@app.route("/create")
def create():
    return render_template("create_card.html")


@app.route("/voice")
def voices():
    try:
        text = speech_en()
    except:
        db.drop_all()  # Caution: This will delete all data
        db.create_all()
        text = ""
        flash("Algo salió mal...")
    return render_template("create_card.html", text=text)


@app.route("/form_create", methods=["GET", "POST"])
def form_create():
    if request.method == "POST":
        if 'img' not in request.files:
            flash('No file part')
            return redirect(request.url)
        img = request.files["img"]
        if img.filename == '':
            flash('No selected file')
            return redirect(request.url)
        

        title = request.form["title"]
        subtitle = request.form["subtitle"]
        text = request.form["text"]

        card = Card(img="", title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()

        filename = secure_filename(f"{card.id}{File.get_filetype(img.filename)}")
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        card.img = f"static/uploaded/{filename}"
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template("create_card.html")

if __name__ == "__main__":
    app.run(debug=True)

