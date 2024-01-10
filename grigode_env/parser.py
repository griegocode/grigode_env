def get_parser(type_: str):
    return {
        "str": str,
        "int": int,
        "float": float,
        "bool": lambda v: v == "True" if v in ["True", "False"] else None,
        "none": lambda _: None,
    }.get(type_)
