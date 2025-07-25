
# Chatbot con Azure OpenAI y Flask

Este es un chatbot funcional que utiliza Azure OpenAI (modelo GPT) y Flask como framework web.

## Configuración

1. Clona este repositorio.
2. Crea un archivo `.env` y agrega:
    - `ENDPOINT_URL`
    - `DEPLOYMENT_NAME`
    - `AZURE_OPENAI_API_KEY`
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar localmente

```bash
python app.py
```

## Desplegar en Azure App Service

1. Sube todos los archivos.
2. Asegúrate de usar `startup.txt` como comando de inicio.
3. Configura las variables del entorno desde el portal de Azure.

## Estructura

- `app.py`: lógica del servidor
- `templates/chat.html`: interfaz HTML
- `static/style.css`: estilos CSS
