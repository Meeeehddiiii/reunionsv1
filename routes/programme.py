# routes/programme.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from models import db, Accueil, Estrade, Sono, Perchiste, Programme

programme_bp = Blueprint('programme', __name__, url_prefix='/programme')

def get_next_candidate(total_candidates=10):
    # Ensemble de tous les candidats possibles (de 1 à total_candidates)
    all_candidates = set(range(1, total_candidates + 1))
    
    # Récupérer tous les candidate_id déjà utilisés dans la table Programme
    used_candidates = {
        programme.candidate_id
        for programme in Programme.query.all()
        if programme.candidate_id is not None
    }
    
    # Déterminer les candidats disponibles
    available_candidates = all_candidates - used_candidates
    
    # Si tous les identifiants ont été utilisés, réinitialiser la rotation
    if not available_candidates:
        available_candidates = all_candidates
    
    # Retourner le candidat disponible le plus petit (ou appliquer une autre logique de sélection)
    return min(available_candidates)

@programme_bp.route('/generate', methods=['GET', 'POST'])
def generate_programme():
    if request.method == 'POST':
        date_planning_str = request.form.get('datePlanning')
        try:
            planning_date = datetime.strptime(date_planning_str, '%Y-%m-%d').date() if date_planning_str else date.today()
        except ValueError:
            flash("La date n'est pas au format correct (YYYY-MM-DD).")
            return redirect(url_for('programme.generate_programme'))

        total_prog = Programme.query.count()  # Nombre de programmes déjà générés

        # Récupérer et trier les membres pour avoir un ordre fixe
        accueil_members = sorted(Accueil.query.all(), key=lambda m: (m.nom, m.prenom))
        # estrade_members = sorted(Estrade.query.all(), key=lambda m: (m.nom, m.prenom))
        sono_members = sorted(Sono.query.all(), key=lambda m: (m.nom, m.prenom))
        perchiste_members = sorted(Perchiste.query.all(), key=lambda m: (m.nom, m.prenom))

        # Ensemble global pour éviter la duplication d'un même couple dans un programme
        used = set()

        # Fonction d'aide : pour une liste de membres donnée, parcourt la liste en partant d'un offset
        # et renvoie le premier couple "Nom Prénom" qui n'est pas déjà utilisé.
        def select_member_category(members, used, offset):
            n = len(members)
            for i in range(n):
                index = (offset + i) % n
                candidate = f"{members[index].nom} {members[index].prenom}"
                if candidate not in used:
                    used.add(candidate)
                    return candidate
            # Si tous les membres sont déjà utilisés, on retourne celui à l'offset (et on l'ajoute quand même)
            candidate = f"{members[offset].nom} {members[offset].prenom}"
            used.add(candidate)
            return candidate

        def select_member_with_role_offset(members, used, offset, role_index):
            """
            Sélectionne un membre unique dans une liste en démarrant à l'offset + role_index.
            Cela permet d'avoir un décalage différent pour chaque rôle au sein de la même catégorie.
            """
            n = len(members)
            for i in range(n):
                index = (offset + role_index + i) % n
                candidate = f"{members[index].nom} {members[index].prenom}"
                if candidate not in used:
                    used.add(candidate)
                    return candidate
            # Si tous les membres sont déjà utilisés, retourne celui à l'offset (même si cela génère une duplication)
            candidate = f"{members[offset].nom} {members[offset].prenom}"
            used.add(candidate)
            return candidate
        
        # Calcul des offsets pour chaque catégorie
        offset_accueil = total_prog % len(accueil_members) if accueil_members else 0
        # offset_estrade = total_prog % len(estrade_members) if estrade_members else 0
        offset_sono = total_prog % len(sono_members) if sono_members else 0
        offset_perchiste = total_prog % len(perchiste_members) if perchiste_members else 0

        # Pour la catégorie Sono, on affecte 4 rôles (zoom, audio, video et estrade)
        zoom    = select_member_category(sono_members, used, offset_sono) if sono_members else None
        audio   = select_member_category(sono_members, used, offset_sono) if sono_members else None
        video   = select_member_category(sono_members, used, offset_sono) if sono_members else None
        estrade = select_member_category(sono_members, used, offset_sono) if sono_members else None

        # Pour la catégorie Accueil, on affecte 3 rôles (parking, entrée, auditorium)
        parking    = select_member_category(accueil_members, used, offset_accueil)
        entree     = select_member_category(accueil_members, used, offset_accueil)
        auditorium = select_member_category(accueil_members, used, offset_accueil)

        # Calcul de l'offset pour Perchiste
        offset_perchiste = total_prog % len(perchiste_members) if perchiste_members else 0

        # Sélection pour les 4 rôles perchiste en utilisant un décalage différent pour chacun
        perchiste1 = select_member_with_role_offset(perchiste_members, used, offset_perchiste, 0)
        perchiste2 = select_member_with_role_offset(perchiste_members, used, offset_perchiste, 1)
        perchiste3 = select_member_with_role_offset(perchiste_members, used, offset_perchiste, 2)
        perchiste4 = select_member_with_role_offset(perchiste_members, used, offset_perchiste, 3)       

        # Optionnel : obtenir le prochain candidate_id via votre fonction de rotation
        candidate = get_next_candidate(total_candidates=10)  # Assurez-vous que cette fonction est définie

        new_programme = Programme(
            datePlanning = planning_date,
            zoom = zoom,
            audio = audio,
            video = video,
            estrade = estrade,
            parking = parking,
            entree = entree,
            auditorium = auditorium,
            perchiste1 = perchiste1,
            perchiste2 = perchiste2,
            perchiste3 = perchiste3,
            perchiste4 = perchiste4,
            candidate_id = candidate
        )

        db.session.add(new_programme)
        db.session.commit()

        flash("Programme généré avec succès!")
        return redirect(url_for('programme.list_programme'))

    return render_template('programme/generate.html')

@programme_bp.route('/')
def list_programme():
    programmes = Programme.query.order_by(Programme.datePlanning.desc()).all()
    return render_template('programme/list.html', programmes=programmes)

@programme_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_programme(id):
    programme = Programme.query.get_or_404(id)
    if request.method == 'POST':
        # Mettez à jour les champs du programme avec les données du formulaire
        programme.datePlanning = request.form.get('datePlanning', programme.datePlanning)
        programme.zoom = request.form.get('zoom', programme.zoom)
        programme.audio = request.form.get('audio', programme.audio)
        programme.video = request.form.get('video', programme.video)
        programme.estrade = request.form.get('estrade', programme.estrade)
        programme.parking = request.form.get('parking', programme.parking)
        programme.entree = request.form.get('entree', programme.entree)
        programme.auditorium = request.form.get('auditorium', programme.auditorium)
        programme.perchiste1 = request.form.get('perchiste1', programme.perchiste1)
        programme.perchiste2 = request.form.get('perchiste2', programme.perchiste2)
        programme.perchiste3 = request.form.get('perchiste3', programme.perchiste3)
        programme.perchiste4 = request.form.get('perchiste4', programme.perchiste4)
        
        db.session.commit()
        flash("Programme modifié avec succès !", "success")
        return redirect(url_for('programme.list_programme'))
    return render_template('programme/edit.html', programme=programme)

@programme_bp.route('/delete/<int:id>', methods=['POST'])
def delete_programme(id):
    programme = Programme.query.get_or_404(id)
    db.session.delete(programme)
    db.session.commit()
    flash("Programme supprimé avec succès !", "success")
    return redirect(url_for('programme.list_programme'))