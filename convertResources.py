import xml.etree.ElementTree as ET
import json
import sys
import re

def help():
    print("Usage: python3 convertResources.py FILE")

def parse_xml_tree(filename):
    tree = ET.parse(filename)
    return tree.getroot()

supported_tags = ["string", "color"]

def tree_to_dict(root):
    resources = {tag: {} for tag in supported_tags}
    
    for child in root:
        if child.tag in supported_tags:
            if "name" not in child.attrib:
                print("Warning: Attribute 'name' not found in child")
                continue
            
            resources[child.tag].update({child.get('name'): child.text})
        else:
            print("Warning: Ignored unsupported tag {}".format(child.tag))

    return resources

def resources_are_valid(resources):
    values_found = False
    found_tag = None
    for tag in supported_tags:
        if len(resources[tag]) > 0:
            if values_found:
                print("Error: Mixed tags are not valid")
                return False, None
            values_found = True
            found_tag = tag
    if not values_found:
        print("Error: No tags found, exiting")
        return False, None

    return True, found_tag


def extract_class_name_and_dict(resources):
    valid, tag = resources_are_valid(resources)
    if not valid:
        exit()

    # append "s" for classname, since it is a collection of items
    class_name = tag + "s"
    class_body_dict = resources[tag]

    return class_name, class_body_dict


def dict_to_js_class_body(class_body_dict):
    json_string = json.dumps(class_body_dict, sort_keys=False,
                     indent=4, separators=(',', ': '))

    # remove the quotes from key, "key": "value" -> key: "value"
    json_string = re.sub(r'(?<!: )"(\S*?)"', '\\1', json_string)

    return json_string


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        help()
        exit()
    
    filename = sys.argv[1]
    root = parse_xml_tree(filename)

    if root.tag != "resources":
        print("File is not an android resource xml")
        exit()

    resources = tree_to_dict(root)

    class_name, class_body_dict = extract_class_name_and_dict(resources)
    class_body_string = dict_to_js_class_body(class_body_dict)
    
    print(f"const {class_name} = {class_body_string};\n\nexport default {class_name};")
