import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger
from typing import Any
from astrostudy.utils.config_loader import get_env_variable

class NASAClient:
    """
    Cliente focado EXCLUSIVAMENTE na comunicação com a API da NASA.
    Seguindo o princípio de Responsabilidade Única (SRP).
    """
    
    def __init__(self):
        self.api_key = get_env_variable("NASA_API_KEY")
        self.base_url = get_env_variable("NASA_BASE_URL")
        self.session = self._build_session()
        
    def _build_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def get_feed(self, start_date: str, end_date: str) -> dict[str, Any]:
        """
        Busca o feed de asteroides. 
        VALIDAÇÃO: Garante que a estrutura básica está presente antes de retornar.
        """
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key
        }
        
        try:
            response = self.session.get(f"{self.base_url}/feed", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # VALIDAÇÃO DE DADOS (Sanity Check)
            if "near_earth_objects" not in data:
                logger.error(f"Resposta da API incompleta para o período {start_date} a {end_date}")
                return {}
                
            return data
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP na API NASA: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado na chamada da API: {e}")
            raise
