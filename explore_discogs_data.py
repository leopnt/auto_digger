import xml.etree.ElementTree as ET
import argparse

def explore_large_xml(xml_file: str, level: int):
    count = 0
    for event, element in ET.iterparse(xml_file, events=("start", "end")):
        if event == "start":
            print(f"Element: {element.tag}, Attributes: {element.attrib}")

            if element.text:
                print(f"Text Content: {element.text}")

        element.clear()

        count += 1
        if count > level:
            return

def main():
    parser = argparse.ArgumentParser(description='Explore the structure of an XML file.')
    parser.add_argument('xml_file', help='Path to the XML file')
    parser.add_argument('num_elements', help='Number of elements processed before it stops recursion')
    args = parser.parse_args()

    explore_large_xml(args.xml_file, int(args.num_elements))

if __name__ == '__main__':
    main()

