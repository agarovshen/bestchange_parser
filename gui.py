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
    use_reverse_spread = tk.BooleanVar()
    check_reverse_spread = tk.Checkbutton(fourth_frame, text="Calculate reverse spread", variable=use_reverse_spread)
    check_reverse_spread.pack()
    

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
        
        try:
            direct_result, reverse_result = on_search(from_code, to_code, use_reverse_spread=False)
        except Exception as e:
            output.config(text=f"Error: {e}", fg="red")
            return
                
        root.title("Exchange Rates")
        output.config(text=f"Loading {from_code} -> {to_code} ...")
        text.delete("1.0", "end")
        print(f"Result: {direct_result}, Type: {type(direct_result)}")
        for r in direct_result:
            print(f"Result index: {r}, Type: {type(r)}\n")
            text.insert("end", format_changer(r) + "\n")
    
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