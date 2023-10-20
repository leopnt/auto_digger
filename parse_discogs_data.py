import xml.etree.ElementTree as ET
import argparse

def explore_large_xml(xml_file: str, level: int):
    count = 0
    num_tabulation = 0
    tab = "  "

    for event, element in ET.iterparse(xml_file, events=("start", "end")):
        if event == "start":
            num_tabulation += 1

            out = f"<{element.tag}"
            for key, value in element.attrib.items():
                out += f' {key}="{value}"'
            out += ">"

            out += "\n"
            
            if element.text:
                out += tab * (num_tabulation + 1) + f"{element.text}\n"
            print(tab * num_tabulation + out, end='')

        
        if event == "end":
            print(tab * num_tabulation + f"</{element.tag}>")
            num_tabulation -= 1

        if count > level:
            return

        count += 1

        element.clear() # clear memory

def main():
    parser = argparse.ArgumentParser(description='Explore the structure of an XML file.')
    parser.add_argument('xml_file', help='Path to the XML file')
    parser.add_argument('num_elements', help='Number of XML elements processed before it stops iteration')
    args = parser.parse_args()

    explore_large_xml(args.xml_file, int(args.num_elements))

if __name__ == '__main__':
    main()
