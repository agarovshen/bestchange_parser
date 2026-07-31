def format_changer(r):
    return(
        f" Changer: {r.changer_name}"
        f" | Rate: {r.exchange_rate:.2f}"
        f" | Inmin: {r.inmin}"
    )