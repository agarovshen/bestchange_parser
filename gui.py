import tkinter as tk
from api import get_rates_by_name

def get_currency_codes():
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Arbitrage Bot")

    #From currency label
    tk.Label(root, text="From e.g. BTC: ").pack()
    from_input = tk.Entry(root)
    from_input.pack()

    #To currency label
    tk.Label(root, text=("To e.g. USDT: ")).pack()
    to_input = tk.Entry(root)
    to_input.pack()

    #Output label
    output = tk.Label(root, text="")
    output.pack()
    result = {}

    # #List of changers
    # text = tk.Text(root, text)
    def on_click():
        result["from_code"] = from_input.get().upper()
        result["to_code"] = to_input.get().upper()
        # output.config(text=f"Loading {result['from_code']} -> {result['to_code']} ...")
        root.destroy()
    
    btn = tk.Button(root, text="GET RATES", command=on_click)
    btn.pack()
    root.mainloop()
    return result["from_code"], result["to_code"]