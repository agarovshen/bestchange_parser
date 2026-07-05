def format_changer(r):
    return(
        f"{r.get('tag')} Changer: {r.get('changer_name')}"
        f" | Rate: {r.get('rate')}"
        f" | Inmax: {r.get('inmax')}"
        f" | Inmin: {r.get('inmin')}")