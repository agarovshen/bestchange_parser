import tkinter as tk
from formatter import format_changer

def run_app(on_search):
    root = tk.Tk()
    root.geometry("600x700")
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
    show_reverse_rates_var = tk.BooleanVar()
    tk.Checkbutton(fourth_frame, 
                   text="Show reverse rates", 
                   variable=show_reverse_rates_var).pack()
    calculate_spreads_var = tk.BooleanVar()
    tk.Checkbutton(fourth_frame, 
                   text="Calculate spreads", 
                   variable=calculate_spreads_var).pack()
    

    #Bottom Frame
    result_frame = tk.Frame(root, bg="yellow")
    result_frame.pack(fill="both", padx=10, pady=10)

    #Text of list of changers
    text = tk.Text(result_frame)
    text.pack(fill="both")
    #List of changers
    def on_click():
        from_code = from_input.get().upper()
        to_code = to_input.get().upper()
        if not from_code or not to_code:
            output.config(text="Please enter both currencies", fg="red")
            return
        direct_direction, reverse_direction, spreads = on_search(from_code, 
                                                        to_code, 
                                                        show_reverse_rates_enabled = show_reverse_rates_var.get(),
                                                        calculate_spreads_enabled = calculate_spreads_var.get())
        # try:
        #     direct_direction, reverse_direction = on_search(from_code, 
        #                                             to_code, 
        #                                             show_reverse_rates_enabled=show_reverse_rates_var.get())
        # except Exception as e:
        #     text.delete("1.0", "end")
        #     text.insert("end", f"Error: {e}")
        #     return               
        root.title("Exchange Rates")
        output.config(text=f"Loading {from_code} -> {to_code} ...")
        text.delete("1.0", "end")
        text.insert("end", f"{direct_direction}:\n")
        for d in direct_direction.rates.select_best(top=3):
            text.insert("end", format_changer(d) + "\n")
        if show_reverse_rates_var.get():
            text.delete("1.0", "end")
            text.insert("end", f"{reverse_direction} \n")
            for r in reverse_direction.selected_rates:
                text.insert("end", format_changer(r) + "\n")
        if calculate_spreads_var.get():
            text.delete("1.0", "end")
            text.insert("end", f"{direct_direction} --> {reverse_direction} \n")
            for s in spreads:
                text.insert("end", f"Spreads = {s} \n")
    btn.config(command=on_click)
############################################################
    #Setting menu
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    setting_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=setting_menu)
    setting_menu.add_command(label="Margin")
    setting_menu.add_command(label="Sort")
    setting_menu.add_separator()
    setting_menu.add_command(label="About")

    root.mainloop()