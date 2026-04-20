from loguru import logger
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

def setup_logger() -> None:
    """Configura logging estruturado para console e arquivo."""
    load_dotenv()
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    # Remove o handler padrão
    logger.remove()
    
    # Console: legível para humanos
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> — <level>{message}</level>",
        colorize=True,
    )
    
    # Arquivo: estruturado
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / "astrostudy_{time:YYYY-MM-DD}.log"
    
    logger.add(
        str(log_path),
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} — {message}",
        rotation="1 day",
        retention="30 days",
        compression="zip",
        enqueue=True,
    )
    
    logger.info(f"Logger configurado com nível: {log_level}")
