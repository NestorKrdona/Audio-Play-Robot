# Configuración de Aplicación Flask con Inicio Automático

Este documento proporciona una guía para configurar una aplicación Flask que se inicia automáticamente con el arranque del sistema utilizando `crontab`.

## Requisitos

- **Python** (versión 3.6 o superior)
- **Pip** (gestor de paquetes para Python)
- **Flask** (para crear la aplicación web)
- **Pygame** (para reproducir audio)
- **Crontab** (para la programación de tareas en Linux)

## Instalación de Dependencias

1. **Instalar Flask y Pygame**:

    ```bash
    pip install flask pygame
    ```

2. **Crear el Entorno Virtual** (opcional pero recomendado):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    Luego instala las dependencias dentro del entorno virtual.

## Creación de la Aplicación Flask

1. **Estructura del Proyecto**:

    ```
    /your_project_directory
        /static
            styles.css
        /templates
            index.html
        app.py
        start_flask_app.sh
    ```

2. **Archivo `app.py`**:

    ```python
    from flask import Flask, render_template, request, jsonify
    import pygame
    import threading

    app = Flask(__name__)

    # Configurar los archivos MP3
    audio_files = {
        "audio1": "ruta/a/tu/primer_archivo_de_audio.mp3",
        "audio2": "ruta/a/tu/segundo_archivo_de_audio.mp3"
    }

    # Inicializar el mezclador de pygame
    pygame.mixer.init()
    current_audio = None

    def play_audio(file):
        global current_audio
        if current_audio != file:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)  # Reproducir en bucle infinito
            current_audio = file

    def stop_audio():
        global current_audio
        if current_audio:
            pygame.mixer.music.stop()
            current_audio = None

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/play/<audio_name>', methods=['POST'])
    def play(audio_name):
        if audio_name in audio_files:
            play_audio(audio_files[audio_name])
            return jsonify({"status": "playing", "audio": audio_name})
        else:
            return jsonify({"status": "error", "message": "Audio not found"}), 404

    @app.route('/stop', methods=['POST'])
    def stop():
        stop_audio()
        return jsonify({"status": "stopped"})

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
    ```

3. **Archivo `index.html`** (en la carpeta `/templates`):

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Control de Audio</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
        <script>
            function playAudio(audioName) {
                fetch(`/play/${audioName}`, { method: 'POST' })
                    .then(response => response.json())
                    .then(data => console.log(data));
            }

            function stopAudio() {
                fetch('/stop', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => console.log(data));
            }
        </script>
    </head>
    <body>
        <h1>Control de Audio</h1>
        <button onclick="playAudio('audio1')">Reproducir Audio 1</button>
        <button onclick="playAudio('audio2')">Reproducir Audio 2</button>
        <button class="stop" onclick="stopAudio()">Detener</button>
    </body>
    </html>
    ```

4. **Archivo `styles.css`** (en la carpeta `/static`):

    ```css
    /* styles.css */
    body {
        font-family: Arial, sans-serif;
        text-align: center;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
    }

    h1 {
        color: #333;
        margin-top: 50px;
    }

    button {
        background-color: #4CAF50; /* Verde */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 10px;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #45a049; /* Verde más oscuro */
    }

    button.stop {
        background-color: #f44336; /* Rojo */
    }

    button.stop:hover {
        background-color: #d32f2f; /* Rojo más oscuro */
    }
    ```

## Configuración de Inicio Automático con Crontab

1. **Crear un Script de Inicio**:

    Crea un archivo llamado `start_flask_app.sh` en `/home/tu_usuario/scripts/` con el siguiente contenido:

    ```bash
    #!/bin/bash

    # Ruta al entorno virtual si estás usando uno
    # source /home/tu_usuario/venv/bin/activate

    # Ruta a tu archivo de aplicación Flask
    cd /home/tu_usuario/tu_proyecto

    # Ejecutar la aplicación Flask
    /usr/bin/python3 app.py >> /home/tu_usuario/tu_proyecto/app.log 2>&1
    ```

2. **Hacer el Script Ejecutable**:

    ```bash
    chmod +x /home/tu_usuario/scripts/start_flask_app.sh
    ```

3. **Editar el Crontab**:

    Ejecuta el siguiente comando para editar el crontab:

    ```bash
    crontab -e
    ```

    Agrega la siguiente línea al final del archivo del crontab:

    ```bash
    @reboot /home/tu_usuario/scripts/start_flask_app.sh
    ```

4. **Verificar el Crontab**:

    Asegúrate de que el crontab esté configurado correctamente:

    ```bash
    crontab -l
    ```

5. **Reiniciar el Sistema**:

    Para probar que el crontab funciona correctamente, reinicia tu sistema:

    ```bash
    sudo reboot
    ```

6. **Verificar los Logs**:

    Después de que el sistema se reinicie, verifica el archivo `app.log` para asegurarte de que la aplicación Flask se haya iniciado correctamente:

    ```bash
    cat /home/tu_usuario/tu_proyecto/app.log
    ```

## Notas Adicionales

- **Entorno Virtual**: Si usas un entorno virtual, activa el entorno en el script de inicio. Ajusta la ruta en el script `start_flask_app.sh` según tu configuración.
- **Permisos**: Asegúrate de que el script y los archivos tengan los permisos adecuados.
- **Rutas Absolutas**: Usa rutas absolutas en el script y el archivo `crontab` para evitar problemas relacionados con el entorno del sistema.

Este archivo `README.md` proporciona una guía completa para configurar y automatizar el inicio de una aplicación Flask. Asegúrate de ajustar las rutas y configuraciones según tus necesidades específicas.
