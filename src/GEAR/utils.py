import itertools


def dict_product(d: dict):
    k = d.keys()
    v = d.values()
    v_product = itertools.product(*v)
    d_product = list()
    for v_p in v_product:
        d_one = dict(zip(k, v_p))
        d_product.append(d_one)
    return d_product
