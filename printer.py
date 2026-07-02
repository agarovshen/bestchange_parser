def print_changer(r, prefix=""):
    print(
        f"{prefix} Changer: {r.get('changer')}"
        f"|Rate: {r.get('rate')}"
        f"|Inmax: {r.get('inmax')}"
        f"|Inmin: {r.get('inmin')}")
    return