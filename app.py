from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import json
import os
from functools import wraps
from dotenv import load_dotenv
from pathlib import Path


################################################################################
#                                                                              #
#   ____       _       _     __  __                                           #
#  |  _ \ __ _| |_ ___| |__ |  \/  | __ _ _ __                                #
#  | |_) / _` | __/ __| '_ \| |\/| |/ _` | '_ \                               #
#  |  __/ (_| | || (__| | | | |  | | (_| | |_) |                              #
#  |_|   \__,_|\__\___|_| |_|_|  |_|\__,_| .__/                               #
#                                        |_|                                   #
#                                                                              #
#              Open Source DCIM for SMBs | By Focus                           #
#              https://github.com/focus-on1/patchmap                          #
#                           📜 License:  MIT                                   #
#                   📅 Version:  1.0.0 - October 2025                          #
#                                                                              #
################################################################################


#######################################################
# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration de la clé secrète pour les sessions
app.secret_key = os.getenv('SECRET_KEY', 'votre-cle-secrete-changez-en-production')

# Mot de passe depuis le .env
MOT_DE_PASSE = os.getenv('APP_PASSWORD', 'admin123')

#####################################################


############
#   Vocabulaire / Documentation    #
############
"""
Le décorateur permet de vérifier si une fonction est vraie sans répéter le code dans d'autres fonctions.
Il permet d'avoir un code plus propre. Ici la fonction prend en argument f (donc elle prend la fonction en compte)
pour retourner verification_admin. La fonction decorated_function fait une vérification simple : si l'utilisateur est 
authentifié (donc une session valide) alors il peut accéder au dashboard.

panneau_bandeaux.json : Ce fichier contient donc tous les bandeaux ainsi que les ports qui sont disponibles et non disponibles.
    Ce fichier peut être rempli directement dans la route /admin/panneaux pour administrer donc les panneaux directement 
    (pour la modification exemple quand vous brassez la prise dans un switch et bien vous pouvez donc dire que le port est pris 
    et le mettre en vert).

disposition.json : Ce fichier contiendra donc toutes les positions ainsi que les assignations des prises à une zone spécifique.
    Il vous permettra d'ajouter des imprimantes et des appareils divers et variés.

verifier_conflit_positions : cette fonction permet de verifie si il y'a des conflit de position  identifiet les bandeau les position il ingiore les materiel tiers (imprimante borne wifi etc) et verifie si la position est deja utilise par une autre zone


methode PATCH : un PATCH sert d'instructions pour modifier une ressource, tandis que PUT représente un remplacement complet de la ressource.
donc pour modifier_position_zone nous shoauite modifier uniquement la position x et y d'une zone specifique sans toucher au reste des donnees.
"""


#######################
#     Fonctions Utilitaires       #
#######################

def verification_admin(f):
    """Décorateur pour protéger les routes - Vérifie l'authentification"""
    @wraps(f)
    def fonction_decoree(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return fonction_decoree

# cree un fichier panneau_bandeaux.json par defaut
def creer_fichier_panneau_par_defaut():
    """Crée un fichier panneau_bandeaux.json par défaut si inexistant"""
    donnees_defaut = {
        "metadata": {
            "nom_baie": "Baie Principale",
            "total_panneaux": 0,
            "total_positions": 0,
            "positions_utilisees": 0,
            "positions_libres": 0,
            "taux_utilisation": "0.0%"
        },
        "panneaux": []
    }
    
    # Créer le dossier static s'il n'existe pas
    os.makedirs('./static', exist_ok=True)
    
    # Créer le fichier avec les données par défaut
    with open('./static/panneau_bandeaux.json', 'w', encoding='utf-8') as fichier:
        json.dump(donnees_defaut, fichier, indent=2, ensure_ascii=False)
    
    print(" Fichier panneau_bandeaux.json créé avec succès")
    return donnees_defaut

# charge le fichier 
def charge_fichier_panneau():
    """Charge les données des panneaux avec création automatique si nécessaire"""
    try:
        with open('./static/panneau_bandeaux.json', 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)
            
            # Vérifier que la structure est correcte
            if 'metadata' not in donnees or 'panneaux' not in donnees:
                print("  Structure du fichier incorrecte, réinitialisation...")
                return creer_fichier_panneau_par_defaut()
            
            return donnees
            
    except FileNotFoundError:
        print(" Fichier panneau_bandeaux.json non trouvé, création automatique...")
        return creer_fichier_panneau_par_defaut()
        
    except json.JSONDecodeError:
        print(" Fichier JSON corrompu, réinitialisation...")
        # Sauvegarder l'ancien fichier en backup
        if os.path.exists('./static/panneau_bandeaux.json'):
            nom_backup = f'./static/panneau_bandeaux.json.backup'
            os.rename('./static/panneau_bandeaux.json', nom_backup)
            print(f" Backup créé : {nom_backup}")
        return creer_fichier_panneau_par_defaut()
        
    except Exception as e:
        print(f" Erreur inattendue lors du chargement : {e}")
        return {
            "error": f"Erreur lors du chargement : {str(e)}",
            "metadata": {
                "nom_baie": "Erreur",
                "total_panneaux": 0,
                "total_positions": 0,
                "positions_utilisees": 0,
                "positions_libres": 0,
                "taux_utilisation": "0.0%"
            },
            "panneaux": []
        }

# sauvegarde le fichier panneau_bandeaux.json
def sauvegarder_fichier_panneau(donnees):
    """Sauvegarde les données des panneaux avec gestion d'erreur"""
    try:
        # Créer le dossier static s'il n'existe pas
        os.makedirs('./static', exist_ok=True)
        
        # Sauvegarder avec indentation pour lisibilité
        with open('./static/panneau_bandeaux.json', 'w', encoding='utf-8') as fichier:
            json.dump(donnees, fichier, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f" Erreur lors de la sauvegarde : {e}")
        return False


# charge le fichier disposition.json
def charger_fichier_disposition():
    """Charge les positions des zones sur le plan"""
    try:
        with open('./static/disposition.json', 'r', encoding='utf-8') as fichier:
            return json.load(fichier)
            
    except FileNotFoundError:
        print(" Fichier disposition.json non trouvé, création automatique...")
        disposition_defaut = {"zones": []}
        sauvegarder_fichier_disposition(disposition_defaut)
        return disposition_defaut
        
    except json.JSONDecodeError:
        print(" Fichier disposition.json corrompu, réinitialisation...")
        disposition_defaut = {"zones": []}
        sauvegarder_fichier_disposition(disposition_defaut)
        return disposition_defaut

# sauvegarde le fichier disposition.json
def sauvegarder_fichier_disposition(donnees):
    """Sauvegarde les positions des zones"""
    try:
        os.makedirs('./static', exist_ok=True)
        with open('./static/disposition.json', 'w', encoding='utf-8') as fichier:
            json.dump(donnees, fichier, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f" Erreur lors de la sauvegarde disposition : {e}")
        return False

# verification des conflits de positions
def verifier_conflit_positions(id_panneau, positions, exclure_zone_id=None):
    """Vérifie si des positions sont déjà utilisées par d'autres zones"""
    donnees = charger_fichier_disposition()
    conflits = []
    
    for zone in donnees.get('zones', []):
        # Ignorer les matériels tiers (pas de panneaux)
        if zone.get('materiel'):
            continue
            
        # Ignorer la zone en cours d'édition
        if exclure_zone_id and zone.get('id') == exclure_zone_id:
            continue
            
        # Support pour le nouveau format multi-panneaux
        if zone.get('panneaux') and isinstance(zone['panneaux'], list):
            for panneau in zone['panneaux']:
                if panneau.get('id') == id_panneau:
                    positions_existantes = panneau.get('positions', [])
                    conflits.extend([pos for pos in positions if pos in positions_existantes])
                    
        # Support pour l'ancien format single panneau
        elif zone.get('panneau') and zone['panneau'].get('id') == id_panneau:
            positions_existantes = zone['panneau'].get('positions', [])
            conflits.extend([pos for pos in positions if pos in positions_existantes])
    
    return list(set(conflits))


def recalculer_metadata(donnees):
    """Recalcule les métadonnées globales"""
    """
    
    total_positions = 24 + 12 = 36

    positions_utilisees = 18 + 6 = 24

    positions_libres = 36 - 24 = 12

    taux = (24 / 36 × 100) = 66.7 %
    """
    total_positions = 0
    positions_utilisees = 0
    
    for panneau in donnees.get('panneaux', []):
        if 'statistiques' in panneau:
            total_positions += panneau['statistiques']['total']
            positions_utilisees += panneau['statistiques']['utilise']
    

    
    positions_libres = total_positions - positions_utilisees
    taux = round((positions_utilisees / total_positions * 100), 1) if total_positions > 0 else 0
    
    donnees['metadata'] = {
        "nom_baie": donnees.get('metadata', {}).get('nom_baie', 'Baie Principale'),
        "total_panneaux": len(donnees.get('panneaux', [])),
        "total_positions": total_positions,
        "positions_utilisees": positions_utilisees,
        "positions_libres": positions_libres,
        "taux_utilisation": f"{taux}%"
    }


#######################
#     Routes d'Authentification       #
#######################

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if request.method == 'POST':
        mot_de_passe = request.form.get('password')
        
        if mot_de_passe == MOT_DE_PASSE:
            session['authenticated'] = True
            flash('Connexion réussie !', 'success')
            
            # Rediriger vers la page demandée ou l'accueil
            page_suivante = request.args.get('next')
            return redirect(page_suivante or url_for('index'))
        else:
            flash('Mot de passe incorrect !', 'error')
    
    return render_template('login.html')


# deconexion 
@app.route('/logout')
def logout():
    """Déconnexion"""
    session.pop('authenticated', None)
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('login'))

#verification status
@app.route('/api/auth/status')
def statut_auth():
    """Vérifie le statut d'authentification"""
    return jsonify({
        "authenticated": session.get('authenticated', False)
    })


@app.route('/api/auth/logout', methods=['POST'])
def deconnexion_api():
    """Déconnexion via API"""
    session.pop('authenticated', None)
    return jsonify({"success": True, "message": "Déconnecté"})


#######################
#     Routes Pages Principales       #
#######################

# page principale 
@app.route('/')
@verification_admin
def index():
    """Page principale - plan des zones"""
    return render_template('index.html')

# baie vue
@app.route('/baie')
@verification_admin
def vue_baie():
    """Page de visualisation de la baie"""
    return render_template('baie.html')

# gestion des panneaux 
@app.route('/admin/panneaux')
@verification_admin
def admin_panneaux():
    """Page d'administration des panneaux"""
    return render_template('admin_panneaux.html')


#######################
#     Routes API Panneaux       #
#######################
# Obtient tous les panneaux
@app.route('/api/panneaux')
@verification_admin
def obtenir_panneaux():
    """Retourne les données des panneaux"""
    donnees = charge_fichier_panneau()
    
    # Si c'est une erreur, retourner un code 500 mais avec les données par défaut
    if "error" in donnees and donnees.get("panneaux") is None:
        return jsonify(donnees), 500
    
    return jsonify(donnees)


# Obtient un panneau spécifique par son ID
@app.route('/api/panneau/<int:id_panneau>')
@verification_admin
def obtenir_panneau(id_panneau):
    """Retourne les détails d'un panneau spécifique"""

    donnees = charge_fichier_panneau()
    
    # filtre ici le panneau par son id
    for panneau in donnees.get('panneaux', []):
        if panneau['id'] == id_panneau:
            print (f" Panneau trouvé : {panneau['nom']} (ID: {id_panneau})")
            return jsonify(panneau)
            
    
    return jsonify({"error": "Panneau non trouvé"}), 404

# Création d'un nouveau panneau
@app.route('/api/panneaux', methods=['POST'])
@verification_admin
def creer_panneau():
    """Crée un nouveau panneau"""
    try:
        nouveau_panneau = request.json
        donnees = charge_fichier_panneau()
        
        # Vérifier si on a une erreur
        if "error" in donnees and donnees.get("panneaux") is None:
            return jsonify({"error": "Impossible de charger les données"}), 500
        
        # Générer un ID unique
        ids_existants = [p['id'] for p in donnees.get('panneaux', [])] # pannaux existants
        nouvel_id = max(ids_existants, default=0) + 1 # calcule du prochain id
        nouveau_panneau['id'] = nouvel_id # assignation de l'id au nouveau panneau
        
        # Calculer automatiquement les statistiques
        total_positions = len(nouveau_panneau['positions_totales'])
        positions_utilisees = len(nouveau_panneau['positions_utilisees'])
        positions_libres = total_positions - positions_utilisees
        taux = round((positions_utilisees / total_positions * 100), 1) if total_positions > 0 else 0
        
        nouveau_panneau['positions_libres'] = [
            p for p in nouveau_panneau['positions_totales'] 
            if p not in nouveau_panneau['positions_utilisees']
        ]
        nouveau_panneau['statistiques'] = {
            "total": total_positions,
            "utilise": positions_utilisees,
            "libre": positions_libres,
            "taux_utilisation": f"{taux}%"
        }
        
        donnees['panneaux'].append(nouveau_panneau)
        
        # Recalculer les métadonnées globales
        recalculer_metadata(donnees)
        
        # Sauvegarder avec gestion d'erreur
        if not sauvegarder_fichier_panneau(donnees):
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
        
        return jsonify({"success": True, "panneau": nouveau_panneau})
        
    except Exception as e:
        print(f" Erreur lors de la création du panneau : {e}")
        return jsonify({"error": str(e)}), 400


# Modification d'un panneau existant
@app.route('/api/panneaux/<int:id_panneau>', methods=['PUT'])
@verification_admin
def modifier_panneau(id_panneau):
    """Met à jour un panneau existant"""
    try:
        panneau_modifie = request.json
        donnees = charge_fichier_panneau()
        
        # Vérifier si on a une erreur
        if "error" in donnees and donnees.get("panneaux") is None:
            return jsonify({"error": "Impossible de charger les données"}), 500
        
        for i, panneau in enumerate(donnees.get('panneaux', [])):
            if panneau['id'] == id_panneau:
                # Garder l'ID existant
                panneau_modifie['id'] = id_panneau
                
                # Recalculer les statistiques
                total_positions = len(panneau_modifie['positions_totales'])
                positions_utilisees = len(panneau_modifie['positions_utilisees'])
                positions_libres = total_positions - positions_utilisees
                taux = round((positions_utilisees / total_positions * 100), 1) if total_positions > 0 else 0
                
                panneau_modifie['positions_libres'] = [
                    p for p in panneau_modifie['positions_totales'] 
                    if p not in panneau_modifie['positions_utilisees']
                ]
                panneau_modifie['statistiques'] = {
                    "total": total_positions,
                    "utilise": positions_utilisees,
                    "libre": positions_libres,
                    "taux_utilisation": f"{taux}%"
                }
                
                donnees['panneaux'][i] = panneau_modifie
                
                # Recalculer les métadonnées globales
                recalculer_metadata(donnees)
                
                # Sauvegarder avec gestion d'erreur
                if not sauvegarder_fichier_panneau(donnees):
                    return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
                
                return jsonify({"success": True, "panneau": panneau_modifie})
        
        return jsonify({"error": "Panneau non trouvé"}), 404
        
    except Exception as e:
        print(f" Erreur lors de la modification du panneau : {e}")
        return jsonify({"error": str(e)}), 400


# Suppression d'un panneau
@app.route('/api/panneaux/<int:id_panneau>', methods=['DELETE'])
@verification_admin
def supprimer_panneau(id_panneau):
    """Supprime un panneau"""
    try:
        donnees = charge_fichier_panneau()
        
        # Vérifier si on a une erreur
        if "error" in donnees and donnees.get("panneaux") is None:
            return jsonify({"error": "Impossible de charger les données"}), 500
        
        # Garde tous les panneaux sauf celui dont l’id correspond à id_panneau lui que on veut supp
        donnees['panneaux'] = [p for p in donnees.get('panneaux', []) if p['id'] != id_panneau]
        
        # Recalculer les métadonnées globales
        recalculer_metadata(donnees)
        
        # Sauvegarder avec gestion d'erreur
        if not sauvegarder_fichier_panneau(donnees):
            return jsonify({"error": "Erreur lors de la sauvegarde"}), 500
        
        return jsonify({"success": True})
        
    except Exception as e:
        print(f" Erreur lors de la suppression du panneau : {e}")
        return jsonify({"error": str(e)}), 400


#######################
#     Routes API Disposition       #
#######################

@app.route('/api/disposition')
@verification_admin
def obtenir_disposition():
    """Retourne les positions des zones sur le plan"""
    donnees = charger_fichier_disposition()
    return jsonify(donnees)


@app.route('/api/disposition', methods=['POST'])
@verification_admin
def sauvegarder_disposition():
    """Sauvegarde une nouvelle zone sur le plan"""
    try:
        nouvelle_zone = request.json
        print (nouvelle_zone)
        
        # Si c'est un matériel tiers, pas besoin de valider les positions
        if not nouvelle_zone.get('materiel'):
            # Validation des positions pour les panneaux normaux
            if nouvelle_zone.get('panneaux') and isinstance(nouvelle_zone['panneaux'], list):
                for donnees_panneau in nouvelle_zone['panneaux']:
                    id_panneau = donnees_panneau.get('id')
                    positions = donnees_panneau.get('positions', [])
                    print(positions)
                    
                    conflits = verifier_conflit_positions(id_panneau, positions)
                    if conflits:
                        return jsonify({
                            "error": f"Les positions {conflits} du panneau {id_panneau} sont déjà utilisées par d'autres zones"
                        }), 400
        
        donnees = charger_fichier_disposition()
        
        # Générer un ID unique pour la zone
        nouvel_id = max([zone.get('id', 0) for zone in donnees.get('zones', [])], default=0) + 1
        nouvelle_zone['id'] = nouvel_id
        
        donnees['zones'].append(nouvelle_zone)
        sauvegarder_fichier_disposition(donnees)
        
        return jsonify({"success": True, "zone": nouvelle_zone})
        
    except Exception as e:
        print(f" Erreur lors de la sauvegarde de la disposition : {e}")
        return jsonify({"error": str(e)}), 400


@app.route('/api/disposition/<int:id_zone>', methods=['PUT'])
@verification_admin
def modifier_zone(id_zone):
    """Met à jour une zone existante"""
    try:
        zone_modifiee = request.json
        
        # Validation des positions pour le nouveau format multi-panneaux
        if zone_modifiee.get('panneaux') and isinstance(zone_modifiee['panneaux'], list):
            for donnees_panneau in zone_modifiee['panneaux']:
                id_panneau = donnees_panneau.get('id')
                positions = donnees_panneau.get('positions', [])
                
                conflits = verifier_conflit_positions(id_panneau, positions, exclure_zone_id=id_zone)
                if conflits:
                    return jsonify({
                        "error": f"Les positions {conflits} du panneau {id_panneau} sont déjà utilisées par d'autres zones"
                    }), 400
        
        # Support pour l'ancien format single panneau (compatibilité)
        elif zone_modifiee.get('panneau'):
            id_panneau = zone_modifiee['panneau'].get('id')
            positions = zone_modifiee['panneau'].get('positions', [])
            
            conflits = verifier_conflit_positions(id_panneau, positions, exclure_zone_id=id_zone)
            if conflits:
                return jsonify({
                    "error": f"Les positions {conflits} sont déjà utilisées par d'autres zones"
                }), 400
        
        donnees = charger_fichier_disposition()
        
        # Trouver et mettre à jour la zone
        for i, zone in enumerate(donnees.get('zones', [])):
            if zone.get('id') == id_zone:
                zone_modifiee['id'] = id_zone  # Garder l'ID existant
                donnees['zones'][i] = zone_modifiee
                sauvegarder_fichier_disposition(donnees)
                return jsonify({"success": True, "zone": zone_modifiee})
        
        return jsonify({"error": "Zone non trouvée"}), 404
        
    except Exception as e:
        print(f"❌ Erreur lors de la modification de la zone : {e}")
        return jsonify({"error": str(e)}), 400


#Supprime une Zone
@app.route('/api/disposition/<int:id_zone>', methods=['DELETE'])
@verification_admin
def supprimer_zone(id_zone):
    """Supprime une zone"""
    try:
        donnees = charger_fichier_disposition()
        donnees['zones'] = [zone for zone in donnees.get('zones', []) if zone.get('id') != id_zone]
        sauvegarder_fichier_disposition(donnees)
        
        return jsonify({"success": True})
        
    except Exception as e:
        print(f" Erreur lors de la suppression de la zone : {e}")
        return jsonify({"error": str(e)}), 400


@app.route('/api/disposition/<int:id_zone>/position', methods=['PATCH'])
@verification_admin
def modifier_position_zone(id_zone):
    """Met à jour uniquement la position d'une zone"""
    try:
        donnees_position = request.json
        x = donnees_position.get('x')
        y = donnees_position.get('y')
        

        if x is None or y is None:
            return jsonify({"error": "Coordonnées x et y requises"}), 400
        
        # Validation des coordonnées (0-100%)
        if not (0 <= x <= 100 and 0 <= y <= 100):
            return jsonify({"error": "Les coordonnées doivent être entre 0 et 100"}), 400
        
        donnees = charger_fichier_disposition()
        
        # Trouver et mettre à jour uniquement la position de la zone
        for zone in donnees.get('zones', []):
            if zone.get('id') == id_zone:
                zone['x'] = x
                zone['y'] = y
                sauvegarder_fichier_disposition(donnees)
                return jsonify({"success": True, "zone": zone})
        
        return jsonify({"error": "Zone non trouvée"}), 404
        
    except Exception as e:
        print(f" Erreur lors de la modification de la position : {e}")
        return jsonify({"error": str(e)}), 400


#######################
#     Routes API Statistiques       #
#######################

@app.route('/api/statistics')
@verification_admin
def obtenir_statistiques():
    """Retourne les statistiques globales"""
    donnees = charge_fichier_panneau()
    
    if "error" in donnees:
        return jsonify(donnees), 500
    
    stats = {
        "resume": donnees.get('metadata', {}),
        "details_panneaux": []
    }
    
    for panneau in donnees.get('panneaux', []):
        # Vérifier si c'est un vrai panneau avec des statistiques
        if 'statistiques' in panneau:
            stats["details_panneaux"].append({
                "id": panneau['id'],
                "nom": panneau['nom'],
                "type": panneau['type'],
                "statistiques": panneau['statistiques']
            })
        else:
            # C'est un appareil (imprimante, borne wifi, etc.)
            stats["details_panneaux"].append({
                "id": panneau['id'],
                "nom": panneau['nom'],
                "type": panneau['type'],
                "statistiques": None  # Pas de stats pour les appareils
            })
    
    return jsonify(stats)


#######################
#     Gestionnaires d'Erreurs       #
#######################

@app.errorhandler(401)
def non_autorise(erreur):
    return redirect(url_for('login'))


@app.errorhandler(403)
def interdit(erreur):
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_non_trouvee(erreur):
    return render_template('404.html'), 404 if os.path.exists('templates/404.html') else ("Page non trouvée", 404)


@app.errorhandler(500)
def erreur_serveur(erreur):
    print(f"❌ Erreur serveur : {erreur}")
    return "Erreur serveur interne", 500


#######################
#     Point d'Entrée       #
#######################

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🗺️  PatchMap - Démarrage de l'application")
    print("="*80)
    
    # Créer les dossiers nécessaires
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    print("✅ Dossiers créés : static/ et templates/")
    
    # Vérifier la présence du mot de passe
    if MOT_DE_PASSE == 'admin123':
        print("⚠️  ATTENTION : Vous utilisez le mot de passe par défaut !")
        print("   Créez un fichier .env avec APP_PASSWORD=votre_mot_de_passe")
    
    # Vérifier les fichiers de données
    if not os.path.exists('./static/panneau_bandeaux.json'):
        print("📁 Création du fichier panneau_bandeaux.json...")
        creer_fichier_panneau_par_defaut()
    else:
        print("✅ Fichier panneau_bandeaux.json trouvé")
    
    if not os.path.exists('./static/disposition.json'):
        print("📁 Création du fichier disposition.json...")
        charger_fichier_disposition()
    else:
        print("✅ Fichier disposition.json trouvé")
    
    print("\n🚀 Serveur démarré sur http://localhost:5000")
    print("📝 Connectez-vous avec le mot de passe configuré dans .env")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)