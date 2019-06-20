# -*- coding: UTF-8 -*-
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, 
    send_from_directory, jsonify
)
from cblog.db import get_db
from cblog.auth import login_required
from werkzeug.utils import secure_filename
import os, time
from flask import current_app
bp = Blueprint('admin', __name__)

@bp.route('/admin/index.html', methods = ('GET','POST'))
@login_required
def admin():
    posts = get_db().execute(
        'SELECT p.id, title, created, updated, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.author_id = ?',
        (session['user_id'],)
    ).fetchall()
    uploadfiles = get_db().execute('SELECT id, fpath, created from '
        'uploadfile where user_id = ?', 
        (session['user_id'], )
    ).fetchall()
    return render_template('admin/admin.html', posts = posts, uploadfiles = uploadfiles)
@bp.route('/admin/addCategory', methods = ("POST", ))
@login_required
def addCategory():
    category = request.form.get("category", default=None)
    error = None
    if not category:
        error = u"类别不能为空！"
        flash(error)
    else:
        db = get_db()
        if db.execute(
            'SELECT value FROM category WHERE value = ?',
            (category, )
        ).fetchone() is None:
            db.execute(
            'INSERT into category(value, user_id) VALUES(?, ?)',
            (category, session['user_id'] )
            )
            db.commit()
    return redirect(url_for('admin.admin'))

@bp.route('/admin/deleteCategory', methods = ("POST", ))
@login_required
def deleteCategory():
    category_ids = request.form.getlist('categories')
    if category_ids:
        db = get_db()
        for category_id in category_ids:
            if db.execute(
                'SELECT value FROM category WHERE id = ? and user_id = ?',
                (category_id, session['user_id'])
            ).fetchone() is not None:
                db.execute(
                'DELETE FROM category where id = ?',
                (category_id, )
                )
                db.commit()
    return redirect(url_for('admin.admin'))


ALLOWED_EXTENSIONS = set(['txt', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 
'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'ini', 'json', 
'plist', 'xml', 'yaml', 'yml','pdf', 'exe', 'zip', 'rar', 'py', 'js', 'css'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/admin/upload.html', methods = ('POST', ))
@login_required
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('admin.admin'))
    file = request.files.get('file', default=None)
    # if user does not select file, browser also
    # submit an empty part without filename
    if not file or file.filename == '':
        flash('No selected file')
    elif not allowed_file(file.filename):
        flash(u'禁止上传该类型文件')
    else:
        filename = str(int(time.time())) + secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        db = get_db()
        db.execute('INSERT INTO uploadfile(fpath, user_id) VALUES(?, ?)',
        (os.path.join(current_app.config['UPLOAD_FOLDER'][len(current_app.root_path):],
         filename), session['user_id']))
        db.commit()
    return redirect(url_for('admin.admin'))

@bp.route('/admin/deleteFile.html?<int:id>', methods=('POST',))
@login_required
def deleteFile(id):
    db = get_db()
    uploadfile = db.execute('SELECT fpath from uploadfile WHERE id = ? and user_id = ?',
    (id, session['user_id'])).fetchone()
    if uploadfile is None:
        return jsonify({'status':-1, 'msg':u'该文件不存在'})
    db.execute('DELETE FROM uploadfile WHERE id = ? and user_id = ?', (id, session['user_id']))
    db.commit()
    os.remove(current_app.root_path + uploadfile['fpath'])
    return jsonify({'status':0, 'msg':u'删除成功'})

@bp.route('/download/<filename>')
def download(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)
