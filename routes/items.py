from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.item import Item
import os
import uuid

items = Blueprint('items', __name__)

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(3, 200)])
    description = TextAreaField('Description')
    category = SelectField('Category', choices=[
        ('ID Cards', 'ID Cards'), ('Electronics', 'Electronics'),
        ('Books', 'Books'), ('Keys', 'Keys'), ('Other', 'Other')
    ])
    location = StringField('Location', validators=[DataRequired()])
    date_lost_found = DateField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('lost', 'Lost'), ('found', 'Found')])
    image = FileField('Image')
    submit = SubmitField('Submit')

@items.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = ItemForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            ext = form.image.data.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            form.image.data.save(f"static/uploads/{filename}")
        
        item = Item(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            location=form.location.data,
            date_lost_found=form.date_lost_found.data,
            status=form.status.data,
            image_filename=filename
        )
        db.session.add(item)
        db.session.commit()
        flash('Item reported!')
        return redirect(url_for('items.index'))
    return render_template('items/report.html', form=form)

@items.route('/')
def index():
    items = Item.query.filter(Item.status.in_(['lost', 'found'])).all()
    return render_template('items/index.html', items=items)

@items.route('/item/<int:item_id>')
def detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('items/detail.html', item=item)
