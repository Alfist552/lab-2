import re
import os
from typing import List, Tuple
import unittest
import tempfile

class MacAddress:
    """Классы для работы с Mac-адресами"""

    MAC_Pattern = re.compile( #Поиск Потенциальныъх MAC-адресов
        r'(?:[0-9A-Za-z]{2}[:-]){5}[0-9A-Za-z]{2}|' #Формат ХХ:ХХ:ХХ:ХХ:ХХ и ХХ-ХХ-ХХ-ХХ-ХХ
        r'(?:[0-9A-Za-z]{4}\.){2}[0-9A-Za-z]{4}|' #XXXX.XXXX.XXXX
        r'[0-9A-Za-z]{12}' #XXXXXXXXXXXX
    )

    Strict_MAC_Pattern = re.compile( #Валидация MAC-адресов
        r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$|'
        r'^([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}$|'
        r'^[0-9A-Fa-f]{12}$'
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
        choice = input("Выберите вариант:(1-3): ").strip()

        if choice == "1":
            mac = input("Введите MAC-адреса для проверки: ").strip()
            if validator.is_valid_mac(mac):
                print(f"Правильный mac-адрес: {mac}")
            else:
                print("Неправильный MAC-адрес")

        elif choice == "2":
            text = input("Введите текст для поиска MAC-адресов ").strip()
            valid_macs, all_found = validator.extract_mac_from_text(text)

            print(f"Найдено адресов: {len(all_found)}")
            print(f"Правильных адресов: {len(valid_macs)}")

            if valid_macs:
                print("Правильные MAC-адреса: ")
                for i, mac in enumerate(valid_macs, 1):
                    print(f"{i}. {mac}")

        elif choice == "3":
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

class TestMacAddress(unittest.TestCase):
    """Класс для Unit-тестов"""

    def setUp(self):
        """Запуск перед каждой функцией для тестирования"""
        self.validator = MacAddress()

    def test_valid_mac_address(self):
        """Тест правильных MAC-адресов"""
        valid_macs = [
          "00:0B:56:62:BD:70",
          "00:3E:D7:41:65:45",
          "BC4F.19C1.7A6E"
        ]

        for mac in valid_macs:
            with self.subTest(mac=mac):
                self.assertTrue(self.validator.is_valid_mac(mac))

    def test_invalid_mac_address(self):
        """Тест неправильных MAC-адресов"""
        invalid_macs = [
            "11:22:33:44:55",
            "YY-XX-BB-CC-DD",
            "ABCDEFGHIJKLM",
            "BC4F.19C1.7A6M"
        ]
        for mac in invalid_macs:
            with self.subTest(mac=mac):
                self.assertFalse(self.validator.is_valid_mac(mac))

    def test_find_mac_addresses_in_text(self):
        """Поиск MAC-адресов в тексте"""
        text = "MAC1: 12:24:24:D9:A5:07, MAC2: 00-1B-44-11-3A-B8"
        found = self.validator.find_mac_address(text)
        self.assertEqual(found,["12:24:24:D9:A5:07","00-1B-44-11-3A-B8"])

    def test_extract_mac_from_text(self):
        """Извлечение MAC-адресов из текста"""
        text = "Valid: 12:24:24:D9:A5:07, Invalid: 122424D9A5GG"
        valid_macs, all_found = self.validator.extract_mac_from_text(text)
        self.assertEqual(len(all_found), 2)
        self.assertEqual(len(valid_macs),1)
        self.assertIn("12:24:24:D9:A5:07", valid_macs)

    def test_extract_mac_from_file(self):
        """Извлечение MAC-адреса из файла"""
        test_content = "12:24:24:D9:A5:07\n12-24-24-D9-A5-07\nInvalid: 001B.5511.3AGG"

        with tempfile.NamedTemporaryFile(mode = 'w', delete = False, encoding = 'utf-8') as f:
            f.write(test_content)
            temp_file = f.name

        try:
            valid_macs, all_found = self.validator.extract_mac_from_file(temp_file)

            self.assertEqual(len(all_found), 3)
            self.assertEqual(len(valid_macs), 2)

            self.assertIn("12:24:24:D9:A5:07", valid_macs)
            self.assertIn("12-24-24-D9-A5-07", valid_macs)

        finally:
            os.unlink(temp_file)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        print("Unit tests")
        unittest.main(verbosity = 2, exit = False)
    else:
        main()