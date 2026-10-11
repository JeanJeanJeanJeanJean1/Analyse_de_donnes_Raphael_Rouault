#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def listedesterritoires(territoiretest, exportationUSD, importationUSD):
    listedesterritoires = [[territoiretest[0], 0]]
    pos = 0
    for element in range(0,len(territoiretest)):
        if territoiretest[element] != listedesterritoires[pos][0]:
            listedesterritoires.append([territoiretest[element], element])
            pos += 1
    lignes = []
    for element in range(1,len(listedesterritoires)):
        lignes.append(listedesterritoires[element][1] - 1)
    lignes.append(len(territoiretest))
    liste = []
    for element in range(0,len(listedesterritoires)):
        liste.append([listedesterritoires[element][0], listedesterritoires[element][1], lignes[element]])
    totalparterritoire = []
    for element in range(0,len(liste)):
        totalparterritoire.append([liste[element][0], exportationUSD[liste[element][1]:liste[element][2]].sum(), importationUSD[liste[element][1]:liste[element][2]].sum()])
    return totalparterritoire

def nettoyage(colonne):
    colonne2 = []
    for element in colonne:
        if element == 'Sans objet' or element =='-':
            colonne2.append(float(0))
        else:
            colonne2.append(float(element))
    return colonne2

def getliste(territoiretest):
    listedesterritoires = [[territoiretest[0], 0]]
    pos = 0
    for element in range(0,len(territoiretest)):
        if territoiretest[element] != listedesterritoires[pos][0]:
            listedesterritoires.append([territoiretest[element], element])
            pos += 1
    lignes = []
    for element in range(1,len(listedesterritoires)):
        lignes.append(listedesterritoires[element][1] - 1)
    lignes.append(len(territoiretest))
    liste = []
    for element in range(0,len(listedesterritoires)):
        liste.append([listedesterritoires[element][0], listedesterritoires[element][1], lignes[element]])
    return liste

# Question 4
print("Question 4")
# Source des données : https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
with open("./data/Afrique-2024.csv", "r", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

# Question 5
print("Question 5")
print(pd.DataFrame(contenu))

# Question 6
print("Question 6")
print("Nombre de lignes :", len(contenu))
print("Nombre de colonnes :", len(contenu.columns))

# Question 7
print("Question 7")
print(contenu.head())

# Question 8
print("Question 8")
print(contenu.dtypes)
print("Valeurs uniques dans Dist_VO (km):", contenu["Dist_VO (km)"].unique())
nature = {
    "year": "qualitative (nominale) — repère temporel",
    "origin_id": "qualitative nominale — identifiant de territoire (un chiffre, mais pas une quantité !)",
    "dest_id": "qualitative nominale — identifiant de territoire",
    "Dist_VO (km)": "quantitative continue — type : str (à cause de '-')",
    "hs92_Section_id": "qualitative nominale — code produit",
    "hs92_HS02_id": "qualitative nominale — code produit",
    "hs92_HS04_id": "qualitative nominale — code produit",
    "hs92_HS06_id": "qualitative nominale — code produit",
    "export_val": "quantitative continue — dollars",
    "import_val": "quantitative continue — dollars",
    "export_ton": "quantitative continue — tonnes, type : str (à nettoyer)",
    "import_ton": "quantitative continue — tonnes, type : str (à nettoyer)",
}
print(nature)

# Contenu des colonnes
# "year" : année
# "origin_id" : territoire de référence
# "dest_id" : territoire partenaire
# "Dist_VO (km)" : distance intercentroïde entre les deux territoires
# "hs92_Section_id" : code Section du produit
# "hs92_HS02_id" : code 2-digit du produit
# "hs92_HS04_id" : code 4-digit du produit
# "hs92_HS06_id" : code 6-digit du produit
# "export_val" : valeur des exportations du territoire de référence vers le territoire partenaire en dollars courants
# "import_val" : valeur des importations du territoire partenaire vers le territoire de référence en dollars courants
# "export_ton" : valeur des exportations du territoire de référence vers le territoire partenaire en tonnes
# "import_ton" : valeur des importations du territoire partenaire vers le territoire de référence en tonnes

# Question 9
print("Question 9")
export_ton = contenu["export_ton"]
import_ton = contenu["import_ton"]

# Question 10
print("Question 10")
effectif_export = 0
effectif_import = 0
for element in range(0, len(export_ton)):
    if export_ton[element] != "-":
        effectif_export += 1
    if import_ton[element] != "-":
        effectif_import += 1
print("Effectif exportations (tonnes) :", effectif_export)
print("Effectif importations (tonnes) :", effectif_import)
# Question 11
print("Question 11")
# Appliquer la fonction listedesterritoires(...) sur vos colonnes ici
resultats = listedesterritoires(contenu["origin_id"], contenu["export_val"], contenu["import_val"])

territoires = []
exportations = []
importations = []
for element in resultats:
    territoires.append(element[0])   # le code ISO du territoire
    exportations.append(element[1])  # le total export USD
    importations.append(element[2])  # le total import USD

# Diagramme exportations
plt.figure(figsize=(14, 6))
plt.bar(territoires, [valeur / 1e9 for valeur in exportations])
plt.xticks(rotation=45, ha="right")
plt.title("Exportations totales par territoire (USD)")
plt.ylabel("Milliards USD")
plt.tight_layout()
plt.savefig("./img/exportations.png", dpi=150)
plt.close()

# Diagramme importations
plt.figure(figsize=(14, 6))
plt.bar(territoires, [valeur / 1e9 for valeur in importations])
plt.xticks(rotation=45, ha="right")
plt.title("Importations totales par territoire (USD)")
plt.ylabel("Milliards USD")
plt.tight_layout()
plt.savefig("./img/importations.png", dpi=150)
plt.close()

# c. Construire la liste des territoires
territoires = []
for element in resultats:
    territoires.append(element[0])

# d + e. Pour chaque territoire : diagramme circulaire export/import
for element in resultats:
    code = element[0]                              # code ISO du territoire
    exportations = element[1] / 1e9                # en milliards, plus lisible
    importations = element[2] / 1e9
    valeurs = [exportations, importations]

    plt.figure(figsize=(6, 6))
    plt.pie(valeurs, labels=["Exportations", "Importations"], autopct="%1.1f%%")
    plt.title(f"Flux du territoire {code} (milliards USD)")
    plt.savefig(f"img/{code}.png", dpi=150)
    plt.close()

# Question 12 : nettoyer les 5 colonnes quantitatives et
# reconstruire un tableau propre (donnees2)
# ------------------------------------------------------------
print("Question 12")

# On nettoie chaque colonne : nettoyage() remplace "-" et "Sans objet"
# par 0, puis convertit en nombre (float)
distances_nettoyees  = nettoyage(contenu["Dist_VO (km)"])
export_usd_nettoyees = nettoyage(contenu["export_val"])
import_usd_nettoyees = nettoyage(contenu["import_val"])
export_ton_nettoyees = nettoyage(contenu["export_ton"])
import_ton_nettoyees = nettoyage(contenu["import_ton"])

# On reconstruit un nouveau tableau Pandas avec les colonnes nettoyées
donnees2titre = ["distance", "export_val_2", "import_val_2",
                 "export_ton_2", "import_ton_2"]

donnees2 = pd.DataFrame({
    donnees2titre[0]: distances_nettoyees,
    donnees2titre[1]: export_usd_nettoyees,
    donnees2titre[2]: import_usd_nettoyees,
    donnees2titre[3]: export_ton_nettoyees,
    donnees2titre[4]: import_ton_nettoyees,
})

# ------------------------------------------------------------
# Question 13 : calculer les paramètres statistiques de chaque
# colonne (moyenne, médiane, mode, écart-type, écart absolu
# moyen, étendue) puis les afficher
# ------------------------------------------------------------
print("Question 13")

parametres = []   # liste des paramètres, colonne par colonne

for colonne in donnees2titre:
    serie = donnees2[colonne]

    moyenne = round(serie.mean(), 2)                                  # centre de gravité
    mediane = round(serie.median(), 2)                                # coupe la série en 2
    mode    = round(serie.mode()[0], 2)                                # valeur la plus fréquente
    ecarttype = round(serie.std(), 2)                                 # dispersion classique
    ecart_absolu_moyenne = round(np.abs(serie - serie.mean()).mean(), 2)  # dispersion sans carrés
    etendue = round(serie.max() - serie.min(), 2)                     # max - min

    parametres.append([colonne, moyenne, mediane, mode,
                       ecarttype, ecart_absolu_moyenne, etendue])

for ligne in parametres:
    print(ligne)

# ------------------------------------------------------------
# Question 14 : distances interquartile (Q3 - Q1) et
# interdécile (D9 - D1) de chaque colonne quantitative
# ------------------------------------------------------------
print("Question 14")

distances = []   # liste des distances inter-quantiles

for colonne in donnees2titre:
    serie = donnees2[colonne]

    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    d1 = serie.quantile(0.10)
    d9 = serie.quantile(0.90)

    interquartile  = round(q3 - q1, 2)
    interdecile    = round(d9 - d1, 2)

    distances.append([colonne, interquartile, interdecile])

for ligne in distances:
    print(ligne)

# ------------------------------------------------------------
# Question 15 : boîtes à moustaches de chaque colonne,
# sauvegardées dans le dossier img (noms différents des
# diagrammes circulaires de la question 11)
# ------------------------------------------------------------
print("Question 15")

for colonne in donnees2titre:
    serie = donnees2[colonne]

    plt.figure(figsize=(6, 6))
    plt.boxplot(serie)
    plt.title(f"Boîte à moustaches : {colonne}")
    plt.savefig(f"img/boite_{colonne}.png", dpi=150)
    plt.close()

# ------------------------------------------------------------
# Question 16 : catégoriser les distances en 8 classes de
# 2500 km et compter les effectifs de chaque classe
# ------------------------------------------------------------
print("Question 16")

# Compteurs : un par classe ]0, 2500], ]2500, 5000], ..., ]17500, 20000]
compteurs = [0, 0, 0, 0, 0, 0, 0, 0]

for distance in distances_nettoyees:
    if distance > 0 and distance <= 2500:
        compteurs[0] += 1
    elif distance > 2500 and distance <= 5000:
        compteurs[1] += 1
    elif distance > 5000 and distance <= 7500:
        compteurs[2] += 1
    elif distance > 7500 and distance <= 10000:
        compteurs[3] += 1
    elif distance > 10000 and distance <= 12500:
        compteurs[4] += 1
    elif distance > 12500 and distance <= 15000:
        compteurs[5] += 1
    elif distance > 15000 and distance <= 17500:
        compteurs[6] += 1
    elif distance > 17500 and distance <= 20000:
        compteurs[7] += 1

# Affichage des effectifs par classe
classes = ["]0, 2500]", "]2500, 5000]", "]5000, 7500]",
           "]7500, 10000]", "]10000, 12500]",
           "]12500, 15000]", "]15000, 17500]", "]17500, 20000]"]

for i in range(8):
    print(f"Classe {classes[i]} : {compteurs[i]} observations")