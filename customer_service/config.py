"""Configuration module for the customer service agent."""
import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AgentModel(BaseModel):
    """Agent model settings."""

    name: str = Field(default="Camila")
    model: str = Field(default="gemini-2.0-flash-001")


class Config(BaseSettings):
    """Configuration settings for agent."""
    GOOGLE_SERVICE_ACCOUNT_FILE: str = "service_account.json"
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../.env"
        ),
        env_prefix="GOOGLE_",
        case_sensitive=True,
    )
    agent_settings: AgentModel = Field(default=AgentModel())
    app_name: str = "customer_service_app"
    CLOUD_PROJECT: str = Field(default="grounded-tine-454414-b2")
    CLOUD_LOCATION: str = Field(default="us-central1")
    CLOUD_STAGING_BUCKET: str = Field(default="gs://grounded-tine-454414-b2-adk-customer-service-staging")
    GENAI_USE_VERTEXAI: str = Field(default="1")
    API_KEY: str | None = Field(default="")
