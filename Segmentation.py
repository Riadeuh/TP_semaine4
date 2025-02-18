import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def thresholdOtsu(image):
    
    # Calculer l'histogramme de l'image
    hist, bin_edges = np.histogram(image.flatten(), bins=256, range=(0, 256))
    
    # Calculer la probabilité de chaque intensité (normalisée)
    total_pixels = image.size
    prob = hist / total_pixels
    
    # Calculer les moments (moyenne et variance) pour chaque classe
    cumulative_sum = np.cumsum(prob)
    cumulative_mean = np.cumsum(prob * np.arange(256))
    
    # Calculer la variance globale
    global_mean = cumulative_mean[-1]
    
    max_between_class_variance = 0
    optimal_threshold = 0
    
    for t in range(1, 256):
        # Moyenne de la classe 1 (avant le seuil t)
        weight1 = cumulative_sum[t]
        mean1 = cumulative_mean[t] / weight1 if weight1 > 0 else 0
        
        # Moyenne de la classe 2 (après le seuil t)
        weight2 = 1 - weight1
        mean2 = (cumulative_mean[-1] - cumulative_mean[t]) / weight2 if weight2 > 0 else 0
        
        # Calculer la variance entre les classes pour ce seuil t
        between_class_variance = weight1 * weight2 * (mean1 - mean2) ** 2
        
        # Maximiser la variance entre les classes
        if between_class_variance > max_between_class_variance:
            max_between_class_variance = between_class_variance
            optimal_threshold = t
    
    return optimal_threshold

image_path = "blobs.png"
image = cv2.imread(image_path)

#on trouve le seuile d'otsu sur l'image demandée
threshold = thresholdOtsu(image)
print(f"On trouve le seuil suivant : {threshold}")

#on applique la valeur du seuillage sur l'image (blanc si le pixel est inférieur au seuil noir sinon)
image_bin =  (image > threshold).astype(np.uint8) * 255

plt.imshow(image_bin, cmap='gray')
plt.title("seuil d'Otsu")
plt.axis('off')
plt.show()
