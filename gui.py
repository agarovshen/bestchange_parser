import tkinter as tk
def run_app():
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Arbitrage Bot")
    label = tk.Label(root, text="Hello Gui")
    label.pack()
    root.mainloop()