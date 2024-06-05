"""
Goal: Multiformat converter (csv - json - xml)
By Fran Ogallas
Start: 21st of May 2024. Last update: 21st of May 2024.
"""
import csv
import json
import re
import sys
from abc import ABC
import xml.etree.ElementTree as ET
from xml.dom import minidom

"""Hola buenas soy andres!!""" 
"""Hello im andres!!"""

class BasicTextFileConverter(ABC):

    def __init__(self, file_name, output_format, supported_formats):
        self.__supported_formats = supported_formats  # THEY MUST BE IN lowercase.
        self.__file_name = file_name
        if self.detect_extension(file_name)[1:] not in supported_formats:
            print("ERROR: Input file has an unsupported extension. Introduce a supported output extension.")
            exit(2)
        else:
            self.__file_name = file_name
        if output_format.lower() not in supported_formats:
            print("ERROR: Unsupported output extension. Introduce a supported output extension.")
            exit(3)
        else:
            self.__output_format = output_format.lower()
        if self.detect_extension(file_name)[1:] == output_format:
            print(f"ERROR: The input file is already a {self.detect_extension(file_name)}. No conversion needed.")
            exit(4)

    @property
    def supported_formats(self):
        return self.__supported_formats

    @property
    def file_name(self):
        return self.__file_name

    @property
    def output_format(self):
        return self.__output_format

    def detect_extension(self, file_name):
        counter = 0
        while counter < len(self.__supported_formats):
            if re.search(rf"\.{self.__supported_formats[counter]}$", file_name) is not None:
                ext = f".{self.__supported_formats[counter]}"
                return ext
            else:
                counter += 1
        print("The format of the input file is not supported by this converter or has a non-valid file name")
        exit(5)

    def remove_ext(self, text, ext):
        return text[:(len(text) - (len(ext)))]

    def print_in_file(self, content, file_name, ext):
        new_file = self.remove_ext(file_name, self.detect_extension(file_name)) + "." + ext
        with open(new_file, "wt", encoding="utf8") as file:
            print(content, file=file)


    def convert(self):
        pass

class CsvJsonConverter(BasicTextFileConverter):

    def __init__(self, file_name, output_format):
        supported_formats = ["csv", "json"]
        super().__init__(file_name, output_format, supported_formats)


    def detect_extension(self, file_name):
        ext = super().detect_extension(file_name)
        return ext

    def csv_to_json(self):
        with open(super().file_name, "rt", encoding="utf8") as input_file:
            csv_content = csv.DictReader(input_file)
            json_content = []
            for row in csv_content:
                json_content.append(row)
            final_content = json.dumps(json_content, indent=2)
            super().print_in_file(final_content, super().file_name, "json")


    def json_to_csv(self):
        with open(super().file_name, "rt", encoding="utf8") as input_file:
            json_content = json.load(input_file)
            csv_rows = [list(json_content[0].keys())]  # It is a list of lists
            for n in range(len(json_content)):
                csv_rows.append(list(json_content[n].values()))
        new_file = self.remove_ext(super().file_name, super().detect_extension(super().file_name)) + ".csv"
        with open(new_file, "wt", encoding="utf8") as output_csv:
            file_writer = csv.writer(output_csv, delimiter=",")
            for i in csv_rows:
                file_writer.writerow(i)

    def convert(self):
        if super().output_format == "json":
            self.csv_to_json()
        else:
            self.json_to_csv()


class CsvXmlConverter(BasicTextFileConverter):

    def __init__(self, file_name, output_format):
        supported_formats = ["csv", "xml"]
        super().__init__(file_name, output_format, supported_formats)

    def detect_extension(self, file_name):
        ext = super().detect_extension(file_name)
        return ext

    def csv_to_xml(self):
        with open(super().file_name, "rt", encoding="utf8") as input_file:
            csv_content = csv.DictReader(input_file)
            rescued_content = list(csv_content)
        xml_content = ET.Element("csvdata")
        xml_subelements = []
        for n in range(len(rescued_content)):
            xml_subelements.append(ET.SubElement(xml_content, "row"))
            row_keys = list(rescued_content[n].keys())
            row_values = list(rescued_content[n].values())
            for m in range(len(row_keys)):
                ET.SubElement(xml_subelements[n], row_keys[m]).text = row_values[m]
        xml_string = minidom.parseString(ET.tostring(xml_content))
        pretty_string = xml_string.toprettyxml()
        new_file = self.remove_ext(super().file_name, super().detect_extension(super().file_name)) + ".xml"
        with open(new_file, "w", encoding="utf8") as output_xml:
            output_xml.write(pretty_string)

    def xml_to_csv(self):
        document = ET.parse(super().file_name)
        root = document.getroot()
        xml_content = []
        pointer = 0
        for child in root:
            xml_content.append({})
            for grandchild in child:
                xml_content[pointer][grandchild.tag] = grandchild.text
            pointer += 1
        csv_rows = [list(xml_content[0].keys())]
        for n in xml_content:
            csv_rows.append(list(n.values()))
        new_file = self.remove_ext(super().file_name, super().detect_extension(super().file_name)) + ".csv"
        with open(new_file, "wt", encoding="utf8") as output_xml:
            file_writer = csv.writer(output_xml, delimiter=",")
            for i in csv_rows:
                file_writer.writerow(i)

    def convert(self):
        if super().output_format == "xml":
            self.csv_to_xml()
        else:
            self.xml_to_csv()


class JsonXmlConverter(BasicTextFileConverter):

    def __init__(self, file_name, output_format):
        supported_formats = ["json", "xml"]
        super().__init__(file_name, output_format, supported_formats)

    def detect_extension(self, file_name):
        ext = super().detect_extension(file_name)
        return ext

    def xml_to_json(self):
        document = ET.parse(super().file_name)
        root = document.getroot()
        xml_content = []
        pointer = 0
        for child in root:
            xml_content.append({})
            for grandchild in child:
                xml_content[pointer][grandchild.tag] = grandchild.text
            pointer += 1
        new_file = self.remove_ext(super().file_name, super().detect_extension(super().file_name)) + ".json"
        with open(new_file, "wt", encoding="utf8") as output_json:
            json.dump(xml_content, output_json, indent=2)

    def json_to_xml(self):
        with open(super().file_name, "rt", encoding="utf8") as input_file:
            json_content = json.load(input_file)
            rescued_content = list(json_content)
            xml_content = ET.Element("csvdata")
            xml_subelements = []
            for n in range(len(rescued_content)):
                xml_subelements.append(ET.SubElement(xml_content, "row"))
                row_keys = list(rescued_content[n].keys())
                row_values = list(rescued_content[n].values())
                for m in range(len(row_keys)):
                    ET.SubElement(xml_subelements[n], row_keys[m]).text = row_values[m]
            xml_string = minidom.parseString(ET.tostring(xml_content))
            pretty_string = xml_string.toprettyxml()
            new_file = self.remove_ext(super().file_name, super().detect_extension(super().file_name)) + ".xml"
            with open(new_file, "w", encoding="utf8") as output_xml:
                output_xml.write(pretty_string)

    def convert(self):
        if super().output_format == "json":
            self.xml_to_json()
        else:
            self.json_to_xml()


class InternalFormatError(ValueError):

    def __init__(self):
        super().__init__("ERROR. An internal function that uses format names tried to use a format name that it "
                         "cannot use")


class CsvJsonXmlConverter(BasicTextFileConverter):

    def __init__(self, file_name, output_format):
        supported_formats = ["csv", "json", "xml"]
        super().__init__(file_name, output_format, supported_formats)

    def detect_extension(self, file_name):
        ext = super().detect_extension(file_name)
        return ext

    def convert(self):
        extension1 = self.detect_extension(super().file_name)
        extension2 = super().output_format
        if ((extension1 == ".csv") or (extension1 == ".json")) and ((extension2 == "csv") or (extension2 == "json")):
            return CsvJsonConverter(super().file_name, extension2).convert()
        elif ((extension1 == ".csv") or (extension1 == ".xml")) and ((extension2 == "csv") or (extension2 == "xml")):
            return CsvXmlConverter(super().file_name, extension2).convert()
        elif ((extension1 == ".xml") or (extension1 == ".json")) and ((extension2 == "xml") or (extension2 == "json")):
            return JsonXmlConverter(super().file_name, extension2).convert()
        else:
            raise InternalFormatError


def argvs_intermediary():
    try:
        argv1 = sys.argv[1]
        argv2 = sys.argv[2]
        return [argv1, argv2]
    except IndexError:
        print("ERROR. Data input incorrectly.")
        exit(1)


def main():
    arguments = argvs_intermediary()
    CsvJsonXmlConverter(arguments[0], arguments[1]).convert()


if __name__ == "__main__":
    main()
