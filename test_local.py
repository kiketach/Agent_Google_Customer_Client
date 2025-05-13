import vertexai
from vertexai.preview import reasoning_engines
from customer_service.agent import root_agent # Importa el agente

# --- Configuración del Proyecto ---
PROJECT_ID = "grounded-tine-454414-b2"
LOCATION = "us-central1"

print("--- Inicializando Vertex AI para pruebas locales ---")
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)
print("Vertex AI inicializado.")

print("\n--- Preparando AdkApp localmente ---")
app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)
print("AdkApp creada.")

print("\n--- Iniciando Pruebas Locales del Agente ---")
print("\n--- Creando Sesión Local ---")
try:
    session = app.create_session(user_id="test_user_001")
    print(f"Sesión creada: {session}")

    print("\n--- Listando Sesiones Locales ---")
    sessions_list = app.list_sessions(user_id="test_user_001")
    print(f"Sesiones listadas: {sessions_list}")

    print("\n--- Obteniendo Sesión Específica Local ---")
    retrieved_session = app.get_session(user_id="test_user_001", session_id=session.id)
    print(f"Sesión recuperada: {retrieved_session}")

    print("\n--- Enviando Consulta Local (stream_query) ---")
    query_message = "Hola como te llamas?"

    print(f"Enviando mensaje al agente: '{query_message}'")
    for event in app.stream_query(
        user_id="test_user_001",
        session_id=session.id,
        message=query_message,
    ):
        print(event)

except Exception as e:
    print(f"Ocurrió un error durante las pruebas locales: {e}")
    import traceback
    traceback.print_exc()
print("\n--- Fin de Pruebas Locales ---")
