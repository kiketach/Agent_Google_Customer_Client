import vertexai
from vertexai import agent_engines

# --- Configuración del Proyecto ---
PROJECT_ID = "grounded-tine-454414-b2"
LOCATION = "us-central1"
AGENT_ENGINE_RESOURCE_NAME = "projects/148419107362/locations/us-central1/reasoningEngines/3159635778414313472"

print("--- Inicializando Vertex AI para interactuar con el Agent Engine desplegado ---")
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)
print("Vertex AI inicializado.")

print(f"\n--- Obteniendo el Agent Engine: {AGENT_ENGINE_RESOURCE_NAME} ---")
try:
    # Usamos agent_engines.get() para obtener el RemoteAgent
    remote_agent_engine = agent_engines.get(AGENT_ENGINE_RESOURCE_NAME)
    print(f"Agent Engine obtenido: {remote_agent_engine.name}")
    print(f"Display Name: {remote_agent_engine.display_name}")

    print("\n--- Creando Sesión Remota ---")
    session = remote_agent_engine.create_session(user_id="remote_user_001")
    print(f"Sesión remota creada: {session}")
    print(f"ID de la sesión: {session['id']}") # Acceder como diccionario


    # Envía consultas a tu agente (remoto)
    print("\n--- Enviando Consulta Remota (stream_query) ---")
    query_message = "Hola Camila, ¿qué modelos de zapatillas de cuero tienes para detal?"

    print(f"Enviando mensaje al agente desplegado: '{query_message}'")
    for event in remote_agent_engine.stream_query(
        user_id="remote_user_001", # Debe coincidir con el user_id de la sesión si la sesión es relevante
        session_id=session['id'], # Acceder como diccionario
        message=query_message,
    ):
        print(event)

except Exception as e:
    print(f"Ocurrió un error al interactuar con el Agent Engine desplegado: {e}")
    import traceback
    traceback.print_exc()
print("\n--- Fin de la interacción remota ---")
