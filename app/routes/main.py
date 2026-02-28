from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Home page."""
    from flask import render_template, redirect, url_for
    from app.models.item import Item

    # Show only active items (lost, found)
    items = Item.query.filter(Item.status.in_(['lost', 'found'])).order_by(Item.created_at.desc()).limit(12).all()
    return render_template('index.html', items=items)


@main.route('/about')
def about():
    """About page."""
    from flask import render_template
    return render_template('about.html')
