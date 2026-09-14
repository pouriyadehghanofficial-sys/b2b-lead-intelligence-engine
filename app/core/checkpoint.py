"""Checkpoint and resume functionality"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class CheckpointManager:
    """Manage pipeline checkpoints for resume capability"""
    
    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        Path(checkpoint_dir).mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(
        self,
        name: str,
        data: Dict,
        step: str = None,
    ) -> str:
        """Save a checkpoint"""
        try:
            checkpoint_data = {
                'name': name,
                'step': step or 'unknown',
                'timestamp': datetime.now().isoformat(),
                'data': data,
            }
            
            filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.checkpoint_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Checkpoint saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Checkpoint save failed: {str(e)}")
            raise
    
    def load_checkpoint(self, name: str) -> Optional[Dict]:
        """Load latest checkpoint by name"""
        try:
            # Find latest checkpoint with this name
            checkpoints = []
            for file in os.listdir(self.checkpoint_dir):
                if file.startswith(name):
                    checkpoints.append(os.path.join(self.checkpoint_dir, file))
            
            if not checkpoints:
                logger.warning(f"No checkpoint found: {name}")
                return None
            
            # Load latest
            latest = max(checkpoints, key=os.path.getctime)
            with open(latest, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Checkpoint loaded: {latest}")
            return data
            
        except Exception as e:
            logger.error(f"Checkpoint load failed: {str(e)}")
            return None
    
    def get_last_checkpoint_step(self, name: str) -> Optional[str]:
        """Get the last checkpoint step"""
        checkpoint = self.load_checkpoint(name)
        if checkpoint:
            return checkpoint.get('step')
        return None
    
    def list_checkpoints(self) -> List[str]:
        """List all checkpoints"""
        try:
            checkpoints = []
            for file in os.listdir(self.checkpoint_dir):
                if file.endswith('.json'):
                    checkpoints.append(file)
            return sorted(checkpoints)
        except Exception as e:
            logger.error(f"Error listing checkpoints: {str(e)}")
            return []
