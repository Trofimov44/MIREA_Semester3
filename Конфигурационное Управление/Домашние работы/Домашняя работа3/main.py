import argparse
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom


class ConfigParser:
    def __init__(self):
        self.constants = {}
        self.data = {}

    def parse(self, text):
        # Удаляем комментарии
        text = re.sub(r"//.*", "", text)
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for line in lines:
            if line.startswith("const"):
                self._parse_constant(line)
            elif line.startswith("#{"):
                self._evaluate_expression(line)
            else:
                self._parse_array(line)

    def _parse_constant(self, line):
        match = re.match(r"const (\w+) = (.+)", line)
        if match:
            name, value = match.groups()
            if re.match(r"^\d+(\.\d+)?$", value):  # Число
                self.constants[name] = float(value)
            elif value.startswith("#{") and value.endswith("}"):  # Постфиксное выражение
                expr = value[2:-1].strip()  # Убираем '#{' и '}'
                self.constants[name] = self._evaluate_expression(expr)
            else:
                raise ValueError(f"Invalid constant value: {value}")
        else:
            raise SyntaxError(f"Invalid syntax: {line}")

    def _evaluate_expression(self, expr):
        tokens = expr.split()
        stack = []
        for token in tokens:
            if re.match(r"^\d+(\.\d+)?$", token):  # Число
                stack.append(float(token))
            elif token in self.constants:  # Константа
                stack.append(self.constants[token])
            elif token in ["+", "-", "*", "/"]:  # Операции
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                elif token == "/":
                    stack.append(a / b)
            elif token == "abs":  # Функция abs()
                a = stack.pop()
                stack.append(abs(a))
            else:
                raise ValueError(f"Unknown token in expression: {token}")
        return stack[0]

    def _parse_array(self, line):
        match = re.match(r"(\w+) = \(list (.+)\)", line)
        if match:
            name, values = match.groups()
            values = values.split()
            self.data[name] = [float(v) if v.isdigit() else v for v in values]
        else:
            raise SyntaxError(f"Invalid syntax: {line}")

    def to_xml(self):
        root = ET.Element("configuration")

        for name, value in self.constants.items():
            ET.SubElement(root, "constant", name=name, value=str(value))

        for name, values in self.data.items():
            array_elem = ET.SubElement(root, "array", name=name)
            for value in values:
                ET.SubElement(array_elem, "value").text = str(value)

        # Преобразование в строку с отступами
        rough_string = ET.tostring(root, encoding="unicode")
        parsed = minidom.parseString(rough_string)
        return parsed.toprettyxml(indent="  ")


def main():
    parser = argparse.ArgumentParser(description="Config to XML converter")
    parser.add_argument("--input", required=True, help="Path to input file")
    parser.add_argument("--output", required=True, help="Path to output file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        text = f.read()

    config_parser = ConfigParser()
    config_parser.parse(text)
    xml_output = config_parser.to_xml()

    with open(args.output, "w") as f:
        f.write(xml_output)


if __name__ == "__main__":
    main()
