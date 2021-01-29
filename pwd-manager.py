# -*- coding: utf-8 -*-

import sqlite3
from getpass import getpass
import random

connection = None
cursor = None

def connect(database):
    global connection, cursor
    # Connexion à la BDD SQLite
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    return

def login():
    global connection, cursor
    # Vérifie si un compte est créé dans la BDD
    cursor.execute("SELECT * FROM users;")
    account = cursor.fetchone()
    if account == None: # Pas de compte crée
        account_setup()
    else:
        correct_pass = password_verification()
        if correct_pass == False:
            verified = security_verification()
            if verified == False:
                reset()
                account_setup()
    options()
    return

def account_setup():
    global connection, cursor
    # Interface Reset Password
    print("Gestion mot de passe maître")
    notMatch = True
    while notMatch:
        password = getpass("Nouveau mot de passe: ")
        password2 = getpass("Retaper votre mot de passe: ")
        if password == password2:
            notMatch = False
        else:
            print("Password incorrect, réessayer")
    security_q = input("question de sécurité: ")
    security_a = input("réponse à la question: ")
    account_info = (password, security_q, security_a)
    cursor.execute("INSERT INTO users VALUES (?, ?, ?);", account_info)
    connection.commit()
    print("Votre compte est à présent crée !")
    return

def password_verification():
    global connection, cursor
    # Check si l'utilisateur à rentré le bon mot de passe
    verified = False
    attempts = 3    # Nombre de tentative
    failedAttempts = 0
    while verified == False and failedAttempts != attempts:
        password = getpass("Entrer votre mot de passe: ")  
        cursor.execute("SELECT * FROM users WHERE pwd = ?;", (password,))
        user_info = cursor.fetchone()
        if user_info == None:   # Mot de passe incorrect
            failedAttempts += 1
            left = attempts-failedAttempts
            word = "essais"
            if left == 1:
                word = "essai"
            print("Votre mot de passe est incorrect, vous avez", str(left), word, "restant")
        else:
            verified = True
    return verified

def security_verification():
    global connection, cursor
    # Check si la question de sécurité est valide
    verified = False
    print("Répondre à la question de sécurité pour accéder au compte")
    cursor.execute("SELECT security_q, security_a FROM users;")
    data = cursor.fetchone()
    question = data[0].lower()
    answer = data[1].lower()
    attempts = 3
    failedAttempts = 0
    while verified == False and failedAttempts != attempts:
        user_answer = input(question + ": ")
        if user_answer == answer:
            print("La réponse est correct")
            verified = True
        else:
            print("La réponse est incorrect")
            failedAttempts += 1
            left = attempts-failedAttempts
            word = "essais"
            if left == 1:
                word = "essai"
            print("Mot de passe invalide, il vous reste", str(left), word, "restant")
    return verified

def reset():
    global connection, cursor
    # Supprime toutes les données dans la database
    cursor.execute("DELETE FROM users;")
    cursor.execute("DELETE FROM website;")
    cursor.execute("DELETE FROM account;")
    connection.commit()
    print("Le programme a été rénitialisé")
    return

def options():
    # Menu des options
    print('''
            1. quitter
            2. gestion du mot de passe maître
            3. Voir les comptes
            4. Ajouter un compte
        ''')
    notValid = True
    while notValid:
        option = input("Choissisez une option: ")
        try:
            option = int(option)
            if option in range(1, 5):
                notValid = False
            else:
                print("Option invalide")
        except:
            print("Option invalide")
    if option == 1:
        quit()
    elif option == 2:
        settings()
    elif option == 3:
        view_accounts()
    else:
        site_name = input("Ajouter un compte pour le site internet: ").lower()
        add_account(site_name)
    return

def settings():
    # Paramètres des options
    print('''
            1. Revenir au menu
            2. Changer le mot de passe
            3. Changer la question de sécurité
            4. Rénitialiser
        ''')
    notValid = True
    while notValid:
        option = input("Choissisez une option: ")
        try:
            option = int(option)
            if option in range(1, 5):
                notValid = False
            else:
                print("Option invalide")
        except:
            print("Option invalide")
    if option == 1:
        options()
    elif option == 2:
        reset_manager_password()
    elif option == 3:
        reset_manager_question()
    else:
        reset()
    return

def reset_manager_password():
    global connection, cursor
    # Changer un mot de passe dejà defini dans la BDD
    print("Configurer un nouveau mot de passe")
    notMatch = True
    while notMatch:
        password1 = getpass("Nouveau mot de passe: ")
        password2 = getpass("Retaper votre mot de passe: ")
        if password1 == password2:
            notMatch = False
        else:
            print("Le mot de passe ne correspond pas, réessayer")
    new_password = (password1,)
    cursor.execute("UPDATE users SET pwd = ?;", new_password)   # Mise à jour du nouveau mot de passe
    connection.commit()
    print("mot de passe mis à jour !")
    settings()
    return

def reset_manager_question():
    global connection, cursor
    print("Configurer une nouvelle question de sécurité")
    question = input("Question de sécurité: ")
    notMatch = True
    while notMatch:
        answer1 = input("Réponse: ")
        answer2 = input("Retaper la réponse: ")
        if answer1 == answer2:
            notMatch = False
        else:
            print("La réponse ne correspond pas, réessayer")
    new_info = (question, answer1)
    cursor.execute("UPDATE users SET security_q = ?, security_a = ?;", new_info)   # Mise à jour de la nouvelle question de sécurité
    connection.commit()
    print("La question de sécurité à été mis à jour")
    settings()
    return

def view_accounts():
    global connection, cursor
    # Affiche les mots de passe de l'utilisateur
    print("Vos comptes pour lesquels vous avez enregistré des mots de passe")
    cursor.execute("SELECT site_name FROM website;")
    site_data = cursor.fetchall()
    print('''
            1. Menu principale''')
    adjust = 2  # Nombre d'option disponible
    max_option = len(site_data) + adjust
    for x in range(adjust, max_option):
        site = site_data[x-adjust][0].lower()
        print('''           ''', str(x) + ". " + site)
    print()
    notValid = True
    while notValid:
        option = input("option: ")
        try:
            option = int(option)
            if option in range(1, max_option):
                notValid = False
        except:
            print("Option invalide")
    if option == 1:
        options()
    else:   # Affiche infos du site
        index = option - adjust
        site = site_data[index][0].lower()
        all_accounts(site) 
    return

def all_accounts(site_name):
    global connection, cursor
    # Permet de visualiser les comptes associés au site
    #site_name - nom du site à récuperer les infos
    cursor.execute("SELECT account_no, acc_uname, acc_pwd FROM account WHERE lower(site_name) = ?;", (site_name,))
    account_info = cursor.fetchall()
    # Plusieurs comptes peuvent être associés à un site
    print("Vos comptes associés au site", site_name)
    count = 1
    for account in account_info:
        uname = account[1]
        pwd = account[2]
        print(count, "- " * 15)
        print("email/username:", uname)
        print("mot de passe:", pwd)
        count += 1
    print("\ncommands: option - numéro du compte | 'QUIT' pour revenir au menu | 'add' pour ajouter un compte")
    print("options: u - mettre à jour le mot de passe | d - supprimer le compte")
    notValid = True
    while notValid:
        command = input("Entrer une commande: ").replace(" ", "")
        if command == "QUIT":
            view_accounts()
        if command == "add":
            add_account(site_name)
        commands = command.split("-")
        if len(commands) == 2:
            option = commands[0].lower()
            acc_num = commands[1]
            if option == "u" or option == "d" or option == "a":
                try:
                    acc_num = int(acc_num) - 1  # On commande l'indexing à partir de 1
                    if acc_num in range(0, len(account_info)):
                        notValid = False
                except:
                    print("Option invalide")
            else:
                print("Option invalide")
        else:
            print("Option invalide")
    account_to_change = account_info[acc_num]
    if option == "u":
        update_account(account_to_change)
    if option == "d":
        delete_account(account_to_change)
    view_accounts()

def update_account(account):
    global connection, cursor
    # Mets à jour le compte de l'utilisateur( username et mot de passe)
    print('''
        1. Changer votre email/username
        2. Changer votre mot de passe
        3. quitter''')
    account_no = account[0]
    exit = False
    # Continue à demander à l'utilisateur d'entrer une option jusqu'a qu'il choisisse de quitter
    while not exit:
        notValid = True
        while notValid:
            option = input("option: ")
            try:
                option = int(option)
                if option in range(1, 4):
                    notValid = False
                else:
                    print("Option invalide")
            except:
                print("Option invalide")
        if option == 1:
            username = input("Entrer votre username/email: ")
            new_info = (username, account_no)
            cursor.execute("UPDATE account SET acc_uname = ? WHERE account_no = ?;", new_info)
            connection.commit()
            print("email/username a été mise à jour")
        elif option == 2:
            password = input("enter new password: ")
            new_info = (password, account_no)
            cursor.execute("UPDATE account SET acc_pwd = ? WHERE account_no = ?;", new_info)
            connection.commit()
            print("mot de passe a été mise à jour")
        else:
            exit = True
    return

def delete_account(account):
    global connection, cursor
    # Supprime un compte dans la base de données
    account_no = account[0]
    cursor.execute("DELETE FROM account WHERE account_no = ?;", (account_no,))
    connection.commit()
    print("Compte supprimé")
    return

def add_account(site_name):
    global connection, cursor
    # Ajoute un compte et génère un numero de compte unique avant de l'insérer dans la BDD. On continu de demander à l'utilisateur d'entrer une option jusqu'a qu'il quitte.
    cursor.execute("SELECT site_name FROM website WHERE lower(site_name) = ?;", (site_name,))
    site_info = cursor.fetchone()
    # Ajoute un site web à la BDD si il n'existe pas
    if site_info == None:
        print("Nouveau site ajouté dans la BDD")
        cursor.execute("INSERT INTO website VALUES (?);", (site_name,))
        connection.commit()
    uname = input("email/username: ")
    password = input("mot de passe: ")
    notValid = True
    while notValid:
        decision = input("Ajouter le compte (y/n)? ").lower()
        if decision == "y" or decision == "n":
            notValid = False
        else:
            print("Entrer invalide")
    if decision == "y":
        # Génère un numero de compte aléatoire et l'insert dans la BDD
        cursor.execute("SELECT account_no FROM account;")
        info = cursor.fetchall()
        allNo = []
        for num in info:
            allNo.append(num[0])
        accNo = random.randint(0, 1000)
        while accNo in allNo:
            accNo = random.randint(0, 1000)
        account_info = (accNo, uname, password, site_name)
        cursor.execute("INSERT INTO account VALUES (?, ?, ?, ?);", account_info)
        connection.commit()
        print("Compte ajouté")
    else:
        print("Compte non ajouté")
    options()
    return

# Connexion à la BDD
def main():
    global connection, cursor
    database = "./pwd-mgr.db"
    connect(database)
    login()
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()