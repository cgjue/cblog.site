# -*- coding: UTF-8 -*-
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from cblog.auth import login_required
from cblog.db import get_db
from cblog.plugin import get_plugin, use_plugin
import traceback

bp = Blueprint('blog', __name__)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@bp.route('/')
def index():
    """Show all the posts, most recent first."""
    
    posts = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)
bp.add_url_rule('/index.html', view_func=index)

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/category/<id>.html', methods=('GET', 'POST'))
def category(id=None):
    if id is None:
        return redirect(url_for('blog.index'))
    else:
        _id = id.split('_')[0]
        category = get_db().execute(
            'SELECT value FROM category where id = ?',
            (_id, )
        ).fetchone()
        if category is None:
            return render_template('404.html')
        posts = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id in (SELECT post_id from category_post'
        ' WHERE category_id = ? ) ORDER BY created DESC',
        (_id,)
        ).fetchall()
        return render_template('blog/category.html', posts = posts, category = category)
        
@bp.route('/view/<id>.html', methods=('GET', 'POST'))
def view(id=None):
    if id is None:
        return redirect(url_for('blog.index'))
    else:
        _id = id.split('_')[0]
        post = get_post(_id, False)
        scripts = ''
        plugin = get_plugin()
        use_p = use_plugin(_id)
        for i in plugin:
            add = True
            for j in use_p:
                if j['plugin_id'] == i['id'] and j['use'] == 0:
                    add = False
            if add:
                scripts += i['script'] + '\n'
        return render_template('blog/view.html', **locals())

@bp.route('/admin/createblog.html', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form.get('title',default = None)
        body = request.form.get('body', default = None)
        category_ids = request.form.getlist('categories')
        error = None
        if not category_ids:
            error = 'category is required.'
        elif not title:
            error = 'Title is required.'
        elif not body:
            error = 'Content is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            
            post_id = -1
            try:
                db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
                )
		
                post_id = db.execute(
                'SELECT max(id) as mid FROM post'
            ).fetchone()['mid']
                print(post_id)
                db.commit()
            except Exception as e:
                print(e)
                traceback.print_exc()
            if post_id != -1: 
                print(category_ids)
                for cid in category_ids:
                    db.execute(
                        'INSERT INTO category_post(category_id, post_id)'
                        'VALUES (?, ?)',
                        (cid, post_id)
                    )
                db.commit()
            else:
                print('insert error')
        return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/admin/updateblog.html?<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form.get('title',default = None)
        body = request.form.get('body', default = None)
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            get_db().execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            get_db().commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/admin/deleteblog.html?<int:id>', methods=('POST',))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    get_db().execute('DELETE FROM post WHERE id = ?', (id,))
    get_db().commit()
    return redirect(url_for('blog.index'))


@bp.route('/view/comment/<post_id>.html', methods=('POST',))
def comment(post_id):
    """
        add comment ,need user login
    """
    if g.user is None:
        return jsonify({'status':False, 'msg': '请先登录' })
    content = request.form.get('content', '')
    
    if not content.strip():
        return jsonify({'status': False, 'msg': '评论内容为空'})
    get_db().execute(
        'INSERT INTO comment(post_id, user_id, content)'
        ' VALUES(?, ?, ?)',
        (post_id, g.user['id'], content))
    get_db().commit()
    
    return jsonify({'status': True, 'msg': 'ok'})

