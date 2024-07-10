# Sistema Integrado de Simulación y Gestión de Incendios mediante Fotogrametría e Inteligencia Artificial

![Imagen de Portada](images/portada.png)

## Insignias

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/release/python-310/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0.1-brightgreen)](https://www.pygame.org/news)
[![NumPy](https://img.shields.io/badge/NumPy-1.21.0-blue)](https://numpy.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5.2-green)](https://opencv.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.5-orange)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-2.4.3-red)](https://keras.io/)
[![PyCharm](https://img.shields.io/badge/PyCharm-2021.1-yellowgreen)](https://www.jetbrains.com/pycharm/)

## Índice

- [Título e imagen de portada](#Título-e-imagen-de-portada)
- [Insignias](#insignias)
- [Índice](#índice)
- [Descripción del proyecto](#descripción-del-proyecto)
- [Estado del proyecto](#Estado-del-proyecto)
- [Características de la aplicación y demostración](#Características-de-la-aplicación-y-demostración)
- [Acceso al proyecto](#acceso-proyecto)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Personas Contribuyentes](#personas-contribuyentes)
- [Personas-Desarrolladores del Proyecto](#personas-desarrolladores)
- [Licencia](#licencia)
- [Conclusión](#conclusión)

## Descripción del proyecto

Este proyecto es un sistema integrado que utiliza técnicas de fotogrametría e inteligencia artificial para simular y gestionar incendios. La simulación de fuego se basa en un autómata celular, mientras que el mapa de riesgo se genera mediante una red profunda U-Net para segmentar imágenes. Cada imagen sirve como red de células para los autómatas celulares, utilizando una heurística que depende de la segmentación y el análisis pixel a pixel.

El dataset utilizado ha sido de creación propia, compuesto por 8600 imágenes y sus respectivas 8600 máscaras, de imágenes aéreas de la Sierra de Madrid. Para su creación se ha utilizado el software GIMP y Python, con cada imagen teniendo un tamaño de 512x512.

### Data Augmentation

Para el entrenamiento de la red profunda U-Net, se han utilizado las siguientes técnicas de data augmentation:

- **Rotación**: Se rotan las imágenes en ángulos aleatorios para simular diferentes orientaciones de las escenas.
- **Traslación**: Se desplazan las imágenes horizontal y verticalmente para cambiar la posición de los objetos.
- **Escalado**: Se modifican las dimensiones de las imágenes para simular diferentes distancias de la cámara.
- **Volteo Horizontal y Vertical**: Se invierten las imágenes horizontal y verticalmente para aumentar la variabilidad.
- **Cambio de Brillo y Contraste**: Se ajustan los niveles de brillo y contraste para simular diferentes condiciones de iluminación.

## Estado del proyecto

Actualmente, el proyecto está en fase de desarrollo. Se han implementado las características básicas, pero se están realizando mejoras y optimizaciones continuas.

## Características de la aplicación y demostración

- Simulación de propagación de fuego basada en autómatas celulares.
- Control de dirección e intensidad del viento en tiempo real.
- Diferentes tipos de suelo con distintos niveles de riesgo de incendio.
- Visualización gráfica interactiva utilizando Pygame.

## Acceso al proyecto

Puedes acceder al proyecto clonando el repositorio desde GitHub:

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
pip install -r requirements.txt
python main.py
