import tkinter as tk
from formatter import format_changer
from settings import ScannerSettings

def run_app(on_search):
    root = tk.Tk()
    root.geometry("800x700")
    root.title("Arbitrage Bot")

    top_frame = tk.Frame(root, bg="yellow")
    top_frame.pack(fill="x", padx=10, pady=10)

    #From currency label
    first_frame = tk.Frame(top_frame, bg="red")
    first_frame.pack(side="left")
    tk.Label(first_frame, text="From e.g. BTC: ").pack(anchor="w", padx=5)
    from_input = tk.Entry(first_frame, width=20)
    from_input.pack()

    #To currency label
    second_frame = tk.Frame(top_frame, bg="green", padx=10)
    second_frame.pack(side="left")
    tk.Label(second_frame, text=("To e.g. USDT: ")).pack(anchor="w", padx=5)
    to_input = tk.Entry(second_frame, width=20)
    to_input.pack()

    #Output label
    third_frame = tk.Frame(top_frame, bg="blue", padx=10)
    third_frame.pack(side="left")
    output = tk.Label(third_frame, text="")
    output.pack()
    btn = tk.Button(third_frame, text="GET RATES", padx=20)
    btn.pack()

    #Fourth frame
    fourth_frame = tk.Frame(top_frame, bg="purple", padx=10)
    fourth_frame.pack(side="left")
    directions_var = tk.IntVar(value=2)
    tk.Radiobutton(
        fourth_frame, 
        text="Find 2 directions",
        variable=directions_var,
        value=2).pack()
    tk.Radiobutton(
        fourth_frame,
        text="Find 3 directions",
        variable=directions_var,
        value=3).pack()
    #Bottom Frame
    result_frame = tk.Frame(root, bg="yellow")
    result_frame.pack(fill="both", padx=10, pady=10)

    #Text of list of changers
    text = tk.Text(result_frame)
    text.pack(fill="both")
    settings = ScannerSettings(
            capital=1000,
            currency="USDTBEP20"
        )
    def on_click():

        if directions_var.get() == 2:
            directions = on_search(settings=settings, directions_var=directions_var.get())        
            root.title("Exchange Rates")
            text.delete("1.0", "end")
            for direction in directions:
                output = (
                    f"{direction['direct']}:\n"
                    f"{'\n'.join(format_changer(rate) for rate in direction['direct_rates'])}\n"
                    f"{direction['reverse']}:\n"
                    f"{'\n'.join(format_changer(rate) for rate in direction['reverse_rates'])}\n"
                    f"SPREADS: {direction['spread']}:\n"
                )
                text.insert("end",output)
        if directions_var.get() == 3:
            cycles = on_search(settings=settings, directions_var=directions_var.get())
            print("5 after give cycles in gui")
            text.delete("1.0", "end")
            
            for cycle in cycles:
                output = (
                    f"{cycle['direction_ab']} ==> {format_changer(cycle['direction_ab_rates'])}:\n"
                    f"{cycle['direction_bc']} ==> {format_changer(cycle['direction_bc_rates'])}:\n"
                    f"{cycle['direction_ca']} ==> {format_changer(cycle['direction_ca_rates'])}:\n"
                    f"SPREADS: {cycle['spread']}:\n"
                )
                text.insert("end", output)
            print("6 after paint in tkinter in gui.py")
    btn.config(command=on_click)
############################################################
    #Setting menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    setting_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=setting_menu)
    setting_menu.add_command(
        label="Scanner Settings",
        command=lambda: open_scanner_settings(settings))
    def open_scanner_settings(settings):
        window = tk.Toplevel(root)
        window.title("Scanner Settings")
        window.geometry("350x150")
        tk.Label(window, text="Capital: ").pack()
        capital_var = tk.StringVar(value=str(settings.capital))
        tk.Entry(window, textvariable=capital_var).pack()
        tk.Label(window, text="Currency: ").pack()
        currency_var = tk.StringVar(value=str(settings.currency))
        tk.Entry(window, textvariable=currency_var).pack()
        def save():
            try:
                capital = float(capital_var.get())
                currency = currency_var.get()
                if capital <= 0:
                    raise ValueError
                settings.capital = capital
                settings.currency = currency
                window.destroy()
            except ValueError:
                print("Invalid capital")
        tk.Button(window, text="Save", command=save).pack()
    setting_menu.add_separator()
    setting_menu.add_command(label="About")

    root.mainloop()