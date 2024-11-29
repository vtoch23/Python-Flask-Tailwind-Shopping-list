from flask import Flask, render_template, redirect, request, url_for
from models import get_items, add_item, delete_item, total_cost, total_discount, total_paid

app = Flask(__name__)


@app.route('/', methods=["GET"])
def get_all():
    errorName = request.args.get('errorName', None)
    errorPrice = request.args.get('errorPrice', None)

    records = get_items()
    total = total_cost()
    total_disc = total_discount()
    paid = total_paid()

    return render_template('index.html', records=records, total=total, total_disc=total_disc, total_paid=paid, errorName=errorName, errorPrice=errorPrice)


@app.route('/add_item', methods=["POST"])
def add():
    errorPrice = None
    errorName = None
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        discount = request.form['discount']
        if discount:
            try:
                discount = int(discount)/100
            except ValueError:
                discount = float(discount)

        if not name:
            errorName = "Enter a valid name"
        if not price:
            errorPrice = "Enter a valid price"

        if errorName or errorPrice:
            return redirect(url_for('get_all', errorName=errorName, errorPrice=errorPrice))

        add_item(name, price, discount)
        return redirect(url_for('get_all'))

@app.route('/delete', methods=['POST'])
def delete():
    errorPrice = None
    errorName = None
    id = request.form['id']
    delete_item(id)

    return redirect(url_for('get_all', errorName=errorName, errorPrice=errorPrice))


if __name__ == '__main__':
    app.run(debug=True)