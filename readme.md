# Test UI site de l'Unamur

Nous avons choisi de tester l'interface utilisateur du site de l'Université de Namur en mettant l'accent sur la transition entre les versions anglaise et française. Nous utiliserons Selenium pour réaliser des tests et détecter les éventuels problèmes lors du changement de langue sur le site. L'objectif est d'obtenir des résultats significatifs et d'améliorer l'expérience utilisateur.

## Table des matières

- [Installation](#installation)
- [Utilisation](#utilisation)

## Installation

Afin d'utiliser le programme vous avez besoin de plusieurs choses:

### Selenium

1. Assurez-vous d'avoir Python installé sur votre système. Vous pouvez le télécharger à partir du site officiel de Python : [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. Installez le gestionnaire de packages pip si ce n'est pas déjà fait. Dans un terminal, exécutez la commande suivante :

```
python -m ensurepip --upgrade
```

3. Installez la bibliothèque Selenium en utilisant pip. Dans le terminal, exécutez la commande suivante :

```
pip install selenium
```


4. Téléchargez le navigateur WebDriver correspondant à votre navigateur préféré (par exemple, Chrome, Firefox, etc.). Assurez-vous de télécharger la version compatible avec votre navigateur et votre système d'exploitation. Vous pouvez trouver les liens de téléchargement et les instructions d'installation sur le site officiel de Selenium : [https://www.selenium.dev/selenium/docs/api/py/index.html#drivers](https://www.selenium.dev/selenium/docs/api/py/index.html#drivers).

5. Ajoutez le chemin d'accès au WebDriver à votre variable d'environnement PATH. Cela permettra à Selenium de localiser le WebDriver lors de l'exécution de vos scripts. Si vous n'êtes pas familier avec la configuration de la variable d'environnement PATH, vous pouvez consulter ce guide : [https://www.selenium.dev/selenium/docs/api/py/index.html#drivers](https://www.selenium.dev/selenium/docs/api/py/index.html#drivers).

Une fois ces étapes terminées, vous devriez avoir Selenium correctement installé et configuré pour être utilisé dans votre projet. Vous pouvez maintenant importer les modules de Selenium dans vos scripts Python et commencer à automatiser les tests d'interface utilisateur.


## Utilisation

Une fois avoir spécifier le lien du webDriver le votre choix (*PATH*), il vous suffire de lancer la fonction :
```
test_unamur_translation(initial_language)
```

Avec comme paramètre soit *"fr"* soit *"en"* en fonction de la langue du site de départ.

Attention à bien specifier le lien du dossier où seront stocké les différentes captures d'écran. (PATH_SCREENSHOT)