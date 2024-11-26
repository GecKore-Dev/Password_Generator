"""
#  _____           _   __               
# |  __ \         | | / /               
# | |  \/ ___  ___| |/ /  ___  _ __ ___ 
# | | __ / _ \/ __|    \ / _ \| '__/ _ \
# | |_\ \  __/ (__| |\  \ (_) | | |  __/
#  \____/\___|\___\_| \_/\___/|_|  \___|
#                                       
# Nom du fichier : password_generator.py
# Version       : 1.0.0
# Auteur        : GecKore-Dev
# GitHub        : https://github.com/GecKore-Dev
"""

import random
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from PIL import Image, ImageTk
import os
import sys

# Fonction pour obtenir le chemin des ressources (logo inclus dans le .exe)
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Chemins pour le logo et l'icône
logo_path = get_resource_path("Geckore/Logo-GecKore.png")
icon_path = get_resource_path("Geckore/Icon-GecKore.ico")

# Fonction pour générer le mot de passe
def generate_password():
    try:
        length = int(length_var.get())

        if length < 4:
            raise ValueError("La longueur doit être d'au moins 4 caractères.")

        # Créer la liste des caractères disponibles
        characters = ""
        if use_uppercase.get():
            characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if use_lowercase.get():
            characters += "abcdefghijklmnopqrstuvwxyz"
        if use_numbers.get():
            characters += "0123456789"
        if use_special.get():
            characters += "!@#$%^&*()-_=+[]{}|;:',.<>?/"

        if not characters:
            raise ValueError("Veuillez sélectionner au moins une option.")

        # Exclure les caractères ambigus
        if exclude_ambiguous.get():
            characters = "".join([c for c in characters if c not in "oO01lI"])

        # Générer le mot de passe
        password = "".join(random.choice(characters) for _ in range(length))

        # Afficher le résultat
        result_text.delete(0, tk.END)
        result_text.insert(0, password)
    except ValueError as ve:
        messagebox.showerror("Erreur", str(ve))
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Fonction pour copier le mot de passe dans le presse-papier
def copy_to_clipboard():
    password = result_text.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Succès", "Mot de passe copié dans le presse-papier !")
    else:
        messagebox.showerror("Erreur", "Aucun mot de passe à copier.")

# Interface graphique
def create_gui():
    global use_uppercase, use_lowercase, use_numbers, use_special, exclude_ambiguous, length_var, result_text

    root = tk.Tk()
    root.title("Générateur de Mots de Passe")
    root.geometry("600x550")
    root.iconbitmap(icon_path)

    # Ajout du logo
    try:
        img = Image.open(logo_path)
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo)
        logo_label.image = logo
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"Erreur lors du chargement du logo : {e}")
        messagebox.showerror("Erreur", f"Impossible de charger le logo : {e}")

    # Titre
    title_label = tk.Label(root, text="Générateur de Mots de Passe", font=("Arial", 20, "bold"), fg="black")
    title_label.pack(pady=5)

    # Options
    options_frame = tk.Frame(root)
    options_frame.pack(pady=10)

    use_numbers = tk.BooleanVar(value=True)
    use_lowercase = tk.BooleanVar(value=True)
    use_uppercase = tk.BooleanVar(value=True)
    use_special = tk.BooleanVar(value=False)
    exclude_ambiguous = tk.BooleanVar(value=False)

    numbers_check = ttk.Checkbutton(options_frame, text="Avec des chiffres [123...]", variable=use_numbers)
    numbers_check.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    lowercase_check = ttk.Checkbutton(options_frame, text="Avec des lettres minuscules [abc...]", variable=use_lowercase)
    lowercase_check.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    uppercase_check = ttk.Checkbutton(options_frame, text="Avec des lettres majuscules [ABC...]", variable=use_uppercase)
    uppercase_check.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    special_check = ttk.Checkbutton(options_frame, text="Avec des caractères spéciaux", variable=use_special)
    special_check.grid(row=3, column=0, padx=5, pady=5, sticky="w")
    ambiguous_check = ttk.Checkbutton(options_frame, text="Exclure les caractères similaires [oO01lI]", variable=exclude_ambiguous)
    ambiguous_check.grid(row=4, column=0, padx=5, pady=5, sticky="w")

    # Longueur du mot de passe
    length_label = tk.Label(root, text="Nombre de caractères :", font=("Arial", 12))
    length_label.pack(pady=5)

    length_var = tk.StringVar(value="12")
    length_entry = ttk.Entry(root, textvariable=length_var, font=("Arial", 12), width=10)
    length_entry.pack(pady=5)

    # Affichage du mot de passe
    result_text = tk.Entry(root, font=("Arial", 14), justify="center", width=50)
    result_text.pack(pady=10)

    # Boutons
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(pady=10)

    generate_button = tk.Button(buttons_frame, text="Créer votre mot de passe", command=generate_password, bg="green", fg="white", font=("Arial", 12))
    generate_button.grid(row=0, column=0, padx=10)

    copy_button = tk.Button(buttons_frame, text="Copier", command=copy_to_clipboard, bg="blue", fg="white", font=("Arial", 12))
    copy_button.grid(row=0, column=1, padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
