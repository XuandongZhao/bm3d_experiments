import os

def dict2name(d: dict):
    res_name = ''
    for k, v in d.items():
        res_name += k + '_' + str(v) + '-'
    return res_name


def name_hyper_res_2_str(name: str, hyper: dict, res: dict):
    whole_name = name + '+' + dict2name(hyper) + '=' + dict2name(res)
    return whole_name


def name_hyper_2_str(name: str, hyper: dict):
    name_hyper = name + '+' + dict2name(hyper)
    return name_hyper


def find_filename_in_dir(search_dir, include_str_list, exclude_str_list=None):
    assert os.path.isabs(search_dir)
    if exclude_str_list is None:
        exclude_str_list = list()
    for file_name in os.listdir(search_dir):
        if not is_include_strs(file_name, *include_str_list):
            continue
        if not is_exclude_str(file_name, *exclude_str_list):
            continue
        return file_name


def is_include_strs(whole_str, *strs):
    for st in strs:
        if st not in whole_str:
            return False
    return True


def is_exclude_str(whole_str, *strs):
    for st in strs:
        if st in whole_str:
            return False
    return True


def is_contain_all(whole_str, name=None, hyper: dict = None, hyper2: dict = None):
    if name is not None:
        if name not in whole_str:
            return False
    if hyper is not None:
        for k, v in hyper.items():
            if k + '_' + str(v) not in whole_str:
                return False
    if hyper2 is not None:
        for k, v in hyper2.items():
            if k + '_' + str(v) not in whole_str:
                return False
    return True


def decode_res(whole_str: str):
    whole_str = whole_str.replace('.png', '')
    _, res_str = whole_str.split('=')
    res_list = res_str.split('-')
    res_dict = dict()
    for res in res_list:
        k, v = res.split('_')
        res_dict[k] = float(v)
    return res_dict
