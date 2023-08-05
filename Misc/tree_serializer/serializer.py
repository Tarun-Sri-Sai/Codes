from os.path import isfile
from json import load


SINGLE_BRANCH = '\u2514'
EXTEND_BRANCH = '\u251C'
HORIZONTAL = '\u2500\u2500'
VERTICAL = '\u2502'


def serialize_util(data, last=False, indent='', root=True):
    if root:
        result = f'{data["value"]}\n'
    else:
        next_indent = SINGLE_BRANCH if last else EXTEND_BRANCH
        result = f'{indent}{next_indent}{HORIZONTAL}{data["value"]}\n'
        indent += f'{VERTICAL}  '
    for child in data['children']:
        last = (child == data['children'][-1])
        result += serialize_util(child, last=last, indent=indent, root=False)
    return result


def serialize(file_path):
    if not isfile(file_path):
        return None
    with open(file_path, 'r') as f:
        data = load(f)
    return serialize_util(data)
