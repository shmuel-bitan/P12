# Epic Events CRM CLI P12 OpenClassRooms

Epic Events CRM CLI est une application en ligne de commande (CLI) développée en Python pour gérer les clients, les contrats et les événements d'une entreprise organisatrice d'événements. 

## Fonctionnalités

- Gestion des utilisateurs :
  - Créer, afficher, mettre à jour et supprimer des utilisateurs
- Gestion des clients :
  - Créer, afficher, mettre à jour et supprimer des clients
- Gestion des contrats :
  - Créer, afficher, mettre à jour et supprimer des contrats
- Gestion des événements :
  - Créer, afficher, mettre à jour et supprimer des événements
- Affichage des événements non attribués et des événements par contact support
- Affichage des contrats par statut signé/non signé

## Exigences

- Python 3.9 ou une version plus récente
- Bibliothèques Python : `sentry-sdk`, `sqlalchemy`, `passlib`, `datetime`
- Configuration de la base de données SQLAlchemy
- Utilisation de Sentry pour la journalisation des exceptions et des erreurs

## Installation

1. Clonez le dépôt :
   ```sh
   git clone https://github.com/votre-utilisateur/epic-events-crm-cli.git
   cd epic-events-crm-cli
Créez un environnement virtuel et activez-le :

```sh
Copier le code
python -m venv venv
source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
Installez les dépendances :

Copier le code
pip install -r requirements.txt
Configurez votre base de données dans le fichier db_config.py.
````
Initialisez Sentry avec votre DSN dans main.py :

````sh
Copier le code
sentry_sdk.init(
    dsn="votre_dsn_sentry",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

````

Utilisation
Lancez l'application avec la commande suivante :

````sh
Copier le code
python main.py
Suivez les instructions à l'écran pour naviguer dans le menu principal et utiliser les différentes fonctionnalités.
````
## Structure du Projet
main.py : Point d'entrée principal de l'application.
controllers.py : Contient les fonctions de contrôle pour gérer les utilisateurs, clients, contrats et événements.
models.py : Définit les modèles SQLAlchemy pour les utilisateurs, clients, contrats et événements.
queries.py : Contient les fonctions de requêtes à la base de données.
views.py : Contient les fonctions d'affichage et de saisie de l'utilisateur.
permissions.py : Gère les permissions des utilisateurs en fonction de leur rôle.
serializers.py : Définit les serializers pour valider et nettoyer les données d'entrée.
Permissions des Utilisateurs
Équipe de gestion :

Créer, mettre à jour et supprimer des utilisateurs
Créer et modifier tous les contrats
Filtrer l'affichage des événements
Modifier des événements
Équipe commerciale :

Créer des clients
Mettre à jour les clients dont ils sont responsables
Modifier les contrats des clients dont ils sont responsables
Filtrer l'affichage des contrats
Créer des événements pour leurs clients
Équipe support :

Filtrer l'affichage des événements
Mettre à jour les événements dont ils sont responsables
Sécurité
Validation et nettoyage des entrées utilisateur avec des serializers
Prévention des injections SQL en utilisant des ORM et des requêtes paramétrées
Principe du moindre privilège appliqué aux permissions d'accès aux données