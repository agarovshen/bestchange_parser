def format_changer(r):
    if not hasattr(r, 'changer'):
        return (str(r), "-", "-")

    return (
        f"{r.changer}",
        f"{r.rate:.8f}",
        f"{r.inmin}"
    )