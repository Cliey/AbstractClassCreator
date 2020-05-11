# This Python file uses the following encoding: utf-8
import re
from class_parsing import AbstractClassParsing

class ClassToInterface(AbstractClassParsing):
    def __init__(self, file_content, new_file_path, prefix):
        super().__init__(file_content, new_file_path, prefix)

    def create_specific_template(self, regex_found):
        return self.make_function_virtual(regex_found)

    def make_function_virtual(self, regex_found):
        elt = regex_found.group("indent") + "virtual " +  regex_found.group("function_prototype")
        elt = elt.replace(";", " = 0;")
        return elt

    def create_pattern_function(self):
        """pattern_tab = "(\s*)"
        pattern_function_return = "(?:\w+(?:\:\:)?)+ "
        pattern_function = "(?:.*\(.*\))" anything(anything)
        pattern_end_of_line = ";\n"""
        return "^(?P<indent>\s*)(?P<function_prototype>(?:\w+(?:\:\:)?)+ (?:.*\(.*\));\n)$"

    def parse_file_content_and_write(self):
        interface_file = open(self.new_file_path, "w")
        print(self.file_content)

        for line in self.file_content:
            print("Searching pattern....")
            new_line = super().parse_line(line)
            interface_file.write(new_line)
        interface_file.close()


if __name__ == "__main__":
    file = open("cpp_files/TableModifier.hpp", "r")
    file_content = file.readlines()
    file.close()

    interfaceCreator = ClassToInterface(file_content, "./cpp_files/ITableModifierNew.hpp", "I")
    interfaceCreator.exec()

    file = open("cpp_files/TableTest.hpp", "r")
    file_content = file.readlines()
    file.close()
    interfaceCreator = ClassToInterface(file_content, "./cpp_files/ITableTestNew.hpp", "I")
    interfaceCreator.exec()