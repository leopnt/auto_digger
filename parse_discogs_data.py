import xml.etree.ElementTree as ET
import argparse
import os
import time


def explore_large_xml(xml_file: str, level: int):
    """
    This function takes an XML file path and a level as input and prints the contents of the XML file up to the specified level.

    Args:
    - xml_file (str): The path of the XML file to be parsed.
    - level (int): The maximum depth of the XML tree to be printed.

    Returns:
    - None
    """
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
            print(tab * num_tabulation + out, end="")

        if event == "end":
            print(tab * num_tabulation + f"</{element.tag}>")
            num_tabulation -= 1

        if count > level:
            return

        count += 1

        element.clear()  # clear memory


def count_releases(xml_file: str) -> int:
    """
    Counts the number of releases in a Discogs XML file.

    Args:
    xml_file (str): The path to the Discogs XML file.

    Returns:
    int: The number of releases in the XML file.
    """
    count = 0

    total_size = os.path.getsize(xml_file)

    start_time = time.time()

    with open(xml_file, "r") as f:
        for event, element in ET.iterparse(f, events=("start", "end")):
            if count % 1000 == 0:
                end_time = time.time()
                elapsed_time = end_time - start_time
                progression = f.tell() / total_size
                remaining_time = elapsed_time / progression

                print(
                    f"count={count} progression={(progression * 100):.2f}% elapsed={int(elapsed_time)}s remaining=~{int(remaining_time / 60.0)}m    ",
                    end="\r",
                )

            if event == "start":
                if element.tag == "release":
                    count += 1

            if event == "end":
                pass

            element.clear()  # clear memory

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Explore the structure of an XML file."
    )
    parser.add_argument("xml_file", help="Path to the XML file")
    parser.add_argument(
        "num_elements",
        help="Number of XML elements processed before it stops iteration",
    )
    args = parser.parse_args()

    # if args.level == 0:
    #    print(f"found {count_releases(args.xml_file)} releases")

    # else:
    explore_large_xml(args.xml_file, int(args.num_elements))


if __name__ == "__main__":
    main()
