import tkinter as tk
from formatter import format_changer
from api_client import scan_arbitrage
from settings import ScannerSettings


def open_scanner_settings(settings, root):
    win = tk.Toplevel(root)
    win.title("Settings")
    win.geometry("200x160")

    tk.Label(win, text="Capital:").pack()
    cap_entry = tk.Entry(win)
    cap_entry.insert(0, str(settings.capital))
    cap_entry.pack()

    tk.Label(win, text="Currency:").pack()
    curr_entry = tk.Entry(win)
    curr_entry.insert(0, str(settings.currency))
    curr_entry.pack()

    err_label = tk.Label(win, text="", fg="red")
    err_label.pack()

    def save():
        try:
            settings.capital = float(cap_entry.get())
            settings.currency = curr_entry.get()
            win.destroy()
        except ValueError:
            err_label.config(text="Invalid input!")

    tk.Button(win, text="Save", command=save).pack(pady=2)


def run_app():
    root = tk.Tk()
    root.title("Scanner")
    root.geometry("600x400")

    settings = ScannerSettings(capital=1000, currency="USDTBEP20")

    top = tk.Frame(root)
    top.pack(fill=tk.X, pady=5)

    dirs_var = tk.IntVar(value=2)
    tk.Radiobutton(top, text="2D", variable=dirs_var, value=2).pack(side=tk.LEFT)
    tk.Radiobutton(top, text="3D", variable=dirs_var, value=3).pack(side=tk.LEFT)

    tk.Button(top, text="Settings", command=lambda: open_scanner_settings(settings, root)).pack(side=tk.LEFT, padx=10)

    txt = tk.Text(root, font=("Consolas", 10))
    txt.pack(fill=tk.BOTH, expand=True)

    def search():
        txt.delete("1.0", "end")
        cnt = dirs_var.get()
        results = scan_arbitrage(settings=settings, directions_var=cnt)
        for item in results:
            
            txt.insert("end", f"--- LOOP (Spread: {item['spread']}) ---\n")

            if cnt == 2:
                # 2D пары (Direct / Reverse)
                txt.insert("end", f"> Direct: {item['direct']}\n")
                for r in item.get("direct_rates", []):
                    ex, rate, lim = format_changer(r)
                    txt.insert("end", f"   Ex: {ex} | Rate: {rate} | Min: {lim}\n")

                txt.insert("end", f"> Reverse: {item['reverse']}\n")
                for r in item.get("reverse_rates", []):
                    ex, rate, lim = format_changer(r)
                    txt.insert("end", f"   Ex: {ex} | Rate: {rate} | Min: {lim}\n")

            elif cnt == 3:
                # 3D треугольники (AB / BC / CA)
                txt.insert("end", f"> AB: {item['direction_ab']}\n")
                for r in item.get("direction_ab_rates", []):
                    ex, rate, lim = format_changer(r)
                    txt.insert("end", f"   Ex: {ex} | Rate: {rate} | Min: {lim}\n")

                txt.insert("end", f"> BC: {item['direction_bc']}\n")
                for r in item.get("direction_bc_rates", []):
                    ex, rate, lim = format_changer(r)
                    txt.insert("end", f"   Ex: {ex} | Rate: {rate} | Min: {lim}\n")

                txt.insert("end", f"> CA: {item['direction_ca']}\n")
                for r in item.get("direction_ca_rates", []):
                    ex, rate, lim = format_changer(r)
                    txt.insert("end", f"   Ex: {ex} | Rate: {rate} | Min: {lim}\n")

            txt.insert("end", "\n")

    tk.Button(top, text="SEARCH", bg="green", fg="white", command=search).pack(side=tk.RIGHT, padx=5)
    root.mainloop()