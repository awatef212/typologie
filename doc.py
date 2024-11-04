"""

# Global Variables Documentation

This document provides an overview of the global variables used in the `main.py` file located at `/home/awatef/Bureau/E15670/main.py`.

## Global Variables

### 1. `fichier_charge`
- **Type**: `bool`
- **Description**: Indicates whether a file has been successfully loaded into the application. It is initially set to `False` and is updated to `True` when a file is loaded successfully using the `charger_fichier` function.

### 2. `df`
- **Type**: `pandas.DataFrame`
- **Description**: Stores the data loaded from the Excel file. This variable is defined globally within the `charger_fichier` function after successfully reading the file using `pd.read_excel`.

### 3. `colonne_selection_fenetre`
- **Type**: `tk.Toplevel`
- **Description**: Represents the window that allows users to select columns from the loaded DataFrame. This variable is created in the `ouvrir_fenetre_colonnes` function when the user decides to select columns.

### 4. `colonnes_coches`
- **Type**: `list`
- **Description**: A list that holds tuples of column names and their associated Boolean variables (for checkboxes) in the column selection window. This variable is initialized in the `ouvrir_fenetre_colonnes` function.

### 5. `resultat_kmeans`
- **Type**: `pandas.DataFrame`
- **Description**: Stores the results of the KMeans clustering operation. This variable is defined globally in the `valider_selection` function after the KMeans calculation is performed.

### 6. `n_clusters`
- **Type**: `int`
- **Description**: Represents the number of clusters specified by the user. This variable is defined globally in the `valider_selection` function after retrieving the value from the entry field.

### 7. `root`
- **Type**: `tk.Tk`
- **Description**: The main application window created using Tkinter. This variable is initialized at the beginning of the script and serves as the root for all other Tkinter widgets.

### 8. `bouton_suivant`
- **Type**: `tk.Button`
- **Description**: A button widget that allows the user to proceed to the column selection window. This button is initially disabled and is enabled when the necessary conditions are met.

### 9. `entry_clusters`
- **Type**: `tk.Entry`
- **Description**: An entry widget where the user inputs the desired number of clusters for the KMeans algorithm. This variable is used to retrieve the number of clusters specified by the user.

### 10. `entry_text`
- **Type**: `tk.Entry`
- **Description**: An entry widget for the user to input a typology name. This variable is used to ensure that the user provides a non-empty string.

### 11. `choix_var`
- **Type**: `tk.StringVar`
- **Description**: A Tkinter variable that holds the selected algorithm option from a dropdown menu. It is used to determine which algorithm the user has chosen.

### 12. `options`
- **Type**: `list`
- **Description**: A list of available algorithm options for the user to choose from. Currently includes "K-Means", "CAH", and "Mixte (non implémentée)".

### 13. `bouton_charger`
- **Type**: `tk.Button`
- **Description**: A button widget that triggers the file loading process when clicked. It calls the `charger_fichier` function.

### 14. `bouton_telecharger`
- **Type**: `tk.Button`
- **Description**: A button widget in the results window that allows the user to download the results of the KMeans clustering. It calls the `telecharger_resultat` function.

### 15. `bouton_update_n_clusters`
- **Type**: `tk.Button`
- **Description**: A button widget in the results window that allows the user to update the number of clusters. It calls the `ouvrir_page_principale` function.

### 16. `bouton_update_colonnes`
- **Type**: `tk.Button`
- **Description**: A button widget in the results window that allows the user to update the selected columns. It calls the `ouvrir_fenetre_colonnes` function.
    """