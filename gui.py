import queue
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

from formatter import format_changer
from settings import ScannerSettings


# ============================================================
# UI CONSTANTS
# ============================================================

BG = "#1e1e1e"
FRAME_BG = "#252526"
DARK_BG = "#21252b"
ENTRY_BG = "#282c34"
BORDER = "#333333"

TEXT = "#d4d4d4"
TEXT_SECONDARY = "#abb2bf"

BLUE = "#61afef"
GREEN = "#98c379"
YELLOW = "#e5c07b"
PURPLE = "#c678dd"
CYAN = "#56b6c2"

FONT = ("Segoe UI", 9)
FONT_BOLD = ("Segoe UI", 9, "bold")


# ============================================================
# SCANNER SETTINGS WINDOW
# ============================================================

def create_setting_entry(parent, label, value, pady):
    var = tk.StringVar(value=str(value))
    frame = tk.Frame(parent, bg=DARK_BG)
    frame.pack(fill=tk.X, pady=pady)
    tk.Label(frame, text=f"{label}:", bg=DARK_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 10)).pack(side=tk.LEFT)
    entry = tk.Entry(frame, textvariable=var, width=16, bg=ENTRY_BG, fg="white", insertbackground="white", relief="flat", highlightbackground="#3e4451", highlightthickness=1)
    entry.pack(side=tk.RIGHT, ipady=4)
    return var, entry


def open_scanner_settings(settings, root):
    if hasattr(root, "_scanner_settings_window"):
        window = root._scanner_settings_window
        if window.winfo_exists():
            window.focus()
            return

    window = root._scanner_settings_window = tk.Toplevel(root)
    window.title("Scanner Settings")
    window.geometry("340x200")
    window.configure(bg=DARK_BG)
    window.resizable(False, False)
    window.transient(root)
    window.grab_set()

    main_frame = tk.Frame(window, bg=DARK_BG, padx=25, pady=25)
    main_frame.pack(fill=tk.BOTH, expand=True)

    capital_var, capital_entry = create_setting_entry(main_frame, "Capital", settings.capital, (0, 12))
    currency_var, currency_entry = create_setting_entry(main_frame, "Currency", settings.currency, (0, 20))

    def save(event=None):
        try:
            capital = float(capital_var.get().replace(",", "."))
            currency = currency_var.get().strip()
            if capital <= 0 or not currency:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive Capital and non-empty Currency.", parent=window)
            return

        settings.capital = capital
        settings.currency = currency
        window.grab_release()
        window.destroy()

    def close(event=None):
        window.grab_release()
        window.destroy()

    window.bind("<Return>", save)
    window.bind("<Escape>", close)

    tk.Button(main_frame, text="Save Settings", command=save, bg=BLUE, fg="#1e1e1e", activebackground="#5294e2", activeforeground="white", font=FONT_BOLD, relief="flat", cursor="hand2").pack(side=tk.BOTTOM, fill=tk.X, ipady=5)

    capital_entry.focus()


# ============================================================
# MAIN APPLICATION
# ============================================================

def run_app(on_search):
    root = tk.Tk()
    root.title("Arbitrage Scanner")
    root.geometry("900x650")
    root.configure(bg=BG)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # ========================================================
    # TTK STYLE
    # ========================================================

    style = ttk.Style()

    for theme in ("clam", "alt", "default"):
        if theme in style.theme_names():
            style.theme_use(theme)
            break

    style.configure("Treeview", background="#252526", foreground=TEXT, fieldbackground="#252526", rowheight=28, font=FONT, borderwidth=0)
    style.configure("Treeview.Heading", background="#1f1f1f", foreground=BLUE, font=FONT_BOLD, borderwidth=0)
    style.map("Treeview", background=[("selected", "#2c313a")])
    style.map("Treeview.Heading", background=[("active", "#252526")])
    style.configure("Slim.Horizontal.TProgressbar", troughcolor=BG, background=BLUE, thickness=2, borderwidth=0)

    # ========================================================
    # TOP PANEL
    # ========================================================

    top_frame = tk.Frame(root, bg=FRAME_BG, padx=20, pady=12, highlightbackground=BORDER, highlightthickness=1)
    top_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 0))
    top_frame.grid_columnconfigure(1, weight=1)

    directions_var = tk.IntVar(value=2)

    mode_frame = tk.Frame(top_frame, bg=FRAME_BG)
    mode_frame.grid(row=0, column=0, sticky="w")

    radio_config = {"bg": FRAME_BG, "fg": "#cccccc", "selectcolor": FRAME_BG, "activebackground": FRAME_BG, "activeforeground": BLUE, "font": FONT_BOLD}

    for text, value in (("2 Directions Loop", 2), ("3 Directions Loop", 3)):
        tk.Radiobutton(mode_frame, text=text, variable=directions_var, value=value, **radio_config).pack(anchor="w")

    btn = tk.Button(top_frame, text="SEARCH ARBITRAGE", bg=GREEN, fg="#1e1e1e", activebackground="#7ea662", activeforeground="white", font=FONT_BOLD, relief="flat", cursor="hand2")
    btn.grid(row=0, column=2, sticky="e", ipadx=18, ipady=6)

    # ========================================================
    # PROGRESS
    # ========================================================

    progress_frame = tk.Frame(root, bg=BG)
    progress_frame.grid_columnconfigure(0, weight=1)

    status_label = tk.Label(progress_frame, text="", bg=BG, fg=YELLOW, font=("Segoe UI", 8))
    status_label.grid(row=0, column=0, sticky="w")

    timer_label = tk.Label(progress_frame, text="", bg=BG, fg=BLUE, font=("Segoe UI", 8, "bold"))
    timer_label.grid(row=0, column=1, sticky="e")

    progress_bar = ttk.Progressbar(progress_frame, style="Slim.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
    progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    # ========================================================
    # RESULTS
    # ========================================================

    result_frame = tk.Frame(root, bg=BG)
    result_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
    result_frame.grid_rowconfigure(0, weight=1)
    result_frame.grid_columnconfigure(0, weight=1)

    columns = ("exchange", "rate", "min_limit")
    tree = ttk.Treeview(result_frame, columns=columns, show="tree headings")

    headings = {"#0": " DIRECTION / STEP", "exchange": "EXCHANGER", "rate": "RATE", "min_limit": "MIN LIMIT"}

    for column, text in headings.items():
        tree.heading(column, text=text, anchor="w")

    for column, width in (("#0", 320), ("exchange", 200), ("rate", 150), ("min_limit", 150)):
        tree.column(column, width=width, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    # ========================================================
    # TREE TAGS
    # ========================================================

    tree.tag_configure("parent_2d", background=DARK_BG, foreground=PURPLE, font=("Segoe UI", 10, "bold"))
    tree.tag_configure("parent_3d", background=DARK_BG, foreground=CYAN, font=("Segoe UI", 10, "bold"))
    tree.tag_configure("step_header", background="#282c34", foreground=TEXT_SECONDARY, font=FONT_BOLD)
    tree.tag_configure("spread_row", background="#1e2227", foreground=GREEN, font=("Segoe UI", 10, "bold"))

    # ========================================================
    # SETTINGS
    # ========================================================

    settings = ScannerSettings(capital=1000, currency="USDTBEP20")
    result_queue = queue.Queue()

    # ========================================================
    # RENDER HELPERS
    # ========================================================

    def render_rates(parent, rates):
        for rate in rates if isinstance(rates, list) else [rates]:
            tree.insert(parent, "end", text="", values=format_changer(rate))

    def render_direction(parent, label, direction, rates):
        node = tree.insert(parent, "end", text=f"  {label}: {direction}", tags=("step_header",), open=True)
        render_rates(node, rates)

    # ========================================================
    # RENDER RESULTS
    # ========================================================

    def render_results(results, directions_count, total_time):
        for item in tree.get_children():
            tree.delete(item)

        root.title(f"Exchange Rates — {directions_count} Directions ({total_time:.2f}s)")

        if directions_count == 2:
            for idx, direction in enumerate(results, 1):
                node = tree.insert("", "end", text=f"  PAIRS LOOP #{idx}", values=("", "", ""), tags=("parent_2d",), open=True)
                render_direction(node, "► Direct", direction["direct"], direction.get("direct_rates", []))
                render_direction(node, "◄ Reverse", direction["reverse"], direction.get("reverse_rates", []))
                tree.insert(node, "end", text=f"  ★ SPREAD: {direction['spread']}", values=("", "", ""), tags=("spread_row",))

        elif directions_count == 3:
            for idx, cycle in enumerate(results, 1):
                node = tree.insert("", "end", text=f"  TRIANGLE LOOP #{idx}", values=("", "", ""), tags=("parent_3d",), open=True)

                for label, key, rates_key in (("►", "direction_ab", "direction_ab_rates"), ("►", "direction_bc", "direction_bc_rates"), ("►", "direction_ca", "direction_ca_rates")):
                    render_direction(node, label, cycle[key], cycle[rates_key])

                tree.insert(node, "end", text=f"  ★ SPREAD: {cycle['spread']}", values=("", "", ""), tags=("spread_row",))

        progress_frame.grid_forget()
        btn.config(state=tk.NORMAL)

    # ========================================================
    # SEARCH
    # ========================================================

    def start_search_thread():
        btn.config(state=tk.DISABLED)
        progress_bar["value"] = 0
        progress_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(2, 0))
        status_label.config(text="Scanning... 0%", fg=YELLOW)
        timer_label.config(text="0.0s")

        start_time = time.perf_counter()

        def update_ui_loop():
            try:
                result = result_queue.get_nowait()
            except queue.Empty:
                elapsed = time.perf_counter() - start_time
                timer_label.config(text=f"{elapsed:.1f}s")
                current = progress_bar["value"]

                if current < 95:
                    current = min(95, current + 2)
                    progress_bar["value"] = current
                    status_label.config(text=f"Scanning... {int(current)}%")

                root.after(80, update_ui_loop)
                return

            results, directions_count, total_time = result
            progress_bar["value"] = 100
            status_label.config(text="Completed", fg=GREEN)
            render_results(results, directions_count, total_time)

        def worker():
            directions_count = directions_var.get()
            results = on_search(settings=settings, directions_var=directions_count)
            total_time = time.perf_counter() - start_time
            result_queue.put((results, directions_count, total_time))

        threading.Thread(target=worker, daemon=True).start()
        update_ui_loop()

    btn.config(command=start_search_thread)

    # ========================================================
    # MENU
    # ========================================================

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    settings_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)

    settings_menu.add_command(label="Scanner Settings", command=lambda: open_scanner_settings(settings, root))
    settings_menu.add_separator()
    settings_menu.add_command(label="About")

    root.mainloop()