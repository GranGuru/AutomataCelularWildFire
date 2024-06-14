import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Definir dimensiones de las imágenes
IMAGE_HEIGHT = 128
IMAGE_WIDTH = 128
N_IMAGE_CHANNELS = 3

# Colores únicos en la máscara de ejemplo
class_colors = {
    'Árboles': (10, 73, 39),  # verde oscuro
    'Plantas no árboles': (98, 158, 98),  # Verde
    'Clase 3': (142, 122, 158),  # Morado - Carreteras
    'Casas': (246, 146, 0),  # Naranja - Casas
    'Caminos de tierra': (80, 48, 0)  # Marrón - Caminos, tierra
}

class_colors_array = np.array(list(class_colors.values()), dtype=np.uint8)


# Función para convertir la máscara de etiquetas de clase a colores
def class_to_color(mask, class_colors_array):
    color_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    for class_index in range(len(class_colors_array)):
        color_mask[mask == class_index] = class_colors_array[class_index]
    return color_mask


# Definición de las funciones personalizadas utilizadas en el modelo
def dice_coefficient(y_true, y_pred, smooth=1):
    y_true = tf.one_hot(tf.squeeze(tf.cast(y_true, tf.int32), axis=-1), depth=len(class_colors))
    y_pred = tf.cast(y_pred, tf.float32)

    y_true_f = tf.keras.backend.flatten(y_true)
    y_pred_f = tf.keras.backend.flatten(y_pred)

    intersection = tf.keras.backend.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (tf.keras.backend.sum(y_true_f) + tf.keras.backend.sum(y_pred_f) + smooth)


def dice_loss(y_true, y_pred):
    return 1 - dice_coefficient(y_true, y_pred)


# Definición del bloque Encoder y Decoder
@tf.keras.utils.register_keras_serializable()
class EncoderBlock(tf.keras.layers.Layer):
    def __init__(self, filters: int, max_pool: bool = True, rate=0.2, **kwargs):
        super().__init__(**kwargs)
        self.filters = filters
        self.max_pool = max_pool
        self.rate = rate
        self.max_pooling = tf.keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2))
        self.conv1 = tf.keras.layers.Conv2D(filters=filters, kernel_size=3, strides=1, padding='same',
                                            activation='relu', kernel_initializer='he_normal')
        self.conv2 = tf.keras.layers.Conv2D(filters=filters, kernel_size=3, strides=1, padding='same',
                                            activation='relu', kernel_initializer='he_normal')
        self.drop = tf.keras.layers.Dropout(rate)
        self.bn = tf.keras.layers.BatchNormalization()

    def call(self, inputs):
        x = self.bn(inputs)
        x = self.conv1(x)
        x = self.drop(x)
        x = self.conv2(x)
        if self.max_pool:
            y = self.max_pooling(x)
            return y, x
        else:
            return x

    def get_config(self):
        config = super().get_config()
        config.update({
            'filters': self.filters,
            'max_pool': self.max_pool,
            'rate': self.rate
        })
        return config


@tf.keras.utils.register_keras_serializable()
class DecoderBlock(tf.keras.layers.Layer):
    def __init__(self, filters: int, rate: float = 0.2, **kwargs):
        super().__init__(**kwargs)
        self.filters = filters
        self.rate = rate
        self.convT = tf.keras.layers.Conv2DTranspose(filters=filters, kernel_size=3, strides=2, padding='same',
                                                     activation='relu', kernel_initializer='he_normal')
        self.bn = tf.keras.layers.BatchNormalization()
        self.net = EncoderBlock(filters=filters, rate=rate, max_pool=False)

    def call(self, inputs):
        x, skip_x = inputs
        x = self.bn(x)
        x = self.convT(x)
        if x.shape[1] != skip_x.shape[1] or x.shape[2] != skip_x.shape[2]:
            skip_x = tf.image.resize_with_crop_or_pad(skip_x, x.shape[1], x.shape[2])
        x = tf.keras.layers.Concatenate(axis=-1)([x, skip_x])
        x = self.net(x)
        return x

    def get_config(self):
        config = super().get_config()
        config.update({
            'filters': self.filters,
            'rate': self.rate,
        })
        return config