# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

PROJECT_NAME = "Agente Multimodal"

# ==========================================
# GEMMA / OLLAMA
# ==========================================

GEMMA_MODEL = "gemma3:4b"

OLLAMA_URL = "http://127.0.0.1:11434"

OLLAMA_TIMEOUT = 900


# ==========================================
# WHISPER
# ==========================================

WHISPER_MODEL = "base"

WHISPER_LANGUAGE = "es"

WHISPER_FP16 = False


# ==========================================
# VOZ
# ==========================================

VOICE_SAMPLE_RATE = 16000

VOICE_CHANNELS = 1

VOICE_BLOCK_SIZE = 1024

VOICE_SILENCE_THRESHOLD = 0.01

VOICE_SILENCE_DURATION = 1.0

VOICE_MAX_DURATION = 20.0

# Palabras que, al ser reconocidas por Whisper, terminan el
# bucle de main.py sin pasar por el Voice Agent / Orchestrator.
VOICE_EXIT_KEYWORDS = (
    "salir",
    "salir del programa",
    "cerrar programa",
    "terminar programa",
    "finalizar programa",
)

# Fragmentos de nombre (en minúsculas) usados para preferir un
# dispositivo de entrada de audio específico. Vacío por defecto:
# cualquier equipo puede definir aquí sus propios auriculares o
# micrófono preferido sin tocar services/voice_recorder.py.
# Ejemplo: ("jbl", "headset", "bluetooth")
VOICE_PREFERRED_INPUT_TOKENS: tuple = ()

# Fragmentos de nombre a evitar al autoseleccionar un dispositivo
# de entrada (dispositivos virtuales, de loopback o de salida mal
# reportados como entrada por el sistema operativo).
VOICE_EXCLUDED_INPUT_TOKENS = (
    "output",
    "speaker",
    "altavoces",
    "playback",
    "asignador de sonido",
    "microsoft - input",
    "virtual",
    "loopback",
)


# ==========================================
# RUTAS - ENTRADA
# ==========================================

INPUT_PATH = "data/input"

DEFAULT_IMAGE_INPUT = "data/input/prueba.jpg"

DEFAULT_AUDIO_INPUT = "data/input/prueba.mp3"


# ==========================================
# RUTAS - SALIDA
# ==========================================

OUTPUT_PATH = "data/output"

VOICE_TEMP_PATH = "data/temp/voz_actual.wav"

IMAGEN_JSON_PATH = "data/output/imagen.json"

AUDIO_JSON_PATH = "data/output/audio.json"

CONSOLIDADO_JSON_PATH = "data/output/consolidado.json"

INFORME_JSON_PATH = "data/output/informe.json"

KNOWLEDGE_JSON_PATH = "data/output/knowledge.json"

GRAFO_SIMPLE_PATH = "data/output/grafo.graphml"

GRAFO_CONOCIMIENTO_PATH = "data/output/grafo_conocimiento.graphml"

REPORT_OUTPUT = "data/output/informe_voz.pdf"

# ==========================================
# OBSIDIAN
# ==========================================

# Carpeta que se utilizará como Vault de Obsidian.
# Se puede cambiar por una ruta absoluta de Windows si ya tienes
# un Vault existente, por ejemplo:
# OBSIDIAN_VAULT_PATH = r"C:\\Users\\HP\\Documents\\MiVault"
OBSIDIAN_VAULT_PATH = "data/output/obsidian_vault"
