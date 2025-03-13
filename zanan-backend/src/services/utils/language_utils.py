from typing import Dict, List
import re

class LanguageUtils:
    """语言工具类
    
    提供语言检测、翻译等通用功能。
    """
    
    @staticmethod
    def is_chinese(text: str) -> bool:
        """判断文本是否为中文
        
        参数:
            text (str): 要检测的文本
            
        返回:
            bool: 如果文本包含中文字符返回True，否则返回False
        """
        # 使用Unicode范围检测中文字符
        pattern = re.compile(r'[\u4e00-\u9fff]')
        return bool(pattern.search(text))
    
    @staticmethod
    def is_english(text: str) -> bool:
        """判断文本是否为英文
        
        参数:
            text (str): 要检测的文本
            
        返回:
            bool: 如果文本只包含英文字符返回True，否则返回False
        """
        # 使用正则表达式检测英文字符
        pattern = re.compile(r'^[a-zA-Z\s]+$')
        return bool(pattern.match(text))