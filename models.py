import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    database="new_db",
    password=""
)


def get_items():
    curr = conn.cursor(dictionary=True)
    curr.execute("select * from prod")
    records = curr.fetchall()
    return records


def add_item(name, price, discount):
    curr = conn.cursor(dictionary=True)
    curr.execute("insert into prod (name, price, discount) values (%s, %s, %s)", (name, price, discount))
    conn.commit()
    return get_items()


def delete_item(id):
    curr = conn.cursor(dictionary=True)
    curr.execute("delete from prod where id = %s", (id, ))
    conn.commit()

    return get_items()


def total_cost():
    curr = conn.cursor(dictionary=True)
    curr.execute("select * from prod")
    records = curr.fetchall()
    total = sum(item['price'] for item in records)
    return total


def total_paid():
    curr = conn.cursor(dictionary=True)
    curr.execute("select * from prod")
    records = curr.fetchall()
    act_price = 0
    total_paid = 0
    for record in records:
        act_price = record['price'] - record['price'] * record['discount']
        total_paid += act_price
    return total_paid


def total_discount():
    curr = conn.cursor(dictionary=True)
    curr.execute("select * from prod")
    records = curr.fetchall()
    total_price = total_cost()
    if records:
        total_discount = sum(item['price'] * item['discount'] for item in records)
        return round((total_discount/total_price)*100)
    else:
        pass
