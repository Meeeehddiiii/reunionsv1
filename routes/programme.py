# routes/programme.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from models import db, Accueil, Estrade, Sono, Perchiste, Programme
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Affiche les logs de niveau DEBUG et supérieur
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        # Récupération et conversion de la date
        date_planning_str = request.form.get('datePlanning')
        try:
            planning_date = datetime.strptime(date_planning_str, '%Y-%m-%d').date() if date_planning_str else date.today()
        except ValueError:
            flash("La date n'est pas au format correct (YYYY-MM-DD).")
            return redirect(url_for('programme.generate_programme'))
        
        # Récupération du nombre de perchistes souhaité (2 ou 4)
        nb_perchistes_str = request.form.get('nbPerchistes')
        try:
            nb_perchistes = int(nb_perchistes_str) if nb_perchistes_str else 4
            if nb_perchistes not in (2, 4):
                nb_perchistes = 4
        except ValueError:
            nb_perchistes = 4

        # Récupération des couples indisponibles et normalisation
        indisponibles_str = request.form.get('indisponibles', '')
        # On normalise ici en minuscules et en enlevant les espaces superflus
        indisponibles = {couple.strip().lower() for couple in indisponibles_str.split(',') if couple.strip()}
        logger.debug("Indisponibles normalisés : %s", indisponibles)

        total_prog = Programme.query.count()  # Nombre de programmes déjà générés

        # Récupérer et trier les membres pour chaque catégorie
        accueil_members = sorted(Accueil.query.all(), key=lambda m: (m.nom, m.prenom))
        sono_members = sorted(Sono.query.all(), key=lambda m: (m.nom, m.prenom))
        perchiste_members = sorted(Perchiste.query.all(), key=lambda m: (m.nom, m.prenom))

        # Un ensemble global pour éviter qu'un même couple apparaisse dans le programme entier
        used_global = set()

        def select_member_category(members, offset, role_index=0, indisponibles=set()):
            """
            Sélectionne un membre dans 'members' en parcourant la liste circulairement,
            en s'assurant que le couple "Nom Prenom" (normalisé en minuscules) n'est ni déjà
            utilisé (dans used_global) ni présent dans l'ensemble 'indisponibles'.
            
            Si aucun candidat n'est trouvé, retourne quand même celui à l'offset + role_index.
            """
            n = len(members)
            for i in range(n):
                index = (offset + role_index + i) % n
                candidate_raw = f"{members[index].nom.strip()} {members[index].prenom.strip()}"
                candidate_normalized = candidate_raw.lower()
                logger.debug("Vérification du candidat (role_index=%d): %s", role_index, candidate_normalized)
                
                if candidate_normalized in indisponibles:
                    logger.debug("Le candidat %s est indisponible.", candidate_normalized)
                    continue
                if candidate_normalized in used_global:
                    logger.debug("Le candidat %s est déjà utilisé.", candidate_normalized)
                    continue
                used_global.add(candidate_normalized)
                logger.debug("Candidat sélectionné pour role_index %d: %s", role_index, candidate_raw)
                return candidate_raw
            # Aucun candidat n'est trouvé, on retourne le candidat à l'offset + role_index (même si déjà utilisé)
            logger.debug("Aucun candidat disponible pour role_index %d.", role_index)
            candidate_raw = f"{members[(offset + role_index) % n].nom.strip()} {members[(offset + role_index) % n].prenom.strip()}"
            logger.debug("Retour fallback pour role_index %d: %s", role_index, candidate_raw)
            return candidate_raw

        # Calcul des offsets pour chaque catégorie (basé sur le nombre de programmes déjà générés)
        offset_accueil = total_prog % len(accueil_members) if accueil_members else 0
        offset_sono = total_prog % len(sono_members) if sono_members else 0
        offset_perchiste = total_prog % len(perchiste_members) if perchiste_members else 0

        # Pour la catégorie Sono : on génère 4 rôles (exemple : zoom, audio, video, estrade)
        zoom = select_member_category(sono_members, offset_sono, 0, indisponibles)
        audio = select_member_category(sono_members, offset_sono, 1, indisponibles)
        video = select_member_category(sono_members, offset_sono, 2, indisponibles)
        estrade = select_member_category(sono_members, offset_sono, 3, indisponibles)

        # Pour la catégorie Accueil : on génère 3 rôles (exemple : parking, entree, auditorium)
        parking = select_member_category(accueil_members, offset_accueil, 0, indisponibles)
        entree = select_member_category(accueil_members, offset_accueil, 1, indisponibles)
        auditorium = select_member_category(accueil_members, offset_accueil, 2, indisponibles)

        # Pour la catégorie Perchiste : générer nb_perchistes rôles
        perchiste_list = []
        for role_index in range(nb_perchistes):
            candidate = select_member_category(perchiste_members, offset_perchiste, role_index, indisponibles)
            perchiste_list.append(candidate)
        if nb_perchistes == 2:
            perchiste1, perchiste2 = perchiste_list
            perchiste3 = perchiste4 = None
        else:
            perchiste1, perchiste2, perchiste3, perchiste4 = perchiste_list

        # Optionnel : obtenir le prochain candidate_id via votre fonction de rotation
        candidate_id = get_next_candidate(total_candidates=10)  # Votre fonction doit être définie ailleurs

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
            candidate_id = candidate_id
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