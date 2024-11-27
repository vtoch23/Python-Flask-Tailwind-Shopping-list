from flask import Flask, render_template, redirect, request, url_for
from models import get_items, add_item, delete_item, total_cost, total_discount, total_paid

app = Flask(__name__)


@app.route('/', methods=["GET"])
def get_all():
    records = get_items()
    total = total_cost()
    total_disc = total_discount()
    total_p = total_paid()
    return render_template('index.html', records=records, total=total, total_disc=total_disc, total_p=total_p)


@app.route('/add_item', methods=["POST"])
def add():
    name = request.form['name']
    price = request.form['price']
    discount = request.form['discount']

    add_item(name, price, discount)

    return redirect(url_for('get_all'))


@app.route('/delete', methods=['POST'])
def delete():
    id = request.form['id']
    delete_item(id)

    return redirect(url_for('get_all'))


if __name__ == '__main__':
    app.run(debug=True)