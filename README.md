# Auto-Clicker

Un outil d'automatisation de clics multiples avec configuration personnalisable des positions et du nombre de clics.

## 📋 Prérequis

- Python 3.x installé sur votre système
- Windows, Linux ou macOS

## 🚀 Installation

1. Créez un environnement virtuel :

```bash
python -m venv .venv
```

````

2. Activez l'environnement virtuel :

- Sous Windows (PowerShell) :

```bash
.venv\Scripts\activate
```

- Sous Linux/macOS :

```bash
source .venv/bin/activate
```

3. Installez les dépendances :

```bash
pip install pyautogui keyboard
```

## 💻 Utilisation

1. Lancez le programme :

```bash
python auto_clicker.py
```

2. Menu Principal :

- Option 1 : Capture de nouvelles positions

  - F2 : Capturer la position actuelle du curseur
  - Entrez le nombre de clics souhaité pour chaque position
  - F3 : Terminer la capture
  - Échap : Quitter le programme

- Option 2 : Afficher/Modifier les positions

  - Voir la liste des positions
  - Modifier les coordonnées
  - Modifier le nombre de clics
  - Supprimer des positions

- Option 3 : Exécuter les clics

  - Définir le délai entre les clics
  - Exécution automatique

- Option 4 : Réexécuter avec les derniers paramètres

  - Relance la dernière séquence de clics

- Option 5 : Quitter le programme

## ⚠️ Notes importantes

- Utilisez la touche Échap pour arrêter le programme à tout moment
- Déplacez rapidement la souris dans un coin de l'écran pour arrêter l'exécution (failsafe)
- Le délai minimum entre les clics est de 0 seconde

## 🛠️ Fonctionnalités

- Capture multiple de positions
- Nombre de clics personnalisable par position
- Délai configurable entre les clics
- Sauvegarde de la dernière configuration
- Interface utilisateur intuitive
- Exécution parallèle des clics

## 🔍 Dépannage

Si vous rencontrez des erreurs :

1. Vérifiez que l'environnement virtuel est activé
2. Assurez-vous que toutes les dépendances sont installées
3. Sous Linux/WSL, des droits supplémentaires peuvent être nécessaires

## 📝 Licence

Ce projet est sous licence libre d'utilisation.

## 👥 Contribution

N'hésitez pas à proposer des améliorations ou signaler des bugs.

```

```
````
