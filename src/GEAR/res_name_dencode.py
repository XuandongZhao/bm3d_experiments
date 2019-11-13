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
