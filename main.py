import re
import urllib.request
import os

class MacAddress:
    """Классы для работы с Mac-адресами"""

    MAC_Pattern = re.compile( #Поиск MAC-адресов
        r'(?:[0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})]' #Формат ХХ:ХХ:ХХ:ХХ:ХХ и ХХ-ХХ-ХХ-ХХ-ХХ
    )

    Strict_MAC_Pattern = re.compile( #Валидация MAC-адресов
        r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|'
    )


