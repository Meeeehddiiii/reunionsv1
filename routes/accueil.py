# routes/accueil.py

from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Accueil, db

accueil_bp = Blueprint('accueil', __name__, url_prefix='/accueil')

# Lister les membres de la table Accueil
@accueil_bp.route('/accueil')
def list_accueil():
    membres = Accueil.query.all()
    return render_template('accueil/list.html', membres=membres)

# Ajouter un membre à la table Accueil
@accueil_bp.route('/accueil/add', methods=['GET', 'POST'])
def add_accueil():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        nouveau_membre = Accueil(nom=nom, prenom=prenom)
        db.session.add(nouveau_membre)
        db.session.commit()
        flash('Membre ajouté avec succès!')
        return redirect(url_for('accueil.list_accueil'))
    return render_template('accueil/add.html')

# Modifier un membre de la table Accueil
@accueil_bp.route('/accueil/edit/<int:id>', methods=['GET', 'POST'])
def edit_accueil(id):
    membre = Accueil.query.get_or_404(id)
    if request.method == 'POST':
        membre.nom = request.form['nom']
        membre.prenom = request.form['prenom']
        db.session.commit()
        flash('Membre modifié avec succès!')
        return redirect(url_for('accueil.list_accueil'))
    return render_template('accueil/edit.html', membre=membre)

# Supprimer un membre de la table Accueil
@accueil_bp.route('/accueil/delete/<int:id>', methods=['POST'])
def delete_accueil(id):
    membre = Accueil.query.get_or_404(id)
    db.session.delete(membre)
    db.session.commit()
    flash('Membre supprimé avec succès!')
    return redirect(url_for('accueil.list_accueil'))