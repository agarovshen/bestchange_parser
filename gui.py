import tkinter as tk
from formatter import format_changer

def run_app(on_search):
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
        # root.destroy()
        # return result["from_code"], result["to_code"]
    btn = tk.Button(root, text="GET RATES", command=on_click)
    btn.pack()
    on_search("BTC", "LTC")
    # from_code, to_code = on_click()
    # print(from_code,to_code)
    # tk.Label(root, text=(from_code,to_code)).pack()
    # on_search(from_code, to_code)
    root.mainloop()
# def show_rates(rates):
#     root = tk.Tk()
#     root.geometry("800x500")
#     root.title("Exchange Rates")

#     text = tk.Text(root)
#     text.pack(fill="both", expand=True)

#     for r in rates:
#         text.insert("end", format_changer(r) + "\n")    
#     root.mainloop()