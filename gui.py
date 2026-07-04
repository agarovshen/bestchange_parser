import tkinter as tk
from formatter import format_changer

def run_app(on_search):
    root = tk.Tk()
    root.geometry("600x700")
    root.title("Arbitrage Bot")
    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", padx=10, pady=10)

    #From currency label
    tk.Label(top_frame, text="From e.g. BTC: ").pack(anchor="w", padx=5)
    from_input = tk.Entry(top_frame)
    from_input.pack(fill="x")

    #To currency label
    tk.Label(top_frame, text=("To e.g. USDT: ")).pack(anchor="w", padx=5)
    to_input = tk.Entry(top_frame)
    to_input.pack(fill="x")

    #Output label
    output = tk.Label(top_frame, text="")
    output.pack()\
    
    #Button
    btn = tk.Button(top_frame, text="GET RATES")
    btn.pack()

    #Bottom Frame
    result_frame = tk.Frame(root)
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
            result = on_search(from_code, to_code)
        except Exception as e:
            output.config(text=f"Error: {e}", fg="red")
            return
                
        root.title("Exchange Rates")
        output.config(text=f"Loading {from_code} -> {to_code} ...")
        text.delete("1.0", "end")

        for r in result:
            text.insert("end", format_changer(r) + "\n")
    
    btn.config(command=on_click)

    root.mainloop()