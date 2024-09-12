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
