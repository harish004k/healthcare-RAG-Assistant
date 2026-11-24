import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_api_version: str
    azure_openai_chat_deployment: str
    azure_openai_embedding_deployment: str
    azure_search_endpoint: str
    azure_search_api_key: str
    azure_search_index_name: str
    azure_storage_connection_string: str
    azure_storage_container: str

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", ""),
            azure_openai_chat_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", ""),
            azure_openai_embedding_deployment=os.getenv(
                "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", ""
            ),
            azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT", ""),
            azure_search_api_key=os.getenv("AZURE_SEARCH_API_KEY", ""),
            azure_search_index_name=os.getenv("AZURE_SEARCH_INDEX_NAME", ""),
            azure_storage_connection_string=os.getenv(
                "AZURE_STORAGE_CONNECTION_STRING", ""
            ),
            azure_storage_container=os.getenv("AZURE_STORAGE_CONTAINER", ""),
        )

    def missing_for_search(self) -> list[str]:
        required = (
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_CHAT_DEPLOYMENT",
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
            "AZURE_SEARCH_ENDPOINT",
            "AZURE_SEARCH_API_KEY",
            "AZURE_SEARCH_INDEX_NAME",
        )
        return [name for name in required if not getattr(self, _setting_field(name))]

    def missing_for_blob(self) -> list[str]:
        required = (
            "AZURE_STORAGE_CONNECTION_STRING",
            "AZURE_STORAGE_CONTAINER",
        )
        return [name for name in required if not getattr(self, _setting_field(name))]


def _setting_field(environment_name: str) -> str:
    return environment_name.lower()
