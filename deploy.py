from vertexai import agent_engines
from customer_service.agent import root_agent
import vertexai
from vertexai.preview import reasoning_engines
import os 

PROJECT_ID = "grounded-tine-454414-b2"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://grounded-tine-454414-b2-adk-customer-service-staging"
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 1. Initialize Vertex AI
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

# 2. Prepare your agent for Agent Engine using AdkApp
app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

print("\n--- Iniciando Despliegue en Agent Engine ---")
try:
    remote_app = agent_engines.create(
        agent_engine=root_agent,
        requirements=[
            "google-cloud-aiplatform[reasoningengine,adk]==1.88.0",
            "python-dotenv==1.1.0",
            "pydantic-settings>=2.0.0",
            "google_api_python_client==2.160.0",
            "pydantic==2.11.4",
            "cloudpickle==3.1.1",
            "protobuf==6.30.2",
            "pytz==2024.2",    
        ]        
    )

    print(f"\nAgent Engine desplegado con éxito: {remote_app.name}")
    print(f"Nombre del recurso: {remote_app.resource_name}")
    print(f"Puedes ver y administrar tu Agent Engine en la consola de Google Cloud:")
    print(f"https://console.cloud.google.com/vertex-ai/agent-engine/locations/{LOCATION}/reasoning-engines/{remote_app.name}?project={PROJECT_ID}")

except Exception as e:
    print(f"\nError durante el despliegue del Agent Engine: {e}")
    import traceback
    traceback.print_exc()
print("\n--- Proceso de Despliegue Finalizado ---")