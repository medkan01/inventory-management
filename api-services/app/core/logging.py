"""
Configuration du système de logging pour l'application.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure le logging pour l'application.
    
    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    
    # Créer le dossier logs s'il n'existe pas
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Format du log
    log_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)8s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Handler console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    
    # Handler fichier avec rotation automatique
    file_handler = RotatingFileHandler(
        filename="logs/app.log",
        maxBytes=10_000_000,  # 10 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    
    # Configuration du root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Réduire le bruit des librairies tierces
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Retourne un logger pour le module spécifié.
    
    Usage:
        logger = get_logger(__name__)
        logger.info("Message")
    
    Args:
        name: Nom du module (utilisez __name__)
    
    Returns:
        Logger configuré
    """
    return logging.getLogger(name)
