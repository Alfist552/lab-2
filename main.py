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

def main():
    "Функция - меню"
    validator = MacAddress()

    print("Меню")
    print("1. Проверка MAC-адреса")
    print("2. Поиск MAC-адреса в тексте")
    print("3. Поиск MAC-адреса в файле")

    try:
        choise = input("Выберите вариант:(1-3): ").strip()

        if choise == "1":
            mac = input("Введите MAC-адреса для проверки: ").strip()
            if validator.is_valid_mac(mac):
                print(f"Правильный mac-адрес: {mac}")
            else:
                print("Неправильный MAC-адрес")

        elif choise == "2":
            text = input("Введите текст для поиска MAC-адресов ").strip()
            valid_macs, all_found = validator.extract_mac_from_text(text)

            print(f"Найдено адресов: {len(all_found)}")
            print(f"Правильных адресов: {len(valid_macs)}")

            if valid_macs:
                print("Правильные MAC-адреса: ")
                for i, mac in enumerate(valid_macs, 1):
                    print(f"{i}. {mac}")

        elif choise == "3":
            file_path = input("Укажите путь файла: ").strip()
            valid_macs, all_found = validator.extract_mac_from_file(file_path)

            print(f"Найдено адресов: {len(all_found)}")
            print(f"Правильных адресов: {len(valid_macs)}")

            if valid_macs:
                print("Правильные MAC-адреса: ")
                for i, mac in enumerate(valid_macs, 1):
                    print(f"{i}. {mac}")
        else:
            print("Неверный выбор.")

    except KeyboardInterrupt:
        print("\n Disconnect by user.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")