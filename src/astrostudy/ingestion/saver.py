import json
from pathlib import Path
from datetime import datetime
from loguru import logger
from typing import Any

class DataSaver:
    """
    Responsável pela persistência segura e auditável dos dados brutos.
    
    SEPARAÇÃO DE RESPONSABILIDADE: Este módulo cuida apenas de I/O e 
    integridade do sistema de arquivos, permitindo que o Client foque apenas na API.
    """
    
    def __init__(self, base_path: str = "data/raw"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_daily_data(self, date_str: str, asteroids: list[dict], metadata: dict[str, Any]) -> bool:
        """
        Salva os dados de um dia específico com controle de duplicidade e metadados.
        
        RETORNA: True se salvou, False se o arquivo já existia (evita sobrescrita).
        """
        file_path = self.base_path / f"{date_str}.json"
        
        # 1. CONTROLE DE DUPLICIDADE (Idempotência)
        if file_path.exists():
            logger.warning(f"Arquivo já existe para a data {date_str}. Pulando para evitar duplicidade.")
            return False
            
        # 2. ENRIQUECIMENTO COM METADADOS (Auditoria)
        # Isso transforma um simples JSON em um registro auditável.
        document = {
            "metadata": {
                "collection_timestamp": datetime.now().isoformat(),
                "records_count": len(asteroids),
                "source_api": metadata.get("source_api", "NASA NeoWs"),
                "api_status": metadata.get("api_status", "SUCCESS")
            },
            "data": {
                "date": date_str,
                "asteroids": asteroids
            }
        }
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(document, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Dados salvos: {date_str} | Registros: {len(asteroids)}")
            return True
            
        except Exception as e:
            logger.error(f"Falha ao persistir dados de {date_str}: {e}")
            raise
