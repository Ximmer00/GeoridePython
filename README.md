# GeoRide Python CLI

![Logo GeoRide](https://github.com/Ximmer00/Georide-Perl/blob/master/logo_transparent.png)

> Cette branche est une modification du master afin de rendre le script utilisable en CLI

## À quoi ça sert ?

Ce script Python permet de :

-   Voir l'état du tracker
-   Verrouiller le tracker de sa moto
-   Le déverouiller
-   Localiser sa moto

## Utilisation

Pour utiliser le script, il faut avoir un tracker ([Site de GeoRide](https://georide.fr/ "Site de GeoRide")) ou avoir un ami qui partage le sien.

Lancement du script :

    python Georide_CLI.py --email 'youremail@domain.com' --password 'yourpass' --command

Les actions possibles sont :
  - lock => verrouille le boitier
  - unlock => deverouille le boitier
  - status => affiche un status résumé du boitier
  - locate => localise la position actuelle du boîtier

Pour comprendre le fonctionnement voici la documentation de l'utilisation de l'API se trouve [ici](https://api.georide.fr "Doc de l'API").

## Contribution

Toute proposition d'amélioration est la bienvenue. Si vous rencontrez un problème ou souhaitez ajouter de nouvelles fonctionnalités, n'hésitez pas à envoyer une pull request.

### Futures améliorations

✌️ 🇫🇷 🏍️
