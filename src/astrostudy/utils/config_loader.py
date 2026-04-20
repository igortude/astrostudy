import yaml
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

def load_config(config_path: str = "config/config.yaml") -> dict[str, Any]:
    """Carrega o arquivo de configuração YAML."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")
    
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_env_variable(var_name: str) -> str:
    """Obtém uma variável de ambiente do arquivo .env."""
    load_dotenv()
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Variável de ambiente {var_name} não definida.")
    return value
