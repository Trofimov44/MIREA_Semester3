import unittest
from main import ConfigParser  # Импортируем ваш класс
import xml.etree.ElementTree as ET


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.parser = ConfigParser()

    def test_parse_constant_number(self):
        """Тест для парсинга числовой константы."""
        text = "const PI = 3.14"
        self.parser.parse(text)
        self.assertIn("PI", self.parser.constants)
        self.assertEqual(self.parser.constants["PI"], 3.14)

    def test_parse_constant_expression(self):
        """Тест для парсинга константного выражения."""
        text = """
        const A = 10
        const B = 20
        const C = #{A B +}
        """
        self.parser.parse(text)
        self.assertEqual(self.parser.constants["C"], 30)

    def test_parse_array(self):
        """Тест для парсинга массива."""
        text = "myArray = (list 1 2 3 4)"
        self.parser.parse(text)
        self.assertIn("myArray", self.parser.data)
        self.assertEqual(self.parser.data["myArray"], [1.0, 2.0, 3.0, 4.0])

    def test_to_xml(self):
        """Тест для проверки генерации XML."""
        text = """
        const PI = 3.14
        const RADIUS = 10
        const AREA = #{PI RADIUS RADIUS * *}
        myArray = (list 1 2 3 4)
        """
        self.parser.parse(text)
        xml_output = self.parser.to_xml()

        # Парсим XML и проверяем содержимое
        root = ET.fromstring(xml_output)

        # Проверяем константы
        constants = root.findall("constant")
        self.assertEqual(len(constants), 3)

        pi = root.find("constant[@name='PI']")
        self.assertIsNotNone(pi)
        self.assertEqual(pi.attrib["value"], "3.14")

        radius = root.find("constant[@name='RADIUS']")
        self.assertIsNotNone(radius)
        self.assertEqual(radius.attrib["value"], "10.0")

        area = root.find("constant[@name='AREA']")
        self.assertIsNotNone(area)
        self.assertEqual(area.attrib["value"], "314.0")

        # Проверяем массив
        array = root.find("array[@name='myArray']")
        self.assertIsNotNone(array)
        values = array.findall("value")
        self.assertEqual(len(values), 4)
        self.assertEqual([v.text for v in values], ["1.0", "2.0", "3.0", "4.0"])

    def test_invalid_syntax(self):
        """Тест для проверки обработки неверного синтаксиса."""
        text = "invalid line"
        with self.assertRaises(SyntaxError):
            self.parser.parse(text)

    def test_invalid_expression(self):
        """Тест для проверки некорректного выражения."""
        text = "const RESULT = #{A B &}"
        with self.assertRaises(ValueError):
            self.parser.parse(text)


if __name__ == "__main__":
    unittest.main()
