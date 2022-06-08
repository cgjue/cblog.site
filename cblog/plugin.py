import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from cblog.db import get_db

def get_plugin():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'plugin_matrix' not in g:
        db = get_db()
        plugin = db.execute('select name,script, id from plugin').fetchall()
        return plugin


def add_plugin(name, script):
    db = get_db()
    has = db.execute('select id from plugin where name = ?', (name, )).fetchone()
    if has:
        return has['id']
    else:
        db.execute('INSERT INTO plugin(name, script) VALUES(?, ?)', (name, script))
        db.commit()
        id = db.execute('select id from plugin where name = ?', (name, )).fetchone()
        return id['id']

def delete_plugin(name):
    db = get_db()
    has = db.execute("select id from plugin where name= ? ", (name, )).fetchone()
    if has:
        db.execute("delete from use_plugin where plugin_id = ?", (has['id'], ))
        db.execute("delete from plugin where name= ?", (name,))
        db.commit()
        return True
    return False
def set_plugin(plugin_id, post_id, use):
    db = get_db()
    id = db.execute('select id from use_plugin where plugin_id = ? and post_id = ?', (plugin_id, post_id)).fetchone()
    if id:
        db.execute('update use_plugin set use=? where id=?', (use, id['id']))
    else:
        db.execute('insert into use_plugin(plugin_id, post_id, use) values(?,?,?)', (plugin_id, post_id, use))
    db.commit()

def update_plugin(plugin_id, name, script):
    db =get_db()
    db.execute('update plugin set name=?, script=? where id=?', (name, script, plugin_id))
    db.commit()

def use_plugin(post_id):
    db = get_db()
    return db.execute("select * from use_plugin where post_id=?", (post_id, )).fetchall()

def use_plugin_all():
    db = get_db()
    return db.execute("select * from use_plugin").fetchall()
    