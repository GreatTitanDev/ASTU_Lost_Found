from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
from app import db
from app.models.item import Item
from app.models.claim import Claim
from functools import wraps

items = Blueprint('items', __name__)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


class ItemForm(FlaskForm):
    """Form for creating/editing items."""
    title = StringField('Item Title', validators=[
        DataRequired(),
        Length(min=3, max=200, message='Title must be between 3 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=1000, message='Description must not exceed 1000 characters')
    ])
    category = SelectField('Category', choices=[(c, c) for c in Item.CATEGORIES], validators=[DataRequired()])
    location = StringField('Location', validators=[
        DataRequired(),
        Length(max=200, message='Location must not exceed 200 characters')
    ])
    date_lost_found = DateField('Date Lost/Found', validators=[DataRequired()])
    status = SelectField('Status', choices=[('lost', 'Lost'), ('found', 'Found')], validators=[DataRequired()])
    image = FileField('Item Image', validators=[])
    submit = SubmitField('Submit')


class ClaimForm(FlaskForm):
    """Form for claiming an item."""
    proof_description = TextAreaField('Proof of Ownership', validators=[
        DataRequired(),
        Length(min=10, message='Please provide at least 10 characters describing the item')
    ])
    submit = SubmitField('Submit Claim')


@items.route('/report', methods=['GET', 'POST'])
@login_required
def report_item():
    """Route to report a lost or found item."""
    form = ItemForm()
    if form.validate_on_submit():
        # Handle file upload
        image_filename = None
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                # Generate unique filename to prevent overwrites and security issues
                ext = file.filename.rsplit('.', 1)[1].lower()
                image_filename = f"{uuid.uuid4()}.{ext}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))
            else:
                flash('Invalid file type. Allowed types: jpg, jpeg, png, gif', 'danger')
                return render_template('items/report.html', form=form)

        # Create new item
        item = Item(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            location=form.location.data,
            date_lost_found=form.date_lost_found.data,
            status=form.status.data,
            image_filename=image_filename
        )
        db.session.add(item)
        db.session.commit()
        flash('Item reported successfully!', 'success')
        return redirect(url_for('items.my_items'))

    return render_template('items/report.html', form=form)


@items.route('/my-items')
@login_required
def my_items():
    """Route to view user's reported items."""
    user_items = Item.query.filter_by(user_id=current_user.id).order_by(Item.created_at.desc()).all()
    return render_template('items/my_items.html', items=user_items)


@items.route('/search')
def search():
    """Route to search and filter items."""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    status = request.args.get('status', '')

    # Build query
    items_query = Item.query.filter(Item.status.in_(['lost', 'found']))

    if query:
        items_query = items_query.filter(
            (Item.title.ilike(f'%{query}%')) |
            (Item.description.ilike(f'%{query}%'))
        )

    if category:
        items_query = items_query.filter_by(category=category)

    if status:
        items_query = items_query.filter_by(status=status)

    items = items_query.order_by(Item.created_at.desc()).all()

    return render_template('items/search.html', items=items, query=query, category=category, status=status)


@items.route('/item/<int:item_id>')
def item_detail(item_id):
    """Route to view item details."""
    item = Item.query.get_or_404(item_id)

    # Check if current user has already claimed this item
    user_claim = None
    if current_user.is_authenticated:
        user_claim = Claim.query.filter_by(item_id=item_id, claimant_id=current_user.id).first()

    # Check if user is the reporter
    is_reporter = current_user.is_authenticated and current_user.id == item.user_id

    return render_template('items/detail.html', item=item, user_claim=user_claim, is_reporter=is_reporter)


@items.route('/item/<int:item_id>/claim', methods=['GET', 'POST'])
@login_required
def claim_item(item_id):
    """Route to claim an item."""
    item = Item.query.get_or_404(item_id)

    # Check if user is the reporter
    if item.user_id == current_user.id:
        flash('You cannot claim your own item.', 'danger')
        return redirect(url_for('items.item_detail', item_id=item_id))

    # Check if already claimed
    existing_claim = Claim.query.filter_by(item_id=item_id, claimant_id=current_user.id).first()
    if existing_claim:
        flash('You have already submitted a claim for this item.', 'warning')
        return redirect(url_for('items.item_detail', item_id=item_id))

    form = ClaimForm()
    if form.validate_on_submit():
        claim = Claim(
            item_id=item_id,
            claimant_id=current_user.id,
            proof_description=form.proof_description.data
        )
        db.session.add(claim)
        db.session.commit()
        flash('Claim submitted successfully! Wait for admin approval.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('items/claim.html', form=form, item=item)


@items.route('/item/<int:item_id>/delete')
@login_required
def delete_item(item_id):
    """Route to delete an item."""
    item = Item.query.get_or_404(item_id)

    # Check if user is the reporter or admin
    if item.user_id != current_user.id and not current_user.is_admin():
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('items.item_detail', item_id=item_id))

    # Delete associated image if exists
    if item.image_filename:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], item.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('items.my_items'))
