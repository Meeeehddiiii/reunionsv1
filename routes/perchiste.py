# routes/perchiste.py

from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Perchiste, db

perchiste_bp = Blueprint('perchiste', __name__, url_prefix='/perchiste')

# Lister les membres de la table Perchiste
@perchiste_bp.route('/perchiste')
def list_perchiste():
    membres = Perchiste.query.all()
    return render_template('perchiste/list.html', membres=membres)

# Ajouter un membre à la table Perchiste
@perchiste_bp.route('/perchiste/add', methods=['GET', 'POST'])
def add_perchiste():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        nouveau_membre = Perchiste(nom=nom, prenom=prenom)
        db.session.add(nouveau_membre)
        db.session.commit()
        flash('Membre ajouté avec succès!')
        return redirect(url_for('perchiste.list_perchiste'))
    return render_template('perchiste/add.html')

# Modifier un membre de la table Perchiste
@perchiste_bp.route('/perchiste/edit/<int:id>', methods=['GET', 'POST'])
def edit_perchiste(id):
    membre = Perchiste.query.get_or_404(id)
    if request.method == 'POST':
        membre.nom = request.form['nom']
        membre.prenom = request.form['prenom']
        db.session.commit()
        flash('Membre modifié avec succès!')
        return redirect(url_for('perchiste.list_perchiste'))
    return render_template('perchiste/edit.html', membre=membre)

# Supprimer un membre de la table Perchiste
@perchiste_bp.route('/perchiste/delete/<int:id>', methods=['POST'])
def delete_perchiste(id):
    membre = Perchiste.query.get_or_404(id)
    db.session.delete(membre)
    db.session.commit()
    flash('Membre supprimé avec succès!')
    return redirect(url_for('perchiste.list_perchiste'))