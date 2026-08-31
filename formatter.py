def format_changer(r):
    # if not hasattr(r, 'changer'):
    #     return (str(r), "-", "-")

    return (
        f"{r.get("changer")}",
        f"{r.get("rate"):.8f}",
        f"{r.get("inmin")}"
    )