import re
from abc import ABC, abstractmethod

class AbstractClassParsing(ABC):
    #PB with reference return & std::unique_ptr<type> etc.
    def __init__(self, file_content, new_file_path, prefix):
        self.file_content = file_content
        self.new_file_path = new_file_path
        self.is_public_member = False
        self.is_private_member = False
        self.end_of_class_detected = False
        self.prefix = prefix
        self.function_pattern = self.create_pattern_function()

    @abstractmethod
    def create_pattern_function(self):
        pass

    @abstractmethod
    def create_specific_template(self, regex_found):
        pass

    def search_public(self, line):
        return re.search("^(?:\s)*public:\n$", line)

    def search_private(self, line):
        return re.search("^(?:\s)*private:\n$", line)

    def set_public_private_flag(self, line):
        if self.search_public(line):
            print("Public Found")
            self.is_public_member = True
            self.is_private_member = False
        if self.search_private(line):
            print("Private Found")
            self.is_public_member = False
            self.is_private_member = True

    def is_end_of_class(self, line):
        if re.search("^(?:\s)*};\n$", line):
            self.end_of_class_detected = True
            self.is_public_member = False
            self.is_private_member = False
            return True

    def is_new_class_detected(self, line):
        self.new_class_search = re.search("^(?P<indent>\s*)class (?P<class_name>\w+)\n$", line)
        return self.new_class_search

    def get_new_class_name(self, line):
        if self.new_class_search:
            print("is_new_class_detected !")
            class_name = self.new_class_search.group("class_name")
            class_name = class_name.replace(class_name, self.prefix + class_name)
            line_to_write = self.new_class_search.group("indent") + "class " + class_name + "\n"
            self.is_public_member = False
            self.is_private_member = False
            self.end_of_class_detected = False
            return line_to_write

    def is_class_public_member(self):
        return self.is_public_member and not self.is_private_member

    def is_class_private_member(self):
        return self.is_private_member and not self.end_of_class_detected

    def parse_public_member(self, line):
        # Parse public keyword
        regex_found_public = re.search("^(?:\s)*public:\n$", line)
        if regex_found_public:
            return regex_found_public.group(0)
        # Parse public function
        regex_found_function = re.search(self.function_pattern, line)
        if regex_found_function:
            return self.create_specific_template(regex_found_function)
        return str()

    def parse_end_of_namespace(self, line):
        pattern_end_of_namespace = "^(?:\s)*} (?:\/\/(?:.*))\n?$"
        regex_found_end_namespace = re.search(pattern_end_of_namespace, line)
        if regex_found_end_namespace:
            return regex_found_end_namespace.group(0)
        return str()

    def parse_line(self, line):
        self.set_public_private_flag(line)

        if self.is_end_of_class(line):
            print("self.is_end_of_class")
            return line
        elif self.is_new_class_detected(line):
            print("self.is_new_class_detected")
            return self.get_new_class_name(line)
        elif self.is_class_public_member():
            print("self.is_class_public_member")
            return self.parse_public_member(line)
        elif self.is_class_private_member():
            print("self.is_class_private_member")
            return str()
        elif self.end_of_class_detected:
            print("self.end_of_class_detected")
            return self.parse_end_of_namespace(line)
        print("else")
        return line

    @abstractmethod
    def parse_file_content_and_write(self):
        pass

    def exec(self):
        self.parse_file_content_and_write()