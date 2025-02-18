from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def voisins_4(x, y):
        return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

def ccLabel(image):
    hauteur, largeur = len(image), len(image[0])
    etiquettes = [[0] * largeur for _ in range(hauteur)]
    etiquette_actuelle = 0
    for i in range(hauteur):
        for j in range(largeur):
            if image[i][j] != 0 and etiquettes[i][j] == 0:
                etiquette_actuelle += 1
                pile = [(i, j)]
                while pile:
                    px, py = pile.pop()
                    if etiquettes[px][py] == 0:
                        etiquettes[px][py] = etiquette_actuelle
                        for vx, vy in voisins_4(px, py):
                            if 0 <= vx < hauteur and 0 <= vy < largeur and image[vx][vy] == image[i][j] and etiquettes[vx][vy] == 0:
                                pile.append((vx, vy))
    return etiquettes

def ccAreaFilter(image, seuil):
    etiquettes = ccLabel(image)
    
    hauteur, largeur = len(image), len(image[0])
    
    tailles = {}
    
    for i in range(hauteur):
        for j in range(largeur):
            etiquette = etiquettes[i][j]
            if etiquette != 0:
                if etiquette not in tailles:
                    tailles[etiquette] = 0
                tailles[etiquette] += 1
    
    nouvelle_image = np.zeros_like(image)
    
    for i in range(hauteur):
        for j in range(largeur):
            etiquette = etiquettes[i][j]
            if etiquette != 0 and tailles[etiquette] >= seuil:
                nouvelle_image[i][j] = image[i][j]
    
    return nouvelle_image

#chargement de l'image pour la traiter
chemin_image = "binary.png"
image = Image.open(chemin_image)
image = np.array(image)

#on détermine un seuil
seuil = 9


image_label = ccLabel(image)
image_filtrée = ccAreaFilter(image, seuil)
image_finale = ccLabel(image_filtrée)

plt.imshow(image_label,cmap = "jet")
plt.title("Labélisation de l'image originale")
plt.show()

plt.imshow(image_filtrée, cmap="jet")
plt.title(f"Image filtrée avec seuil {seuil}")
plt.show()

plt.imshow(image_finale,cmap = "jet")
plt.title("Labélisation de l'image filtrée")
plt.show()




