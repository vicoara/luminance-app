"""
Núcleo de extracción de paletas de color.

Usa clustering K-Means en espacio de color LAB (perceptualmente uniforme)
para extraer los colores dominantes de una imagen.
"""

import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans


def extract_palette(image_path: str, n_colors: int = 6) -> list[dict]:
    """
    Extrae una paleta de colores dominantes de una imagen.

    Args:
        image_path: Ruta al archivo de imagen.
        n_colors:   Cantidad de colores a extraer (default: 6, rango recomendado: 3-10).

    Returns:
        Lista de dicts ordenada por porcentaje descendente:
        [{"hex": "#rrggbb", "rgb": [r, g, b], "percentage": float}, ...]

    Raises:
        ValueError: Si OpenCV no puede leer el archivo.
    """
    # 1. Leer imagen en formato BGR
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {image_path}")

    # 2. Redimensionar si el lado más largo supera 400px
    #    (acelera el clustering sin afectar la calidad de la paleta)
    h, w = img.shape[:2]
    max_side = max(h, w)
    if max_side > 400:
        scale = 400 / max_side
        img = cv2.resize(
            img,
            (int(w * scale), int(h * scale)),
            interpolation=cv2.INTER_AREA,
        )

    # 3. Convertir de BGR a LAB
    #    LAB es perceptualmente uniforme: distancias iguales = diferencias iguales al ojo humano.
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # 4. Aplanar a array 2D (n_pixels, 3)
    pixels = img_lab.reshape(-1, 3).astype(np.float32)

    # 5. Clustering con MiniBatchKMeans en espacio LAB
    kmeans = MiniBatchKMeans(n_clusters=n_colors, random_state=42, n_init=3)
    labels = kmeans.fit_predict(pixels)
    centroids = kmeans.cluster_centers_

    # 6. Convertir cada centroide de LAB a RGB y calcular porcentaje
    palette = []
    total_pixels = len(labels)

    for i, centroid in enumerate(centroids):
        # Reconvertir LAB → BGR → RGB
        lab_pixel = centroid.reshape(1, 1, 3).astype(np.uint8)
        bgr_pixel = cv2.cvtColor(lab_pixel, cv2.COLOR_LAB2BGR)
        b, g, r = bgr_pixel[0, 0]

        # 7. Porcentaje de píxeles que pertenecen a este cluster
        percentage = round(float(np.sum(labels == i) / total_pixels * 100), 2)

        palette.append(
            {
                "hex": f"#{int(r):02x}{int(g):02x}{int(b):02x}",
                "rgb": [int(r), int(g), int(b)],
                "percentage": percentage,
            }
        )

    # 8. Ordenar por porcentaje descendente (color más dominante primero)
    palette.sort(key=lambda c: c["percentage"], reverse=True)

    return palette
