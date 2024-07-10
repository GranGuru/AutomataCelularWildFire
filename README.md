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

Los incendios forestales son un tema real que afecta a todos, no solo a las personas, sino también a los animales, plantas, ecosistemas e incluso a la climatología global. Con el cambio climático, la contaminación, accidentes, incluso eventos naturales y provocados por el hombre; la probabilidad de que se inicie un incendio es constante.

Por ello, el objetivo principal de esta investigación es proporcionar una herramienta para la planificación y el entrenamiento ante emergencias de incendios forestales con la idea de crear un servicio que impacte de manera positiva en la sociedad y ayuda a combatir los incendios.

El desarrollo del proyecto se ha basado en el estudio de las investigaciones más recientes sobre incendios, simulaciones y la aplicación de tecnología de inteligencia artificial en simulaciones. Por ello, la aplicación desarrollada emplea un modelo de segmentación U-Net para generar mapas de riesgo del terreno y utiliza autómatas celulares para simular la propagación del fuego bajo diversas condiciones.

Para conseguir el objetivo de que el modelo U-Net sea fiable, se ha creado un conjunto de datos específico de áreas no urbanas con 7 clases y un total de 8600 imágenes, que permite segmentar semánticamente las imágenes aéreas que capture un dron y obtener un mapa de riesgo con preciso. El modelo alcanzó métricas de rendimiento significativas, incluyendo un coeficiente de Dice de 0.7697 y una precisión de 0.7697 en los datos de entrenamiento, con métricas de validación de 0.6952 para ambos.

La integración de técnicas avanzadas de aprendizaje profundo con simulación interactiva ofrece una plataforma adecuada para el entrenamiento y la planificación de emergencias. Este proyecto establece una sólida base para utilizar tecnologías avanzadas en la gestión de incendios forestales y presenta un potencial significativo para aplicaciones del mundo real en la preparación y respuesta ante emergencias.

Es un proyecto de Fin de Estudios del Master en Inteligencia Artificial de la universidad UNIR. Mi nombre es Antonio Adam Bejar Gladkowski, mi correo electronico es antonio.adam.bejar@hotmail.com.

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
