from flask import Flask, render_template, redirect, url_for
import os
import requests
import json
from forms import ItemEditForm, NewItemForm

app_client = Flask(__name__)
app_client.config['SECRET_KEY'] = os.environ.get('secret_key')

base_url = 'http://127.0.0.1:5000'


@app_client.route("/")
def items():
    r = requests.get(f'{base_url}/items')
    result = json.loads(r.text)
    return render_template("items.html", result=result)


@app_client.route("/new_item", methods=['GET', 'POST'])
def new_item():
    form = NewItemForm()
    if form.validate_on_submit():
        add_item = {
            "name": form.name.data,
            "price": form.price.data,
            "qtty": form.qtty.data
        }
        r = requests.post(f'{base_url}/items', json=add_item)
        return redirect(url_for('items'))
    return render_template("new_item.html", form=form)


@app_client.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    form = ItemEditForm()
    r = requests.get(f'{base_url}/items/{id}')
    result = json.loads(r.text)
    if form.validate_on_submit():
        add_item = {
            "name": form.name.data,
            "price": form.price.data,
            "qtty": form.qtty.data
        }
        r = requests.put(f'{base_url}/items/{id}', json=add_item)
        return redirect(url_for('items'))
    return render_template("edit.html", form=form, result=result)


@app_client.route("/delete/<int:id>", methods=['GET'])
def delete(id):
    r = requests.delete(f'{base_url}/items/{id}')

    return redirect(url_for('items'))


if __name__ == '__main__':
    app_client.run(host='127.0.0.1', port=5001, debug=True)
