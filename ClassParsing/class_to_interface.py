# This Python file uses the following encoding: utf-8
import re
from ClassParsing.class_parsing import AbstractClassParsing

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
        """Pattern to get info about function parsed.
        Can parse :
            - namespace::A<namespace::type>
            - const fct(Arg1, Arg2) const;
        Regex :
            ^(?P<indent>\s*)(?P<function_prototype>(?:const )?(?P<type>(?:\w+(?:\:\:)?)+)(?P<subtype><?(?P>type)>?)? (?:.*\(.*\))(?: const)?;\n)$"""

        type_regex = "(?:(?:\w+(?:\:\:)?)+)"
        regex = "^(?P<indent>\s*)(?P<function_prototype>(?:const )?" + type_regex + "(?P<subtype><?" + type_regex + ">?)? (?:.*\(.*\))(?: const)?;\n)$"
        return regex

    def parse_file_content_and_write(self):
        interface_file = open(self.new_file_path, "w")
        print(self.file_content)

        for line in self.file_content:
            print("Searching pattern....")
            new_line = super().parse_line(line)
            interface_file.write(new_line)
        interface_file.close()
