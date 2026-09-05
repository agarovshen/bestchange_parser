import tkinter as tk
from tkinter import ttk
from formatter import format_changer
from api_client import scan_arbitrage
from settings import ScannerSettings

# --- Палитра тёмной темы ---
BG_MAIN = "#1e1e2e"       # Основной фон (Catppuccin Mocha)
BG_PANEL = "#181825"      # Фон панелей и карточек
BG_FIELD = "#313244"      # Фон полей ввода и текстового блока
FG_TEXT = "#cdd6f4"       # Основной цвет текста
FG_SUBTEXT = "#a6adc8"    # Второстепенный текст
ACCENT_GREEN = "#a6e3a1"  # Зелёный акцент для кнопки поиска
ACCENT_BLUE = "#89b4fa"   # Голубой акцент для заголовков и линий
ACCENT_RED = "#f38ba8"    # Красный цвет ошибок
BORDER_COLOR = "#45475a"  # Цвет границ


def open_scanner_settings(settings, root):
    win = tk.Toplevel(root)
    win.title("Settings")
    win.geometry("260x210")
    win.configure(bg=BG_MAIN)
    win.resizable(False, False)

    # Делаем окно модальным (поверх основного)
    win.transient(root)
    win.grab_set()

    padding_frame = tk.Frame(win, bg=BG_MAIN, padx=20, pady=15)
    padding_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(
        padding_frame, text="Capital:", bg=BG_MAIN, fg=FG_SUBTEXT, font=("Segoe UI", 9)
    ).pack(anchor="w")
    cap_entry = tk.Entry(
        padding_frame,
        bg=BG_FIELD,
        fg=FG_TEXT,
        insertbackground=FG_TEXT,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
        highlightcolor=ACCENT_BLUE,
        font=("Segoe UI", 10),
    )
    cap_entry.insert(0, str(settings.capital))
    cap_entry.pack(fill=tk.X, pady=(2, 10), ipady=3)

    tk.Label(
        padding_frame, text="Currency:", bg=BG_MAIN, fg=FG_SUBTEXT, font=("Segoe UI", 9)
    ).pack(anchor="w")
    curr_entry = tk.Entry(
        padding_frame,
        bg=BG_FIELD,
        fg=FG_TEXT,
        insertbackground=FG_TEXT,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
        highlightcolor=ACCENT_BLUE,
        font=("Segoe UI", 10),
    )
    curr_entry.insert(0, str(settings.currency))
    curr_entry.pack(fill=tk.X, pady=(2, 5), ipady=3)

    err_label = tk.Label(padding_frame, text="", fg=ACCENT_RED, bg=BG_MAIN, font=("Segoe UI", 8))
    err_label.pack(pady=2)

    def save():
        try:
            settings.capital = float(cap_entry.get())
            settings.currency = curr_entry.get()
            win.destroy()
        except ValueError:
            err_label.config(text="Invalid input!")

    save_btn = tk.Button(
        padding_frame,
        text="Save",
        command=save,
        bg=BG_FIELD,
        fg=FG_TEXT,
        activebackground=BORDER_COLOR,
        activeforeground=FG_TEXT,
        bd=0,
        relief=tk.FLAT,
        font=("Segoe UI", 9, "bold"),
        cursor="hand2",
    )
    save_btn.pack(fill=tk.X, pady=(5, 0), ipady=4)


def run_app():
    root = tk.Tk()
    root.title("Scanner")
    root.geometry("680x480")
    root.configure(bg=BG_MAIN)

    # Настройка стилей ttk для радиокнопок
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Dark.TRadiobutton",
        background=BG_PANEL,
        foreground=FG_TEXT,
        font=("Segoe UI", 9, "bold"),
        focuscolor=BG_PANEL,
    )
    style.map(
        "Dark.TRadiobutton",
        background=[("active", BG_PANEL)],
        foreground=[("active", ACCENT_BLUE)],
    )

    settings = ScannerSettings(capital=1000, currency="USDTBEP20")

    # Панель управления (Top Bar)
    top = tk.Frame(root, bg=BG_PANEL, padx=12, pady=10)
    top.pack(fill=tk.X, side=tk.TOP)

    dirs_var = tk.IntVar(value=2)

    # Радиокнопки
    rb2 = ttk.Radiobutton(top, text="2D", variable=dirs_var, value=2, style="Dark.TRadiobutton")
    rb2.pack(side=tk.LEFT, padx=(0, 5))
    rb3 = ttk.Radiobutton(top, text="3D", variable=dirs_var, value=3, style="Dark.TRadiobutton")
    rb3.pack(side=tk.LEFT, padx=(0, 15))

    # Кнопка Settings
    settings_btn = tk.Button(
        top,
        text="⚙ Settings",
        command=lambda: open_scanner_settings(settings, root),
        bg=BG_FIELD,
        fg=FG_TEXT,
        activebackground=BORDER_COLOR,
        activeforeground=FG_TEXT,
        bd=0,
        font=("Segoe UI", 9, "bold"),
        padx=10,
        cursor="hand2",
    )
    settings_btn.pack(side=tk.LEFT)

    # Кнопка SEARCH
    search_btn = tk.Button(
        top,
        text="SEARCH",
        bg=ACCENT_GREEN,
        fg=BG_PANEL,
        activebackground="#89dceb",
        activeforeground=BG_PANEL,
        bd=0,
        font=("Segoe UI", 9, "bold"),
        padx=15,
        cursor="hand2",
    )
    search_btn.pack(side=tk.RIGHT)

    # Контейнер с текстовым полем и скроллбаром
    container = tk.Frame(root, bg=BG_MAIN, padx=10, pady=10)
    container.pack(fill=tk.BOTH, expand=True)

    txt = tk.Text(
        container,
        font=("Consolas", 10),
        bg=BG_FIELD,
        fg=FG_TEXT,
        insertbackground=FG_TEXT,
        selectbackground=BORDER_COLOR,
        selectforeground=FG_TEXT,
        bd=0,
        padx=10,
        pady=10,
        wrap=tk.WORD,
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
    )

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=txt.yview)
    txt.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Цветовые теги для консольного вывода
    txt.tag_configure("loop_header", foreground=ACCENT_BLUE, font=("Consolas", 10, "bold"))
    txt.tag_configure("dir_name", foreground=ACCENT_GREEN, font=("Consolas", 10, "bold"))
    txt.tag_configure("sub_info", foreground=FG_SUBTEXT)

    def search():
        txt.delete("1.0", "end")
        cnt = dirs_var.get()
        results = scan_arbitrage(settings=settings, directions_var=cnt)
        print("3. results in gui")

        for item in results:
            txt.insert("end", f"--- LOOP (Spread: {item['spread']}) ---\n", "loop_header")

            if cnt == 2:
                for name, direction_name, rate in (
                    ("Direct", item.get("direct_name", {}), item.get("best_direct_rate", {})),
                    ("Reverse", item.get("reverse_name", {}), item.get("best_reverse_rate", {})),
                ):
                    ex, best_rate, lim = format_changer(rate)
                    txt.insert("end", f"> {name}: {direction_name}\n", "dir_name")
                    txt.insert("end", f"   Ex: {ex} | Rate: {best_rate} | Min: {lim}\n", "sub_info")

            elif cnt == 3:
                # 3D треугольники (AB / BC / CA)
                txt.insert("end", f"> AB: {item['direction_ab']}\n", "dir_name")
                for r in item.get("direction_ab_rates", []):
                    ex, rate, lim = format_changer(r)
                    txt.insert("end", f"   Ex: {ex} | Rate: {rate} | Min: {lim}\n", "sub_info")

                txt.insert("end", f"> BC: {item['direction_bc']}\n", "dir_name")
                for r in item.get("direction_bc_rates", []):
                    ex, rate, lim = format_changer(r)
                    txt.insert("end", f"   Ex: {ex} | Rate: {rate} | Min: {lim}\n", "sub_info")

                txt.insert("end", f"> CA: {item['direction_ca']}\n", "dir_name")
                for r in item.get("direction_ca_rates", []):
                    ex, rate, lim = format_changer(r)
                    txt.insert("end", f"   Ex: {ex} | Rate: {rate} | Min: {lim}\n", "sub_info")

            txt.insert("end", "\n")

    # Привязываем команду к кнопке поиска после объявления функции
    search_btn.config(command=search)

    root.mainloop()