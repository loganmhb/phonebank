# all the imports
import os
import re
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'phonebank.db'),
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('PHONEBANK_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    """Initialize a new, empty database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

@app.route('/')
def show_contacts():
    db = get_db()
    cur = db.execute('select * from contacts order by id asc')
    contacts = cur.fetchall()
    return render_template('show_contacts.html', contacts=contacts)

@app.route('/', methods=['POST'])
def add_contact():
    db = get_db()
    f = request.form
    cleaned_number = re.sub(r'\D', '', f['phone_number'])
    if len(cleaned_number) != 10:
        abort(400)
    db.execute('insert into contacts (name, address, phone_number, notes) values (?, ?, ?, ?)', [f['name'], f['address'], f['phone_number'], f['notes']])
    db.commit()
    flash('Contact added.')
    return redirect(url_for('show_contacts'))
