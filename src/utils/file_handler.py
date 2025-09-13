import json
import os
from datetime import datetime
from typing import List, Dict

class FileHandler:
    def __init__(self, base_dir: str = "data"):
        """初始化文件处理器
        Args:
            base_dir: 数据存储的基础目录
        """
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def save_songs(self, songs: List[Dict]) -> str:
        """保存歌曲列表到JSON文件
        Args:
            songs: 歌曲列表
        Returns:
            保存的文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hot_songs_{timestamp}.json"
        filepath = os.path.join(self.base_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(songs, f, ensure_ascii=False, indent=2)
        
        return filepath
