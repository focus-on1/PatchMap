# 🗺️ PatchMap - Gestion Visuelle des Panneaux de Brassage

<div align="center">

<img src="https://i.ibb.co/VPWNjy1/c3e11d5d-f87e-4303-8d40-b2092e492403.png" alt="PatchMap Logo" width="150"/>


**Solution DCIM Open Source pour PME - Gestion intelligente de votre infrastructure réseau**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/focus-on1/patchmap)

[Installation](#-installation) • [Fonctionnalités](#-fonctionnalités) • [Utilisation](#-utilisation) • [Déploiement](#-déploiement-sur-vercel) • [Documentation](#-documentation)

</div>

---

## 📖 À propos du projet

**PatchMap** est une application web moderne de gestion des panneaux de brassage (patch panels) développée dans le cadre d'une mission professionnelle à Lyon. Ce projet m'a permis d'acquérir des compétences solides en développement full-stack, en gestion d'infrastructure IT et en conception d'interfaces utilisateur intuitives.

### 🎯 Contexte

Développé pour répondre aux besoins réels d'une entreprise lyonnaise, PatchMap permet de visualiser et gérer l'infrastructure réseau de manière graphique et interactive. L'application facilite le suivi des connexions, l'attribution des ports et la documentation de l'infrastructure réseau.

### 🏆 Compétences acquises

- **Développement Backend** : Architecture Flask, API RESTful, gestion de sessions
- **Frontend Moderne** : JavaScript vanilla, manipulation DOM, interfaces drag & drop
- **Gestion de Données** : JSON, persistance de données, validation
- **Infrastructure IT** : Compréhension des panneaux de brassage, câblage structuré
- **Sécurité** : Authentification, protection des routes, gestion des sessions
- **DevOps** : Déploiement local et cloud (Vercel), gestion d'environnements

---

## ✨ Fonctionnalités

### 🔐 Authentification Sécurisée
- Système de connexion par mot de passe
- Protection de toutes les routes administratives
- Gestion des sessions Flask
- Interface de login moderne et responsive

### 📊 Dashboard Interactif
- Vue d'ensemble de l'infrastructure réseau
- Statistiques en temps réel (taux d'utilisation, ports disponibles)
- Cartographie visuelle des panneaux de brassage
- Interface drag & drop pour positionner les équipements

### 🔌 Gestion des Panneaux
- Création et édition de panneaux de brassage (24 ou 48 ports)
- Attribution individuelle des ports (libre/occupé)
- Codes couleur pour visualisation rapide
- Informations détaillées par port

### 🗺️ Plan Interactif
- Positionnement graphique des zones de travail
- Liaison automatique zones ↔ panneaux ↔ ports
- Support multi-panneaux par zone
- Gestion d'équipements tiers (imprimantes, bornes WiFi)

### 📈 Statistiques Avancées
- Taux d'occupation global
- Statistiques par panneau
- Export des données (JSON)
- Historique des modifications

---

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour cloner le repository)

### Installation Locale

1. **Cloner le repository**
```bash
git clone https://github.com/focus-on1/patchmap.git
cd patchmap
```

2. **Créer un environnement virtuel** (recommandé)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine du projet :
```env
SECRET_KEY=votre-cle-secrete-super-securisee
APP_PASSWORD=votre-mot-de-passe-admin
```

> ⚠️ **Important** : Changez ces valeurs par défaut en production !

5. **Créer l'image de bannière** (optionnel)

Placez une image `patchmap-banner.png` dans le dossier `static/` pour personnaliser l'interface.

6. **Lancer l'application**
```bash
python app.py
```

L'application sera accessible sur : **http://localhost:5000**

---

## 📁 Structure du Projet

```
patchmap/
│
├── app.py                          # Application Flask principale
├── requirements.txt                # Dépendances Python
├── .env                           # Variables d'environnement (à créer)
├── .gitignore                     # Fichiers à ignorer par Git
├── README.md                      # Documentation
│
├── static/                        # Fichiers statiques (auto-générés)
│   ├── panneau_bandeaux.json     # Données des panneaux (créé automatiquement)
│   ├── disposition.json          # Positions des zones (créé automatiquement)
│   └── patchmap-banner.png       # Image de bannière (optionnel)
│
└── templates/                     # Templates HTML
    ├── index.html                # Dashboard principal
    ├── login.html                # Page de connexion
    ├── admin_panneaux.html       # Administration des panneaux
    └── baie.html                 # Vue détaillée de la baie
```

---

## 💡 Utilisation

### Premier Lancement

Au premier démarrage, l'application crée automatiquement :
- Le dossier `static/` pour les données
- `panneau_bandeaux.json` avec une structure vide
- `disposition.json` pour les positions des zones

### Workflow Typique

1. **Connexion**
   - Accédez à `/login`
   - Entrez le mot de passe configuré dans `.env`

2. **Création des Panneaux**
   - Allez dans "Administration des Panneaux"
   - Créez vos panneaux (24 ou 48 ports)
   - Nommez-les selon votre convention

3. **Attribution des Ports**
   - Cliquez sur un panneau
   - Marquez les ports utilisés/libres
   - Ajoutez des notes si nécessaire

4. **Positionnement sur le Plan**
   - Accédez au dashboard principal
   - Utilisez le drag & drop pour positionner les zones
   - Liez les zones aux panneaux correspondants

5. **Suivi et Maintenance**
   - Consultez les statistiques
   - Mettez à jour l'état des ports
   - Exportez les données si besoin

---

## 🌐 Déploiement sur Vercel

### ⚠️ Limitations Importantes

**PatchMap sur Vercel fonctionne en MODE LECTURE SEULE (Static)**

Les fichiers JSON sont générés lors du build et ne peuvent pas être modifiés directement sur Vercel. Pour mettre à jour les données :

1. Modifiez les fichiers localement
2. Committez les changements
3. Repoussez sur GitHub
4. Vercel redéploiera automatiquement

### Configuration Vercel

1. **Créer un fichier `vercel.json`**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "SECRET_KEY": "@secret_key",
    "APP_PASSWORD": "@app_password"
  }
}
```

2. **Créer `requirements.txt`**
```txt
Flask==3.0.0
python-dotenv==1.0.0
```

3. **Déploiement**

```bash
# Installer Vercel CLI
npm i -g vercel

# Se connecter
vercel login

# Déployer
vercel

# Configurer les secrets
vercel secrets add secret_key "votre-cle-secrete"
vercel secrets add app_password "votre-mot-de-passe"
```

4. **Configuration des Variables d'Environnement**

Dans le dashboard Vercel :
- Ajoutez `SECRET_KEY`
- Ajoutez `APP_PASSWORD`
- Redéployez l'application

### Partage avec l'Équipe IT

Une fois déployé, partagez l'URL Vercel avec votre équipe :
```
https://votre-projet.vercel.app
```

> 💡 **Astuce** : Créez un document partagé avec :
> - L'URL de l'application
> - Le mot de passe d'accès
> - La procédure pour demander des modifications

---

## 🔒 Sécurité

### Bonnes Pratiques

- ✅ Changez toujours le mot de passe par défaut
- ✅ Utilisez une `SECRET_KEY` forte et unique
- ✅ Ne committez jamais le fichier `.env`
- ✅ Limitez l'accès aux personnes autorisées
- ✅ Effectuez des sauvegardes régulières des fichiers JSON

### Fichiers Sensibles

Le `.gitignore` inclut :
```gitignore
.env
*.pyc
__pycache__/
instance/
.venv/
venv/
*.log
```

---

## 📊 Structure des Données

### panneau_bandeaux.json

```json
{
  "metadata": {
    "nom_baie": "Baie Principale",
    "total_panneaux": 3,
    "total_positions": 72,
    "positions_utilisees": 45,
    "positions_libres": 27,
    "taux_utilisation": "62.5%"
  },
  "panneaux": [
    {
      "id": 1,
      "nom": "Panel-A-01",
      "type": "24-ports",
      "ports": [...]
    }
  ]
}
```

### disposition.json

```json
{
  "zones": [
    {
      "id": 1,
      "nom": "Bureau Direction",
      "x": 25,
      "y": 30,
      "panneaux": [
        {
          "id": 1,
          "positions": [1, 2, 3, 4]
        }
      ]
    }
  ]
}
```

---

## 🛠️ Technologies Utilisées

### Backend
- **Flask 3.0** - Framework web Python
- **Python 3.8+** - Langage de programmation
- **python-dotenv** - Gestion des variables d'environnement

### Frontend
- **HTML5 / CSS3** - Structure et style
- **JavaScript ES6** - Interactivité
- **Fetch API** - Communication avec le backend

### Déploiement
- **Vercel** - Hébergement cloud
- **Git** - Contrôle de version

---

## 🐛 Dépannage

### L'application ne démarre pas

```bash
# Vérifier les dépendances
pip install -r requirements.txt

# Vérifier la version de Python
python --version  # Doit être 3.8+

# Vérifier les permissions
chmod +x app.py  # Linux/MacOS uniquement
```

### Erreur d'authentification

- Vérifiez que le fichier `.env` existe
- Vérifiez que `APP_PASSWORD` est correctement défini
- Supprimez les espaces avant/après le mot de passe

### Fichiers JSON corrompus

L'application crée automatiquement des backups :
```bash
ls static/*.backup  # Liste des backups disponibles
```

Pour restaurer :
```bash
cp static/panneau_bandeaux.json.backup static/panneau_bandeaux.json
```

---

## 🗺️ Roadmap

### Version 1.x (MVP - Actuelle)
- ✅ Authentification basique
- ✅ Gestion des panneaux
- ✅ Plan interactif
- ✅ Statistiques de base

### Version 2.0 (Prévue)
- 🔄 Multi-utilisateurs avec rôles
- 🔄 Base de données SQLite/PostgreSQL
- 🔄 Export PDF/Excel
- 🔄 API REST documentée
- 🔄 Historique des modifications
- 🔄 Notifications par email

### Version 3.0 (Future)
- 📋 Scanner de réseau intégré
- 📋 SNMP monitoring
- 📋 Mobile app (PWA)
- 📋 Intégration LDAP/Active Directory

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Poussez sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Guidelines

- Respectez le style de code existant
- Ajoutez des commentaires explicatifs
- Testez vos modifications en local
- Documentez les nouvelles fonctionnalités

---

## 📝 License

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

```
MIT License

Copyright (c) 2025 Focus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👨‍💻 Auteur

**Focus** - [GitHub](https://github.com/focus-on1)

Développé avec ❤️ à Lyon dans le cadre d'une mission professionnelle en entreprise.

---

## 🙏 Remerciements

- L'équipe IT de l'entreprise lyonnaise pour le contexte réel d'application
- La communauté Flask pour l'excellent framework
- Tous les contributeurs et utilisateurs de PatchMap

---

## 📞 Support

Pour toute question ou problème :

- 🐛 [Ouvrir une issue](https://github.com/focus-on1/patchmap/issues)
- 💬 [Discussions](https://github.com/focus-on1/patchmap/discussions)
- 📧 Email : [votre-email@example.com]

---

<div align="center">

**[⬆ Retour en haut](#-patchmap---gestion-visuelle-des-panneaux-de-brassage)**

Made with 🗺️ by Focus | © 2025

</div>
