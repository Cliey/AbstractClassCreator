from class_parsing import AbstractClassParsing
import re

class ClassToMock(AbstractClassParsing):
    def __init__(self, file_content, new_file_path, prefix):
        super().__init__(file_content, new_file_path, prefix)

    def create_specific_template(self, regex_found):
        return self.make_mock_method(regex_found)

    def create_pattern_function(self):
        return "^(?P<indent>\s*)(?:virtual )?(?P<function_return>\w+(?:\:\:)?)+ (?P<function_name>.*)\((?P<args>.*)\)(?: = 0)?;\n$"

    def make_mock_method(self, regex_found):
        args = self.extract_args_type(regex_found.group("args"))
        elt = regex_found.group("indent") + "MOCK_METHOD(" + regex_found.group("function_return") + ", "+ regex_found.group("function_name") + ", (" + args + "));\n"
        return elt

    def is_include(self, line):
        return re.search("^#(?:include|pragma) .*\n$", line)

    def extract_args_type(self, args):
        pattern = "(?P<args_type>(?:\w+(?:\:\:)?)+(?:&)?)(?:\s\w+)?(?:,)?"
        regex_found = re.findall(pattern, args)
        return_str = ', '.join(regex_found)
        return return_str

    def build_header_file(self, interface_file):
        interface_file.write("#pragma once\n")
        interface_file.write("#include \"gmock/gmock.h\"\n")
        interface_file.write("#include \"YourInterfaceClass.hpp\"\n")

    def parse_file_content_and_write(self):
        interface_file = open(self.new_file_path, "w")
        print(self.file_content)
        self.build_header_file(interface_file)

        for line in self.file_content:
            print("Searching pattern....")
            if self.is_include(line):
                continue
            new_line = super().parse_line(line)
            interface_file.write(new_line)
        interface_file.close()


if __name__ == "__main__":
    file = open("cpp_files/TableModifier.hpp", "r")
    file_content = file.readlines()
    file.close()

    mockCreator = ClassToMock(file_content, "./cpp_files/MockTableModifierNew.hpp", "Mock")
    mockCreator.exec()

    file = open("cpp_files/TableTest.hpp", "r")
    file_content = file.readlines()
    file.close()
    mockCreator = ClassToMock(file_content, "./cpp_files/MockTableTestNew.hpp", "Mock")
    mockCreator.exec()