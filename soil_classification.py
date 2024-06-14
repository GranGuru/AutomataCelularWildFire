import numpy as np
import cv2
import tensorflow as tf

# Definir los colores de las clases
class_colors = {
    'Árboles': (10, 73, 39),
    'Plantas no árboles': (98, 158, 98),
    'Clase 3': (142, 122, 158),  # Ajustar este valor según sea necesario
    'Casas': (246, 146, 0),   # Ajustado con el valor correcto identificado
    'Caminos de tierra': (80, 48, 0)  # Ajustado con el valor correcto identificado
}
index_to_class = {class_name: i for i, class_name in enumerate(class_colors.keys())}
class_colors_array = np.array(list(class_colors.values()), dtype=np.uint8)

# Nuevo diccionario de colores
label_colors = {
    0: (255, 0, 0),  # Rojo para árboles
    1: (0, 255, 0),  # Verde para plantas
    2: (255, 165, 0),  # Naranja para casas
    3: (0, 255, 255),  # Cian para caminos de tierra
    4: (255, 255, 0)  # Amarillo para la clase 3
}

# Diccionario para mapear colores a niveles de riesgo
color_to_risk = {
    (255, 0, 0): 5,  # Rojo para árboles
    (0, 255, 0): 2,  # Verde para riesgo moderado
    (255, 165, 0): 4,  # Naranja para riesgo muy alto
    (0, 255, 255): 1,  # Cian para rocas
    (255, 255, 0): 3  # Amarillo para riesgo alto
}

# Crear un diccionario para mapear las clases a niveles de riesgo
class_to_risk = {
    0: 5,  # Árboles
    1: 2,  # Plantas no árboles
    2: 4,  # Casas
    3: 1,  # Caminos de tierra
    4: 3   # Clase 3
}

# Función para convertir la máscara de etiquetas de clase a colores usando el nuevo diccionario
def class_to_new_color(mask, label_colors):
    color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    for class_index, color in label_colors.items():
        color_mask[mask == class_index] = color
    return color_mask

# Función para preprocesar la imagen y la máscara
def preprocess_image(image_path, target_size=(128, 128)):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_png(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    original_image = image  # Guardar la imagen original
    image = tf.image.resize(image, target_size)
    return image, original_image

def classify_soil(image_path, model, target_size=(128, 128)):
    # Preprocesar la imagen
    image, original_image = preprocess_image(image_path, target_size)
    image = tf.expand_dims(image, axis=0)  # Añadir dimensión de batch

    # Predecir la máscara
    pred_mask = model.predict(image, verbose=0)  # Deshabilitar la barra de progreso
    pred_mask = tf.argmax(pred_mask, axis=-1)
    pred_mask = tf.squeeze(pred_mask, axis=0)  # Eliminar la dimensión de batch

    # Redimensionar la máscara predicha a las dimensiones originales
    original_size = tf.shape(original_image)[:2]
    pred_mask = tf.image.resize(tf.expand_dims(pred_mask, axis=-1), original_size, method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    pred_mask = tf.squeeze(pred_mask, axis=-1)

    # Convertir la máscara de clases a colores usando el nuevo diccionario
    pred_mask_np = pred_mask.numpy()
    color_mask = class_to_new_color(pred_mask_np, label_colors)

    # Crear una copia coloreada de pred_mask_np para devolverla
    pred_mask_colored = np.zeros((pred_mask_np.shape[0], pred_mask_np.shape[1], 3), dtype=np.uint8)
    for class_index, color in label_colors.items():
        pred_mask_colored[pred_mask_np == class_index] = color

    # Crear el mapa de clasificación de riesgo
    img_height, img_width = pred_mask_np.shape
    risk_map = np.zeros((img_height, img_width), dtype=int)  # Inicializar mapa de riesgo con ceros
    for class_index, risk_level in class_to_risk.items():
        risk_map[pred_mask_np == class_index] = risk_level

    # Guardar las imágenes resultantes
    raw_mask_path = image_path.replace(".png", "_mask.png")
    color_mask_path = image_path.replace(".png", "_color_mask.png")
    classified_image_path = image_path.replace(".png", "_classified.png")

    cv2.imwrite(raw_mask_path, pred_mask_np)
    cv2.imwrite(color_mask_path, color_mask)
    cv2.imwrite(classified_image_path, cv2.cvtColor(color_mask, cv2.COLOR_RGB2BGR))

    print(f"Classified image saved at {classified_image_path}")
    print(f"Raw mask saved at {raw_mask_path}")
    print(f"Color mask saved at {color_mask_path}")

    # Convertir los tensores a arreglos de NumPy para el retorno
    original_image_np = original_image.numpy()
    original_image_np = (original_image_np * 255).astype(np.uint8)  # Asegurarse de que los valores estén en el rango correcto

    return original_image_np, color_mask, risk_map

def resize_and_crop_image(image, target_width, target_height):
    height, width = image.shape[:2]

    if width <= target_width and height <= target_height:
        new_width, new_height = width, height
    else:
        aspect_ratio = width / height
        target_aspect_ratio = target_width / target_height

        if (width - target_width) < (height - target_height):
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * aspect_ratio)

        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        top_border = (target_height - new_height) // 2
        bottom_border = target_height - new_height - top_border
        left_border = (target_width - new_width) // 2
        right_border = target_width - new_width - left_border

        image_with_border = cv2.copyMakeBorder(
            resized_image, top_border, bottom_border, left_border, right_border,
            cv2.BORDER_CONSTANT, value=[0, 0, 0]
        )
        return image_with_border

    top_border = (target_height - new_height) // 2
    bottom_border = target_height - new_height - top_border
    left_border = (target_width - new_width) // 2
    right_border = target_width - new_width - left_border
    image_with_border = cv2.copyMakeBorder(image, top_border, bottom_border, left_border, right_border,
                                           cv2.BORDER_CONSTANT, value=[0, 0, 0])
    return image_with_border

def process_new_image(file_path, model):
    new_image = cv2.imread(file_path)
    if new_image is not None:
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        target_width = 1643
        target_height = 995
        new_image = resize_and_crop_image(new_image, target_width, target_height)
        return classify_soil(file_path, model)

    return None, None, None
