import tkinter as tk
import pandas as pd
import numpy as np

from tkinter import filedialog, messagebox, ttk
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

fichier_charge = False

# Fonction pour charger un fichier Excel
def charger_fichier():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if filepath:
        try:
            global df
            global fichier_charge
            fichier_charge = True
            df = pd.read_excel(filepath)
            messagebox.showinfo("Succès", f"Fichier {filepath} chargé avec succès.")
            bouton_suivant.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")

# Fonction pour ouvrir la fenêtre de sélection des colonnes
def ouvrir_fenetre_colonnes():
    bouton_suivant.config(state=tk.NORMAL)
    global colonne_selection_fenetre
    colonne_selection_fenetre = tk.Toplevel(root)
    colonne_selection_fenetre.title("Sélection des colonnes")
    
    # Création du cadre principal pour inclure la barre de défilement
    frame_canvas = tk.Frame(colonne_selection_fenetre)
    frame_canvas.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(frame_canvas)
    scroll_y = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    frame_content = tk.Frame(canvas)
    
    frame_content.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=frame_content, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    tk.Label(frame_content, text="Sélectionnez les colonnes à utiliser:").pack()
    
    global colonnes_coches
    colonnes_coches = []
    
    for colonne in df.columns:
        var = tk.BooleanVar()
        tk.Checkbutton(frame_content, text=colonne, variable=var).pack(anchor='w')
        colonnes_coches.append((colonne, var))

    bouton_valider_colonnes = tk.Button(frame_content, text="Valider", command=valider_selection)
    bouton_valider_colonnes.pack(side=tk.LEFT, padx=10, pady=10)


# Fonction pour valider la sélection des colonnes
def valider_selection():
    colonnes_selectionnees = [col for col, var in colonnes_coches if var.get()]
    if not colonnes_selectionnees:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins une colonne.")
        return

    global resultat_kmeans, n_clusters
    n_clusters = int(entry_clusters.get())
    resultat_kmeans = calculate_kmeans(df[colonnes_selectionnees], n_clusters)

    afficher_resultats()

# Fonction de calcul de KMeans
def calculate_kmeans(df, n_clusters):
    df = df.copy()
    for col in df.columns:
        if df[col].dtype not in [np.int64, np.float64, np.uint8, np.uint16, np.uint32, np.uint64, np.float16, np.float32, np.float64]:
            df = df.drop(col, axis=1)
    X = df  # Remplacez par vos attributs

    # Normaliser les données
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. Appliquer K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df.loc[:, 'Cluster'] = kmeans.fit_predict(X_scaled)
    
    results = {}

    global_means = df.mean()
    global_std = df.std()
    n = df.shape[0]

    for i in range(n_clusters):
        result = {} 
        data_cluster = df[df['Cluster'] == i]
        n_C = data_cluster.shape[0]
        for var in df.columns:
            var_results = {}  
            mean_cluster = data_cluster[var].mean()
            global_mean = global_means[var]
            std_dev = global_std[var]
            denominator = std_dev * np.sqrt(n / n_C)
            if denominator == 0:
                test_value = np.nan
            else:
                test_value = (mean_cluster - global_mean) / denominator
            # values = pd.unique(data_cluster[var]).tolist()
            # for value in values:
            mean = data_cluster[var].mean()  
                # var_results[value] = mean
            result[var] = {"test_value": test_value, "mean": mean , "Global mean": global_mean}
            
        results[f"Cluster {i}"] = result
    
    data_list = []

    # Parcours du dictionnaire `results` pour construire les lignes du DataFrame
    for cluster_name, features in results.items():
        for feature, values in features.items():
            # Ajout d'une ligne pour chaque combinaison cluster-feature avec les valeurs correspondantes
            data_list.append({
                'Cluster': cluster_name,
                'Feature': feature,
                'test_value': round(values['test_value'], 2),
                'mean': values['mean'].round(2),
                'global_mean': values['Global mean'].round(2)
            })

    # Conversion de la liste en DataFrame
    df_ = pd.DataFrame(data_list)
    print(f'df_ colonnes : {df_.columns}')
    return df_.copy()
# Fonction pour afficher les résultats sous forme de tableau
def afficher_resultats():
    colonne_selection_fenetre.destroy()  # Ferme la fenêtre de sélection des colonnes
    if 'Cluster' not in resultat_kmeans.columns:
        messagebox.showerror("Erreur", "La colonne 'Cluster' n'a pas été ajoutée correctement.")
        return
    resultat_fenetre = tk.Toplevel(root)
    resultat_fenetre.title("Résultats de KMeans")
    
    tree = ttk.Treeview(resultat_fenetre, columns=resultat_kmeans.columns.to_list(), show="headings")
    
    # Configuration des colonnes
    for col in resultat_kmeans.columns:
        tree.heading(col, text=col)
        # tree.column(col, width=100, anchor='center')
    
    # Insertion des lignes
    for _, row in resultat_kmeans.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True)

    bouton_telecharger = tk.Button(resultat_fenetre, text="Télécharger le résultat", command=lambda: telecharger_resultat(resultat_kmeans))
    bouton_telecharger.pack()

    bouton_update_n_clusters = tk.Button(resultat_fenetre, text="Update n_clusters", command=ouvrir_page_principale)
    bouton_update_n_clusters.pack()

    bouton_update_colonnes = tk.Button(resultat_fenetre, text="Update variables", command=ouvrir_fenetre_colonnes)
    bouton_update_colonnes.pack()

# Fonction pour télécharger les résultats
def telecharger_resultat(df):
    filepath = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if filepath:
        try:
            df.to_excel(filepath, index=False)
            messagebox.showinfo("Succès", f"Résultats enregistrés dans {filepath}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")

# Fonction pour ouvrir la page principale
def ouvrir_page_principale():
    root.deiconify()

def verifier_conditions():
    # Vérifier si le fichier est chargé
    if not fichier_charge:
        bouton_suivant.config(state=tk.DISABLED)
        return

    # Vérifier si l'option est choisie
    if choix_var.get() not in options:
        bouton_suivant.config(state=tk.DISABLED)
        return

    # Vérifier si l'entrée des clusters est un entier >= 2
    try:
        n_clusters = int(entry_clusters.get())
        if n_clusters < 2:
            raise ValueError
    except ValueError:
        bouton_suivant.config(state=tk.DISABLED)
        return

    # Vérifier si le champ de texte est rempli
    if not entry_text.get().strip():
        bouton_suivant.config(state=tk.DISABLED)
        return

    # Si toutes les conditions sont remplies, activer le bouton "Suivant"
    bouton_suivant.config(state=tk.NORMAL)

# Initialisation de l'interface principale
root = tk.Tk()
root.title("KMeans Interface Utilisateur")

# Bouton de chargement du fichier
bouton_charger = tk.Button(root, text="Charger un fichier Excel", command=charger_fichier)
bouton_charger.pack()

# Entrée pour le nombre de clusters
tk.Label(root, text="Nombre de clusters (>= 2) :").pack()
entry_clusters = tk.Entry(root)
entry_clusters.pack()
entry_clusters.bind("<KeyRelease>", lambda event: verifier_conditions())  # Vérifie en temps réel

# Entrée en chaîne de caractères obligatoire
tk.Label(root, text="Nom de la Typologie :").pack()
entry_text = tk.Entry(root)
entry_text.pack()
entry_text.bind("<KeyRelease>", lambda event: verifier_conditions())  # Vérifie en temps réel

# Menu de sélection unique
options = ["K-Means", "CAH", "Mixte (non implémentée)"]
choix_var = tk.StringVar()
choix_var.set("Choisissez une option")  

tk.Label(root, text="Choisissez un Algo :").pack()
menu_choix = tk.OptionMenu(root, choix_var, *options, command=lambda _: verifier_conditions())
menu_choix.pack()

# Bouton "Suivant"
bouton_suivant = tk.Button(root, text="Suivant", command=ouvrir_fenetre_colonnes, state=tk.DISABLED)
bouton_suivant.pack()

root.mainloop()