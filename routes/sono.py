# routes/sono.py

from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Sono, db

sono_bp = Blueprint('sono', __name__, url_prefix='/sono')

# Lister les membres de la table Sono
@sono_bp.route('/sono')
def list_sono():
    membres = Sono.query.all()
    return render_template('sono/list.html', membres=membres)

# Ajouter un membre à la table Sono
@sono_bp.route('sono/add', methods=['GET', 'POST'])
def add_sono():
    flash("JE SUIS ICI")
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        nouveau = Sono(nom=nom, prenom=prenom)
        db.session.add(nouveau)
        db.session.commit()
        flash("Membre Sono ajouté avec succès!")
        return redirect(url_for('sono.list_sono'))
    return render_template('sono/add.html')

# Modifier un membre de la table Sono
@sono_bp.route('/sono/edit/<int:id>', methods=['GET', 'POST'])
def edit_sono(id):
    membre = Sono.query.get_or_404(id)
    if request.method == 'POST':
        membre.nom = request.form['nom']
        membre.prenom = request.form['prenom']
        db.session.commit()
        flash('Membre modifié avec succès!')
        return redirect(url_for('sono.list_sono'))
    return render_template('sono/edit.html', membre=membre)

# Supprimer un membre de la table Sono
@sono_bp.route('/sono/delete/<int:id>', methods=['POST'])
def delete_sono(id):
    membre = Sono.query.get_or_404(id)
    db.session.delete(membre)
    db.session.commit()
    flash('Membre supprimé avec succès!')
    return redirect(url_for('sono.list_sono'))