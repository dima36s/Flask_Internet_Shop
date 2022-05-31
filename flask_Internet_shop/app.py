from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item_shop(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.TEXT, nullable=False)
    price = db.Column(db.INTEGER, nullable=False)
    is_active = db.Column(db.TEXT, default=True)

    def __repr__(self):
        return self.title


db.create_all()


@app.route('/')
def homepage():
    items = Item_shop.query.order_by(Item_shop.price).all()
    return render_template("index.html", items=items)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        item = Item_shop(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except TypeError:
            return "Произошла ошибка, попробуйте еще раз"
    else:
        return render_template("create.html")


if __name__ == '__main__':
    app.run(debug=True)
