import os


def _get_dir_contents(parent_dir):
    sub_dirs, files = [], []
    for item in os.listdir(parent_dir):
        item_path = os.path.join(parent_dir, item)
        if os.path.isdir(item_path):
            sub_dirs.append(item)
        else:
            files.append(item)
    return sub_dirs, files


def _compare_file_contents(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        if f1.read() != f2.read():
            print(f"Contents in [{file1}] and [{file2}] don't match")
            return False

    return True


def _get_base_item_paths(items, base_path, parent_dir):
    return {
        os.path.join(base_path, item): os.path.join(parent_dir, item)
        for item in items}


def _compare_dir_contents(dir1, dir2, ignore_missing=False, base_path=None):
    if (basename1 := os.path.basename(dir1)) != os.path.basename(dir2):
        print(f"Directory names for [{dir1}] and [{dir2}] don't match")
        return False

    if base_path is None:
        base_path = basename1

    sub_dirs1, files1 = _get_dir_contents(dir1)
    sub_dirs2, files2 = _get_dir_contents(dir2)

    sub_dir_paths1 = _get_base_item_paths(sub_dirs1, base_path, dir1)
    sub_dir_paths2 = _get_base_item_paths(sub_dirs2, base_path, dir2)

    if not ignore_missing and len(sub_dir_paths1) != len(sub_dir_paths2):
        print(f'Sub-directories missing between [{dir1}] and [{dir2}]')
        return False

    comparison_result = set()

    for key in set(sub_dir_paths1.keys()).intersection(
            set(sub_dir_paths2.keys())):
        comparison_result.add(
            _compare_dir_contents(sub_dir_paths1[key], sub_dir_paths2[key],
                                  ignore_missing, key))

    file_paths1 = _get_base_item_paths(files1, base_path, dir1)
    file_paths2 = _get_base_item_paths(files2, base_path, dir2)

    if not ignore_missing and len(file_paths1) != len(file_paths2):
        print(f'Files missing between [{dir1}] and [{dir2}]')
        return False

    for key in set(file_paths1.keys()).intersection(set(file_paths2.keys())):
        comparison_result.add(_compare_file_contents(file_paths1[key],
                                                     file_paths2[key]))

    return all(comparison_result)


def compare_dir_contents(dir1, dir2, *, ignore_missing=False):
    return _compare_dir_contents(dir1, dir2, ignore_missing)
