import re
import os
from typing import List, Tuple

class MacAddress:
    """Классы для работы с Mac-адресами"""

    MAC_Pattern = re.compile( #Поиск MAC-адресов
        r'(?:[0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})]' #Формат ХХ:ХХ:ХХ:ХХ:ХХ и ХХ-ХХ-ХХ-ХХ-ХХ
    )

    Strict_MAC_Pattern = re.compile( #Валидация MAC-адресов
        r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|'
    )

    def find_mac_address(self, text: str) -> List[str]:
        """Нахождение MAC-адресов"""
        return self.MAC_Pattern.findall(text)

    def is_valid_mac(self, mac_address: str) -> bool:
        """Проверкка является ли строка MAC-адресом"""
        return bool(self.Strict_MAC_Pattern.match(mac_address.strip()))

    def extract_mac_from_text(self, text: str) -> Tuple[List[str], List[str]]:
        """Извлечение из текста MAC-адресов"""
        all_found = self.find_mac_address(text)
        valid_macs = [mac for mac in all_found if self.is_valid_mac(mac)]
        return valid_macs, all_found

    def extract_mac_from_file(self, file_path: str) -> Tuple[List[str], List[str]]:
        """Извлечение из файла MAC-адресов"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        try:
            with open(file_path, "r", encoding = 'utf-8', errors = 'ignore') as file:
                content = file.read()
        except Exception as e:
            raise IOError(f"Ошибка чтения файла {e}")

        return self.extract_mac_from_text(content)