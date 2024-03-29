from flask import abort, request, redirect, render_template, url_for, flash
from flask_login import login_required, current_user

from .forms import PitchForm, CommentForm
from . import main
from ..models import Dislike, Pitch, Comment, Like
from .. import db


# Views
@main.route('/')
@main.route('/home')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.query.all()
    # pitches = []
    return render_template('index.html', pitches=pitches, title='Pitch App!')


# @main.route('/db')
# def create_db():
#     db.create_all()

#     return "Data Bases Created"


@main.route('/general')
def general():
    pitches = Pitch.query.all()
    pitch = Pitch.query.filter_by(category='General').all()
    return render_template('general.html', pitch=pitch, title='General Pitches', pitches=pitches)


@main.route('/pickuplines')
def pickuplines():
    pitches = Pitch.query.all()
    pitch = Pitch.query.filter_by(category='Pickuplines').all()
    return render_template('pickuplines.html', pitch=pitch, title='Pickupline Pitches', pitches=pitches)


@main.route('/quotes')
def quotes():
    pitches = Pitch.query.all()
    pitch = Pitch.query.filter_by(category='Quotes').all()
    return render_template('quotes.html', pitch=pitch, title='Quote Pitches', pitches=pitches)


@main.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def pitch():
    form = PitchForm()
    if form.validate_on_submit():
        pitch = Pitch(category=form.category.data,
                      content=form.content.data, author=current_user)
        db.session.add(pitch)
        db.session.commit()
        flash('Pitch added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template("pitch.html", title='Pitch-App | New Pitch', form=form)


@main.route('/comments/<int:pitch_id>', methods=['POST', 'GET'])
@login_required
def comment(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    form = CommentForm()
    allComments = Comment.query.filter_by(pitch_id=pitch_id).all()
    if form.validate_on_submit():
        postedComment = Comment(comment=form.comment.data,
                                user_id=current_user.id, pitch_id=pitch_id)
        pitch_id = pitch_id
        db.session.add(postedComment)
        db.session.commit()
        flash('Comment added successfully')

        return redirect(url_for('main.comment', pitch_id=pitch_id))

    return render_template("comment.html", pitch=pitch, title='React to Pitch!', form=form, allComments=allComments)


@main.route('/like/<pitch_id>/', methods=['GET'])
@login_required
def like(pitch_id):
    pitch = Pitch.query.filter_by(id=pitch_id)
    like = Like.query.filter_by(
        author=current_user.id, pitch_id=pitch_id).first()
    dislike = Dislike.query.filter_by(
        author=current_user.id, pitch_id=pitch_id).first()

    if not pitch:
        flash('Pitch not found', category='error')
    elif like:
        return redirect(url_for('main.index', pitch_id=pitch_id))
    else:
        like = Like(author=current_user.id, pitch_id=pitch_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/dislike/<pitch_id>/', methods=['GET'])
@login_required
def dislike(pitch_id):
    pitch = Pitch.query.filter_by(id=pitch_id)
    dislike = Dislike.query.filter_by(
        author=current_user.id, pitch_id=pitch_id).first()
    l = Like.query.filter_by(author=current_user.id, pitch_id=pitch_id).first()

    if not pitch:
        flash('Pitch not found', category='error')
    elif dislike:
        return redirect(url_for('main.index', pitch_id=pitch_id))
    else:

        d = Dislike(author=current_user.id, pitch_id=pitch_id)
        db.session.add(d)
        db.session.commit()

    return redirect(url_for('main.index'))


# Delete comment
@main.route('/delete/comment/<comment_id>')
@login_required
def deleteComment(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()

    if not comment:
        flash('Comment not found', category='error')
    elif current_user.id != comment.user.id and current_user.id != pitch.author.id:
        flash('YOu are not authorized to delete this comment', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/delete/pitch/<pitch_id>')
@login_required
def deletePitch(pitch_id):
    pitch = Pitch.query.filter(Pitch.id == pitch_id).first()

    if not pitch:
        flash('Pitch not found', category='error')
    elif current_user.id != pitch.author.id:
        flash('You are not authorized to delete this pitch', category='error')
    else:
        db.session.delete(pitch)
        db.session.commit()
    return redirect(url_for('main.index'))
