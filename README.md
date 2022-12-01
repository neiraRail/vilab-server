# Vilab server

Servidor Flask con api REST que recibe y gestiona la captura de eventos de un nodo vilab.

## API
- **GET status/** devuelve el estado del servidor web.
---

- **GET events/** devuelve todos los eventos que estén en la base de datos.
- **GET events/\<id>** devuelve el evento con ese id. 
- **POST events/** ingresa un evento a la base de datos.
---
- **POST files/** recibe un archivo multipart y lo guarda en el servidor.