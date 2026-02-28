from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.item import Item
from app.models.claim import Claim
from app.models.user import User
from functools import wraps

admin = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics."""
    # Get statistics
    total_items = Item.query.count()
    lost_items = Item.query.filter_by(status='lost').count()
    found_items = Item.query.filter_by(status='found').count()
    claimed_items = Item.query.filter_by(status='claimed').count()
    resolved_items = Item.query.filter_by(status='resolved').count()

    pending_claims = Claim.query.filter_by(status='pending').count()
    total_claims = Claim.query.count()
    approved_claims = Claim.query.filter_by(status='approved').count()
    rejected_claims = Claim.query.filter_by(status='rejected').count()

    total_users = User.query.filter_by(role='student').count()

    # Get recent items
    recent_items = Item.query.order_by(Item.created_at.desc()).limit(10).all()

    # Get pending claims with item details
    pending_claims_list = Claim.query.filter_by(status='pending').order_by(Claim.created_at.desc()).all()

    stats = {
        'total_items': total_items,
        'lost_items': lost_items,
        'found_items': found_items,
        'claimed_items': claimed_items,
        'resolved_items': resolved_items,
        'pending_claims': pending_claims,
        'total_claims': total_claims,
        'approved_claims': approved_claims,
        'rejected_claims': rejected_claims,
        'total_users': total_users
    }

    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_items=recent_items,
                         pending_claims=pending_claims_list)


@admin.route('/claims')
@login_required
@admin_required
def manage_claims():
    """Manage all claims."""
    status_filter = request.args.get('status', 'pending')

    if status_filter == 'all':
        claims = Claim.query.order_by(Claim.created_at.desc()).all()
    else:
        claims = Claim.query.filter_by(status=status_filter).order_by(Claim.created_at.desc()).all()

    return render_template('admin/claims.html', claims=claims, status_filter=status_filter)


@admin.route('/claim/<int:claim_id>/approve')
@login_required
@admin_required
def approve_claim(claim_id):
    """Approve a claim."""
    claim = Claim.query.get_or_404(claim_id)

    if claim.status != 'pending':
        flash('This claim has already been processed.', 'warning')
        return redirect(url_for('admin.manage_claims'))

    # Update claim status
    claim.status = 'approved'

    # Update item status
    item = claim.item
    item.status = 'claimed'

    db.session.commit()
    flash(f'Claim approved! The item "{item.title}" has been marked as claimed.', 'success')
    return redirect(url_for('admin.manage_claims'))


@admin.route('/claim/<int:claim_id>/reject')
@login_required
@admin_required
def reject_claim(claim_id):
    """Reject a claim."""
    claim = Claim.query.get_or_404(claim_id)

    if claim.status != 'pending':
        flash('This claim has already been processed.', 'warning')
        return redirect(url_for('admin.manage_claims'))

    # Update claim status
    claim.status = 'rejected'

    db.session.commit()
    flash('Claim rejected.', 'info')
    return redirect(url_for('admin.manage_claims'))


@admin.route('/items')
@login_required
@admin_required
def manage_items():
    """Manage all items."""
    status_filter = request.args.get('status', '')

    if status_filter:
        items = Item.query.filter_by(status=status_filter).order_by(Item.created_at.desc()).all()
    else:
        items = Item.query.order_by(Item.created_at.desc()).all()

    return render_template('admin/items.html', items=items, status_filter=status_filter)


@admin.route('/item/<int:item_id>/status/<string:new_status>')
@login_required
@admin_required
def update_item_status(item_id, new_status):
    """Update item status."""
    item = Item.query.get_or_404(item_id)

    if new_status not in ['lost', 'found', 'claimed', 'resolved']:
        flash('Invalid status.', 'danger')
        return redirect(url_for('admin.manage_items'))

    item.status = new_status
    db.session.commit()
    flash(f'Item status updated to {new_status}.', 'success')
    return redirect(url_for('admin.manage_items'))


@admin.route('/users')
@login_required
@admin_required
def manage_users():
    """Manage users."""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)
