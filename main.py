import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

class VybekidTradeView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vybekid TradeView")
        self.geometry("1000x600")
        self.configure(bg="#1e1e1e")
        self.create_widgets()

    def create_widgets(self):
        # Top Title
        title = tk.Label(self, text="Vybekid TradeView", font=("Helvetica", 20, "bold"),
                         fg="white", bg="#1e1e1e")
        title.pack(pady=10)

        # Main frame
        main_frame = tk.Frame(self, bg="#1e1e1e")
        main_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Left Frame (Chart area)
        chart_frame = tk.Frame(main_frame, bg="#2e2e2e", bd=2, relief="groove")
        chart_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(0, weight=3)

        chart_canvas = tk.Canvas(chart_frame, bg="black", width=600, height=400)
        chart_canvas.pack()
        chart_canvas.create_text(300, 200, text="Price Chart Placeholder", fill="white", font=("Helvetica", 14))

        # Right Frame (Order book and history)
        right_frame = tk.Frame(main_frame, bg="#2e2e2e", bd=2, relief="groove")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(1, weight=1)

        # Order book
        order_label = tk.Label(right_frame, text="Order Book", bg="#2e2e2e", fg="white", font=("Helvetica", 12, "bold"))
        order_label.pack()
        self.order_book = tk.Listbox(right_frame, bg="black", fg="lime", height=10)
        self.order_book.pack(fill="both", padx=5, pady=5)
        self.populate_orders()

        # Trade history
        history_label = tk.Label(right_frame, text="Trade History", bg="#2e2e2e", fg="white", font=("Helvetica", 12, "bold"))
        history_label.pack()
        self.trade_history = tk.Listbox(right_frame, bg="black", fg="cyan", height=10)
        self.trade_history.pack(fill="both", padx=5, pady=5)
        self.populate_history()

        # Bottom frame (Buy/Sell controls)
        bottom_frame = tk.Frame(main_frame, bg="#2e2e2e", bd=2, relief="groove")
        bottom_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.amount_var = tk.StringVar()
        ttk.Label(bottom_frame, text="Amount:", background="#2e2e2e", foreground="white").pack(pady=2)
        ttk.Entry(bottom_frame, textvariable=self.amount_var).pack(pady=2)

        ttk.Button(bottom_frame, text="Buy", command=self.buy_order).pack(pady=5)
        ttk.Button(bottom_frame, text="Sell", command=self.sell_order).pack(pady=5)

    def populate_orders(self):
        for i in range(10):
            price = round(random.uniform(99, 101), 2)
            volume = random.randint(1, 50)
            self.order_book.insert("end", f"{price} - {volume} BTC")

    def populate_history(self):
        for _ in range(10):
            time = datetime.now().strftime("%H:%M:%S")
            price = round(random.uniform(99, 101), 2)
            self.trade_history.insert("end", f"{time} | {price} USD")

    def buy_order(self):
        amt = self.amount_var.get()
        if amt:
            now = datetime.now().strftime("%H:%M:%S")
            self.trade_history.insert("end", f"{now} | Bought {amt} BTC")
            self.amount_var.set("")

    def sell_order(self):
        amt = self.amount_var.get()
        if amt:
            now = datetime.now().strftime("%H:%M:%S")
            self.trade_history.insert("end", f"{now} | Sold {amt} BTC")
            self.amount_var.set("")

if __name__ == "__main__":
    app = VybekidTradeView()
    app.mainloop()
