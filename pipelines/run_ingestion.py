import time
from datetime import datetime, timedelta
from loguru import logger
from astrostudy.utils.logger import setup_logger
from astrostudy.ingestion.nasa_client import NASAClient
from astrostudy.ingestion.saver import DataSaver

def main():
    """
    Orquestrador do Pipeline de Ingestão.
    Lida com chunking, validação, cronometragem e persistência.
    """
    setup_logger()
    logger.info("🚀 Iniciando Pipeline de Ingestão (Modo Senior)")
    
    start_time_total = time.time()
    
    # 🎯 CONFIGURAÇÃO CONTROLADA: 365 dias para análise física e estatística profunda
    days_to_collect = 365
    today = datetime.now()
    end_dt = today
    start_dt = today - timedelta(days=days_to_collect - 1)
    
    client = NASAClient()
    saver = DataSaver()
    
    # Lógica de Chunking (7 dias max por request na NASA)
    current_start = start_dt
    total_records = 0
    
    while current_start <= end_dt:
        chunk_end = min(current_start + timedelta(days=6), end_dt)
        s_str = current_start.strftime("%Y-%m-%d")
        e_str = chunk_end.strftime("%Y-%m-%d")
        
        logger.info(f"🛰️ Coletando chunk: {s_str} até {e_str}")
        
        try:
            chunk_start_time = time.time()
            data = client.get_feed(s_str, e_str)
            duration = time.time() - chunk_start_time
            
            if not data:
                logger.warning(f"Nenhum dado retornado para o período {s_str} a {e_str}")
                current_start = chunk_end + timedelta(days=1)
                continue

            neos = data.get("near_earth_objects", {})
            
            # Itera sobre os dias do chunk para salvar individualmente
            for date_str, asteroids in neos.items():
                saved = saver.save_daily_data(
                    date_str=date_str,
                    asteroids=asteroids,
                    metadata={"api_status": "SUCCESS", "duration_sec": round(duration, 2)}
                )
                if saved:
                    total_records += len(asteroids)
            
            logger.info(f"⏱️ Chunk finalizado em {duration:.2f}s")
            
        except Exception as e:
            logger.error(f"❌ Falha crítica no processamento do chunk {s_str}: {e}")
            # Em produção, poderíamos continuar para o próximo chunk ou parar
            break
            
        current_start = chunk_end + timedelta(days=1)

    total_duration = time.time() - start_time_total
    logger.success(f"✅ Pipeline finalizado! Total de registros: {total_records} | Tempo total: {total_duration:.2f}s")

if __name__ == "__main__":
    main()
