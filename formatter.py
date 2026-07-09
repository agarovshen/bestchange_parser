def format_changer(r):
    return(
        f"{r.get('tag')} Changer: {r.get('changer_name')}"
        f" | Rate: {r.get('exchange_rate'):.2f}"
        f" | Inmax: {r.get('inmax')}"
        f" | Inmin: {r.get('inmin')}")