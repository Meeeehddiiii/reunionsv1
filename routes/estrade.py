# routes/estrade.py

from flask import Blueprint, render_template, request, redirect, flash, url_for
from models import Estrade, db

estrade_bp = Blueprint('estrade', __name__, url_prefix='/estrade')

# Lister les membres de la table Estrade
@estrade_bp.route('/estrade')
def list_estrade():
    membres = Estrade.query.all()
    return render_template('estrade/list.html', membres=membres)

# Ajouter un membre à la table Estrade
@estrade_bp.route('/estrade/add', methods=['GET', 'POST'])
def add_estrade():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        nouveau_membre = Estrade(nom=nom, prenom=prenom)
        db.session.add(nouveau_membre)
        db.session.commit()
        flash('Membre ajouté avec succès!')
        return redirect(url_for('estrade.list_estrade'))
    return render_template('estrade/add.html')

# Modifier un membre de la table Estrade
@estrade_bp.route('/estrade/edit/<int:id>', methods=['GET', 'POST'])
def edit_estrade(id):
    membre = Estrade.query.get_or_404(id)
    if request.method == 'POST':
        membre.nom = request.form.get('nom', membre.nom)  # Garde la valeur existante si 'nom' n'est pas présent
        # membre.nom = request.form['nom']
        membre.prenom = request.form.get('prenom', membre.prenom)  # Garde la valeur existante si 'prenom' n'est pas présent
        # membre.prenom = request.form['prenom']
        db.session.commit()
        flash('Membre modifié avec succès!')
        return redirect(url_for('estrade.list_estrade'))
    return render_template('estrade/edit.html', membre=membre)

# Supprimer un membre de la table Estrade
@estrade_bp.route('/estrade/delete/<int:id>', methods=['POST'])
def delete_estrade(id):
    membre = Estrade.query.get_or_404(id)
    db.session.delete(membre)
    db.session.commit()
    flash('Membre supprimé avec succès!')
    return redirect(url_for('estrade.list_estrade'))