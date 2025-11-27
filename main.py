import re
import urllib.request
import os
from typing import List

class MacAddress:
    """Классы для работы с Mac-адресами"""

    MAC_Pattern = re.compile( #Поиск MAC-адресов
        r'(?:[0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})]' #Формат ХХ:ХХ:ХХ:ХХ:ХХ и ХХ-ХХ-ХХ-ХХ-ХХ
    )

    Strict_MAC_Pattern = re.compile( #Валидация MAC-адресов
        r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|'
    )

    def find_mac_address(self, text: str) -> List[str]:
        return self.MAC_Pattern.findall(text)

    def is_valid_mac(self, mac_address: str) -> bool:
        """Проверкка является ли строка MAC-адресом"""
        return bool(self.Strict_MAC_Pattern.match(mac_address.strip()))
