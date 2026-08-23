import time
import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox
from formatter import format_changer
from settings import ScannerSettings

def open_scanner_settings(settings, root):
    # Предотвращаем открытие дубликатов окон
    if hasattr(open_scanner_settings, "window") and open_scanner_settings.window.winfo_exists():
        open_scanner_settings.window.focus()
        return

    window = tk.Toplevel(root)
    open_scanner_settings.window = window
    window.title("Scanner Settings")
    window.geometry("340x200")
    window.configure(bg="#21252b")
    window.resizable(False, False)
    
    window.transient(root)
    window.grab_set()

    main_frame = tk.Frame(window, bg="#21252b", padx=25, pady=25)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # --- Capital ---
    capital_frame = tk.Frame(main_frame, bg="#21252b")
    capital_frame.pack(fill=tk.X, pady=(0, 12))

    tk.Label(capital_frame, text="Capital:", bg="#21252b", fg="#abb2bf", font=("Segoe UI", 10)).pack(side=tk.LEFT)
    capital_var = tk.StringVar(value=str(settings.capital))
    capital_entry = tk.Entry(
        capital_frame, textvariable=capital_var, width=16,
        bg="#282c34", fg="#ffffff", insertbackground="white",
        relief="flat", highlightbackground="#3e4451", highlightthickness=1
    )
    capital_entry.pack(side=tk.RIGHT, ipady=4)

    # --- Currency ---
    currency_frame = tk.Frame(main_frame, bg="#21252b")
    currency_frame.pack(fill=tk.X, pady=(0, 20))

    tk.Label(currency_frame, text="Currency:", bg="#21252b", fg="#abb2bf", font=("Segoe UI", 10)).pack(side=tk.LEFT)
    currency_var = tk.StringVar(value=str(settings.currency))
    currency_entry = tk.Entry(
        currency_frame, textvariable=currency_var, width=16,
        bg="#282c34", fg="#ffffff", insertbackground="white",
        relief="flat", highlightbackground="#3e4451", highlightthickness=1
    )
    currency_entry.pack(side=tk.RIGHT, ipady=4)

    def save(event=None):
        try:
            capital = float(capital_var.get().replace(",", "."))
            currency = currency_var.get().strip()

            if capital <= 0 or not currency:
                raise ValueError

            settings.capital = capital
            settings.currency = currency
            window.destroy()

        except ValueError:
            messagebox.showerror(
                "Error", 
                "Please enter a valid positive Capital and non-empty Currency.", 
                parent=window
            )

    # Привязка горячих клавиш Enter / Esc
    window.bind("<Return>", save)
    window.bind("<Escape>", lambda e: window.destroy())

    save_btn = tk.Button(
        main_frame, text="Save Settings", command=save,
        bg="#61afef", fg="#1e1e1e", activebackground="#5294e2", activeforeground="#ffffff",
        font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2"
    )
    save_btn.pack(side=tk.BOTTOM, fill=tk.X, ipady=5)

    capital_entry.focus()


def run_app(on_search):
    root = tk.Tk()
    root.geometry("900x650")
    root.title("Arbitrage Scanner")
    root.configure(bg="#1e1e1e")

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # --- Стилизация TTK ---
    style = ttk.Style()
    available_themes = style.theme_names()
    for theme in ["clamp", "alt", "default"]:
        if theme in available_themes:
            style.theme_use(theme)
            break

    style.configure("Treeview",
                    background="#252526",
                    foreground="#d4d4d4",
                    fieldbackground="#252526",
                    rowheight=28,
                    font=("Segoe UI", 9),
                    borderwidth=0)
    
    style.configure("Treeview.Heading",
                    background="#1f1f1f",
                    foreground="#61afef",
                    font=("Segoe UI", 9, "bold"),
                    borderwidth=0)
    
    style.map("Treeview", background=[("selected", "#2c313a")])
    style.map("Treeview.Heading", background=[("active", "#252526")])

    style.configure("Slim.Horizontal.TProgressbar",
                    troughcolor="#1e1e1e",
                    background="#61afef",
                    thickness=2,
                    borderwidth=0)

    # --- Верхняя Панель ---
    top_frame = tk.Frame(root, bg="#252526", padx=20, pady=12, highlightbackground="#333333", highlightthickness=1)
    top_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 0))
    top_frame.grid_columnconfigure(1, weight=1)

    mode_frame = tk.Frame(top_frame, bg="#252526")
    mode_frame.grid(row=0, column=0, sticky="w")

    directions_var = tk.IntVar(value=2)

    rb1 = tk.Radiobutton(
        mode_frame, text="2 Directions Loop", variable=directions_var, value=2,
        bg="#252526", fg="#cccccc", selectcolor="#252526", activebackground="#252526",
        activeforeground="#61afef", font=("Segoe UI", 9, "bold")
    )
    rb1.pack(anchor="w")

    rb2 = tk.Radiobutton(
        mode_frame, text="3 Directions Loop", variable=directions_var, value=3,
        bg="#252526", fg="#cccccc", selectcolor="#252526", activebackground="#252526",
        activeforeground="#61afef", font=("Segoe UI", 9, "bold")
    )
    rb2.pack(anchor="w")

    btn = tk.Button(
        top_frame, text="SEARCH ARBITRAGE", bg="#98c379", fg="#1e1e1e",
        activebackground="#7ea662", activeforeground="#ffffff",
        font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2"
    )
    btn.grid(row=0, column=2, sticky="e", ipadx=18, ipady=6)

    # --- Полоса загрузки ---
    progress_frame = tk.Frame(root, bg="#1e1e1e", height=18)
    progress_frame.grid_columnconfigure(0, weight=1)

    status_label = tk.Label(progress_frame, text="", bg="#1e1e1e", fg="#e5c07b", font=("Segoe UI", 8))
    status_label.grid(row=0, column=0, sticky="w")

    timer_label = tk.Label(progress_frame, text="", bg="#1e1e1e", fg="#61afef", font=("Segoe UI", 8, "bold"))
    timer_label.grid(row=0, column=1, sticky="e")

    progress_bar = ttk.Progressbar(progress_frame, style="Slim.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
    progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    # --- Нижняя Панель ---
    result_frame = tk.Frame(root, bg="#1e1e1e")
    result_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=10)
    result_frame.grid_rowconfigure(0, weight=1)
    result_frame.grid_columnconfigure(0, weight=1)

    columns = ("exchange", "rate", "min_limit")
    tree = ttk.Treeview(result_frame, columns=columns, show="tree headings")
    
    tree.heading("#0", text=" DIRECTION / STEP", anchor="w")
    tree.heading("exchange", text="EXCHANGER", anchor="w")
    tree.heading("rate", text="RATE", anchor="w")
    tree.heading("min_limit", text="MIN LIMIT", anchor="w")

    tree.column("#0", width=320, stretch=True)
    tree.column("exchange", width=200, anchor="w")
    tree.column("rate", width=150, anchor="w")
    tree.column("min_limit", width=150, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    tree.tag_configure("parent_2d", background="#21252b", foreground="#c678dd", font=("Segoe UI", 10, "bold"))
    tree.tag_configure("parent_3d", background="#21252b", foreground="#56b6c2", font=("Segoe UI", 10, "bold"))
    tree.tag_configure("step_header", background="#282c34", foreground="#abb2bf", font=("Segoe UI", 9, "bold"))
    tree.tag_configure("spread_row", background="#1e2227", foreground="#98c379", font=("Segoe UI", 10, "bold"))

    settings = ScannerSettings(capital=1000, currency="USDTBEP20")

    # Очередь сообщений для безопасной передачи из фонового потока
    result_queue = queue.Queue()

    def start_search_thread():
        btn.config(state=tk.DISABLED)
        progress_bar["value"] = 0
        
        progress_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(2, 0))
        status_label.config(text="Scanning... 0%", fg="#e5c07b")
        timer_label.config(text="0.0s")
        
        start_time = time.time()

        def update_ui_loop():
            # Проверяем, пришли ли данные из фонового потока
            try:
                results, directions_count, total_time = result_queue.get_nowait()
                render_results(results, directions_count, total_time)
                return
            except queue.Empty:
                pass

            # Обновление UI прогресса строго в главном потоке
            elapsed = time.time() - start_time
            timer_label.config(text=f"{elapsed:.1f}s")

            current_val = progress_bar["value"]
            if current_val < 95:
                next_val = min(95, current_val + 2.0)
                progress_bar["value"] = next_val
                status_label.config(text=f"Scanning... {int(next_val)}%")

            root.after(80, update_ui_loop)

        def worker():
            directions_count = directions_var.get()
            results = on_search(settings=settings, directions_var=directions_count)
            total_time = time.time() - start_time
            result_queue.put((results, directions_count, total_time))

        threading.Thread(target=worker, daemon=True).start()
        update_ui_loop()

    def render_results(results, directions_count, total_time):
        for item in tree.get_children():
            tree.delete(item)

        if directions_count == 2:
            root.title(f"Exchange Rates — 2 Directions ({total_time:.2f}s)")
            for idx, direction in enumerate(results, 1):
                node_id = tree.insert("", "end", text=f"  PAIRS LOOP #{idx}", values=("", "", ""), tags=("parent_2d",), open=True)
                
                d_node = tree.insert(node_id, "end", text=f"  ► Direct: {direction['direct']}", tags=("step_header",), open=True)
                for rate in direction.get('direct_rates', []):
                    tree.insert(d_node, "end", text="", values=format_changer(rate))

                r_node = tree.insert(node_id, "end", text=f"  ◄ Reverse: {direction['reverse']}", tags=("step_header",), open=True)
                for rate in direction.get('reverse_rates', []):
                    tree.insert(r_node, "end", text="", values=format_changer(rate))

                tree.insert(node_id, "end", text=f"  ★ SPREAD: {direction['spread']}", values=("", "", ""), tags=("spread_row",))

        elif directions_count == 3:
            root.title(f"Exchange Rates — 3 Directions ({total_time:.2f}s)")
            for idx, cycle in enumerate(results, 1):
                node_id = tree.insert("", "end", text=f"  TRIANGLE LOOP #{idx}", values=("", "", ""), tags=("parent_3d",), open=True)

                # Унифицированная обработка списков / словарей для 3D
                for key_dir, key_rates in [('direction_ab', 'direction_ab_rates'), 
                                           ('direction_bc', 'direction_bc_rates'), 
                                           ('direction_ca', 'direction_ca_rates')]:
                    dir_node = tree.insert(node_id, "end", text=f"  ► {cycle[key_dir]}", tags=("step_header",), open=True)
                    rates = cycle[key_rates]
                    rates_list = rates if isinstance(rates, list) else [rates]
                    for rate in rates_list:
                        tree.insert(dir_node, "end", text="", values=format_changer(rate))

                tree.insert(node_id, "end", text=f"  ★ SPREAD: {cycle['spread']}", values=("", "", ""), tags=("spread_row",))

        progress_frame.grid_forget()
        btn.config(state=tk.NORMAL)

    btn.config(command=start_search_thread)

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    setting_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=setting_menu)
    setting_menu.add_command(label="Scanner Settings", command=lambda: open_scanner_settings(settings, root))
    setting_menu.add_separator()
    setting_menu.add_command(label="About")

    root.mainloop()