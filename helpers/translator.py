default_lang = 'en'

dictionary = {
    'Username:': 'Nom Utilisateur:',
    'Password:': 'Mot De Passe:',
    'Confirm Password:': 'Confirmer Mot De Passe:',
    'Gender:': 'Sexe:',
    'Company:': 'Société:',
    'First Name:': 'Prénom:',
    'Last Name:': 'Nom:',
    'Sign in': 'Se Connecter',
    'Sign In': 'Connecter',
    'Sign Up': 'S\'enregistrer',
    'Sign up': 'S\'enregistrer',
    'View Password': 'Voir Mot De Passe',
    'Forgot your password?': 'Mot de passe oublié?',
    'Step 1: Authentication Settings': 'Étape 1: Paramètres d\'authentification',
    'Step 2: Identification Information': 'Informations d\'identification',
    'Step 3: Personal Information': 'Étape 3: Informations personnelles',
    'Go Back': 'Retourner',
    'Next Step': 'Continuer',
    'View Password': 'Voir MDP',
    'Hide Password': 'Cacher MDP',
    'My Projects': 'Mes Projets',
    'My Sessions': 'Mes Sessions',
    'Create New Project': 'Nouveau Projet',
    'Load From Device': 'Charger Projet',
    'Access Project': 'Accéder Projet',
    'Create New Session': 'Nouvelle Session',
    'Join Session': 'Joindre Session',
    'Created In': 'Créé en',
    'Edited In': 'Modifié en',
    'Members:': 'Membres:',
    'Members': 'Membres',
    'Open': 'Ouvrir',
    'Edit': 'Modifier',
    'Share': 'Partager',
    'Delete': 'Supprimer',
    'Leave': 'Quitter',
    'General Info': 'Informations Générales',
    'History': 'Historique',
    'Project\'s Title:': 'Titre:',
    'Creation Date:': 'Date de Creation:',
    'Last Edit:': 'Dernière Modification:',
    'Open Editor': 'Ouvrir l\'éditeur',
    'Share Project': 'Partager Projet',
    'Export as XML': 'Exporter au XML',
    'Export to XML': 'Exporter au XML',
    'Revert': 'Revenir',
    'Session\'s Title:': 'Titre:',
    'End Session': 'Supprimer la Session',
    'Invite': 'Inviter',
    'Kick': 'Expulser',
    'Saved Collaborators': 'Collaborateurs Enregistrés',
    'Profile Photo:': 'Photo de Profile:',
    'Upload Photo': 'Changer Photo',
    'Save Changes': 'Sauvegarder',
    'Hover over the position you want, then left-click to drop; Press <Escape> if you want to cancel.': 'Survolez la position vous souhaitez, puis mettre une clicke gauche pour la déposer; Appuyez sur <Escape> pour annuler.',
    'Left-click in order to cancel resize mode': 'Clicke-gauche pour annuler le mode de redimensionnement',
    'Select an element in order to make a connection; Press <Escape> to cancel': 'Sélectionnez un élément pour établir une connexion; Appuyez sur <Escape> pour annuler',
    'Selection mode is enabled': 'Le mode de sélection est activé',
    'Move mode is enabled, press arrows to move around the canvas': 'Le mode de déplacement est activé, appuyez sur les flèches pour vous déplacer dans le canvas',
    'Process elements cannot be selected': 'On ne peut pas selectionner les elements de type Process',
    'Change Name': 'Change le Nom',
    'Associate': 'Associer',
    'Dissociate': 'Dissocier',
    'Resize': 'Redimensionner',
    'You don\'t have the right to edit this diagram!': 'Vous n\'avez pas le droit de modifier ce diagramme!',
    'Are you sure you want to leave this window?': 'Voulez-vous vraiment quitter cette fenêtre?',
    'A screenshot was taken before saving': 'Une capture d\'écran a été prise avant l\'enregistrement',
    'Sorry, a connection cannot be made between': 'Désolé, aucune connexion ne peut être établie entre',
    'and': 'et',
    'Accept': 'Accepter',
    'Decline': 'Refuser',
    'Open Session': 'Ouvrir la Session'
}

def translate(content):
    global default_lang
    # if it's english no need
    if default_lang != 'fr':
        return content
    # if there's no translation
    if content not in dictionary:
        return content
    # return translation
    return dictionary[content]