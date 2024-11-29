import logging
from datetime import datetime

class GameLogger:
    def __init__(self):
        self.logger = logging.getLogger('TestamentDuel')
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(f'logs/game_{datetime.now():%Y%m%d_%H%M%S}.log')
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch) 