# Microservicio-clima
[Microservicio de Clima para la aplicación Chatbot Granja](https://github.com/joaquinuc150/microservicio-clima)

- Debora Alayo
- Joaquín Gatica

## Pre-Instalación

El sistema utiliza como variable de entorno una API-KEY del RapidApi para obtener el clima actual de las ciudades:

- Ingresar a [WeatherAPI](https://rapidapi.com/weatherapi/api/weatherapi-com), suscribirse al servicio y ingresar como variable de entorno el RAPID_KEY.

- Crear archivo .env dentro de la carpeta /app, con la variable de entorno RAPID_KEY='API-KEY-DE-RapidAPI'

*Para no crear cuenta, utilizar .env que se encuentra en la entrega de aula*

## Como usar

El sistema se debe ejecutar en el siguiente orden:

- Crear network:
  
      docker network create microsvcs


- Primero ejecutar el message_broker en la carpeta message_broker

      // Servicio RabbitMQ
      cd message_broker
      docker-compose up --build
  
- Luego, ejecutar los dos servicios, clima y usuario (usuario siendo un servicio simple que solo recibe eventos)

      // Servicio Clima
      docker-compose up --build

      // Servicio Usuarios
      cd service_users
      docker-compose up --build

- Para ingresar al servicio clima, ingresar a [localhost:80/docs](localhost:80/docs) para ver documentación del servicio.