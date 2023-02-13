import xmltodict
import json
import re


def bpmn_to_dict(bpmn_path):
    with open(bpmn_path, "rb") as bpmn_file:
        bpmn_data: dict = xmltodict.parse(bpmn_file)
        bpmn_data = json.loads(json.dumps(bpmn_data, indent=4))
        return bpmn_data


def get_coords_deltas(bpmn_path):
    with open(bpmn_path, "rb") as bpmn_file:
        data = bpmn_file.read().decode('utf-8')
        x = min([int(i.split('"')[1]) for i in re.findall(r'x="\d+"', data)])
        y = min([int(i.split('"')[1]) for i in re.findall(r'y="\d+"', data)])
    return x, y

