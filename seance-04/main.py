#coding:utf8

import numpy as np
import pandas as pd
import math
import scipy
import scipy.stats
import matplotlib.pyplot as plt

# C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement 
# que pratiquement. D'autre part, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de 
# probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente
# afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les 
# résultats ne sont pas conformes à la théorie probabiliste.
# Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle
# principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests 
# y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
# Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par 
# une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il 
# présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous 
# aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

# Par convention, on place les fonctions locales au début du code après les bibliothèques.
def ouvrirUnFichier(nom):
    return pd.read_csv(nom)
# Question 1 : Théorie de l'échantillonnage (intervalles de fluctuation)
# L'échantillonnage se base sur la répétitivité.
print("Question 1")
df = ouvrirUnFichier("data/Echantillonnage-100-Echantillons.csv")
df.head()
print (df.shape)
print (df.iloc[0])
print (df.iloc[0].sum())
moyennes = df.mean().round(0)
print("Moyennes : ", moyennes)
moyennes.sum()
print("Moyenne des moyennes : ", moyennes.sum())
total = moyennes / moyennes.sum()
total = total.round(2)
print("Fréquence des moyennes : ", total)
# Fréquences réelles de la population mère (pour la comparaison)
reel = {"Pour": 852/2185, "Contre": 911/2185, "Sans opinion": 422/2185}

n = 1000  # taille d'un échantillon
for nom, f in total.items():          # nom + valeur, pour chaque opinion
    marge = 1.96 * math.sqrt(f * (1 - f) / n)
    bas, haut = f - marge, f + marge
    print(nom, "→ intervalle [", round(bas, 2), ";", round(haut, 2), "]")
    if bas <= reel[nom] <= haut:
        print("  → la fréquence réelle", round(reel[nom], 2), "est DANS l'intervalle")
    else:
        print("  → la fréquence réelle", round(reel[nom], 2), "est HORS de l'intervalle")

# Question 2 : Théorie de l'estimation (intervalles de confiance)
#L'estimation se base sur l'effectif.
print("Question 2")

# Échantillon 1
echantillon = df.iloc[0]
valeurs = list(echantillon)
print("Valeurs : ", valeurs)
total = sum(valeurs)
fréquences = [v / total for v in valeurs]
print("Fréquences : ", fréquences)
# Calcul de l'intervalle de confiance pour chaque opinion
n = total  # taille de l'échantillon
for f in fréquences:
    marge = 1.96 * math.sqrt(f * (1 - f) / n)
    bas, haut = f - marge, f + marge
    print("Intervalle de confiance [", round(bas, 2), ";", round(haut, 2), "]")

# Échantillon 2 
echantillon = df.iloc[6]
valeurs = list(echantillon)
print("Valeurs : ", valeurs)
total = sum(valeurs)
fréquences = [v / total for v in valeurs]
print("Fréquences : ", fréquences)

# Calcul de l'intervalle de confiance pour chaque opinion
n = total 
for f in fréquences:
    marge = 1.96 * math.sqrt(f * (1 - f) / n)
    bas, haut = f - marge, f + marge
    print("Intervalle de confiance [", round(bas, 2), ";", round(haut, 2), "]")


# Question 3 : Théorie de la décision (tests d'hypothèse)
# La décision se base sur la notion de risques alpha et bêta.
# Comme à la séance précédente, l'ensemble des tests se trouve au lien 
# : https://docs.scipy.org/doc/scipy/reference/stats.html
print("Question 3")

serie1 = ouvrirUnFichier("data/Loi-normale-Test-1.csv")
serie2 = ouvrirUnFichier("data/Loi-normale-Test-2.csv")
W1, p1 = scipy.stats.shapiro(serie1.iloc[:, 0])
W2, p2 = scipy.stats.shapiro(serie2.iloc[:, 0])
print ("Test de normalité de Shapiro-Wilk : ", (W1, p1))
print ("Test de normalité de Shapiro-Wilk : ", (W2, p2))

#Histogrammes des deux séries

for b in (10, 30, 50, 80):
    plt.figure()
    plt.hist(serie1.iloc[:, 0], bins=b)
    plt.title(f"Test 1 - bins={b}")
    plt.savefig(f"Img/test1-bins-{b}.png", dpi=150)
for b in (10, 30, 50, 80):
    plt.figure()
    plt.hist(serie2.iloc[:, 0], bins=b)
    plt.title(f"Test 2 - bins={b}")
    plt.savefig(f"Img/test2-bins-{b}.png", dpi=150)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(serie1.iloc[:, 0], bins=50); axes[0].set_title("Test 1")
axes[1].hist(serie2.iloc[:, 0], bins=50); axes[1].set_title("Test 2")
plt.savefig("Img/Question3.png", dpi=150)

#Histogrammes de trois lois types
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].hist(np.random.normal(170, 10, 2000), bins=50)   # cloche (loi normale)
axes[0].set_title("Normale")
axes[1].hist(np.random.exponential(2, 2000), bins=50)  # pic à 0 (loi exponentielle)
axes[1].set_title("Exponentielle")
axes[2].hist(np.random.uniform(0, 10, 2000), bins=50)   # plateau (loi uniforme)
axes[2].set_title("Uniforme")
plt.savefig("Img/lois-types.png", dpi=150)
plt.show()

# Question bonus
print("Question bonus")
