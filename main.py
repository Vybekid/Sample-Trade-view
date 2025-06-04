import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

class VybekidTradeView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vybekid TradeView")
        self.geometry("1100x650")
        self.configure(bg="#1e1e1e")

        self.prices = [100.0] * 40  # Start with flat prices
        self.max_points = 40

        self.create_widgets()
        self.update_chart_loop()

    def create_widgets(self):
        title = tk.Label(self, text="Vybekid TradeView", font=("Helvetica", 20, "bold"),
                         fg="white", bg="#1e1e1e")
        title.pack(pady=10)

        main_frame = tk.Frame(self, bg="#1e1e1e")
        main_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Chart frame
        chart_frame = tk.Frame(main_frame, bg="#2e2e2e", bd=2, relief="groove")
        chart_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(0, weight=3)

        self.chart_canvas = tk.Canvas(chart_frame, bg="black", width=700, height=400)
        self.chart_canvas.pack()

        # Right panel
        right_frame = tk.Frame(main_frame, bg="#2e2e2e", bd=2, relief="groove")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(1, weight=1)

        tk.Label(right_frame, text="Order Book", bg="#2e2e2e", fg="white", font=("Helvetica", 12, "bold")).pack()
        self.order_book = tk.Listbox(right_frame, bg="black", fg="lime", height=10)
        self.order_book.pack(fill="both", padx=5, pady=5)
        self.populate_orders()

        tk.Label(right_frame, text="Trade History", bg="#2e2e2e", fg="white", font=("Helvetica", 12, "bold")).pack()
        self.trade_history = tk.Listbox(right_frame, bg="black", fg="cyan", height=10)
        self.trade_history.pack(fill="both", padx=5, pady=5)
        self.populate_history()

        # Bottom frame
        bottom_frame = tk.Frame(main_frame, bg="#2e2e2e", bd=2, relief="groove")
        bottom_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.amount_var = tk.StringVar()
        ttk.Label(bottom_frame, text="Amount:", background="#2e2e2e", foreground="white").pack(pady=2)
        ttk.Entry(bottom_frame, textvariable=self.amount_var).pack(pady=2)

        ttk.Button(bottom_frame, text="Buy", command=self.buy_order).pack(pady=5)
        ttk.Button(bottom_frame, text="Sell", command=self.sell_order).pack(pady=5)

    def populate_orders(self):
        self.order_book.delete(0, tk.END)
        for i in range(10):
            price = round(random.uniform(99, 101), 2)
            volume = random.randint(1, 50)
            self.order_book.insert("end", f"{price} - {volume} BTC")

    def populate_history(self):
        self.trade_history.delete(0, tk.END)
        for _ in range(10):
            time = datetime.now().strftime("%H:%M:%S")
            price = round(random.uniform(99, 101), 2)
            self.trade_history.insert("end", f"{time} | {price} USD")

    def update_chart_loop(self):
        self.simulate_price()
        self.draw_chart()
        self.after(1000, self.update_chart_loop)

    def simulate_price(self):
        last_price = self.prices[-1]
        new_price = round(last_price + random.uniform(-0.3, 0.3), 2)
        self.prices.append(new_price)
        if len(self.prices) > self.max_points:
            self.prices.pop(0)

    def draw_chart(self):
        self.chart_canvas.delete("all")
        w = 700
        h = 400
        margin = 20
        chart_w = w - 2 * margin
        chart_h = h - 2 * margin

        max_price = max(self.prices)
        min_price = min(self.prices)
        price_range = max_price - min_price or 1

        x_scale = chart_w / (len(self.prices) - 1)
        y_scale = chart_h / price_range

        points = []
        for i, price in enumerate(self.prices):
            x = margin + i * x_scale
            y = margin + (max_price - price) * y_scale
            points.append((x, y))

        for i in range(1, len(points)):
            self.chart_canvas.create_line(points[i - 1][0], points[i - 1][1],
                                          points[i][0], points[i][1],
                                          fill="lime", width=2)

        # Draw border and title
        self.chart_canvas.create_text(w // 2, 15, text="Live Price Chart (Simulated)", fill="white", font=("Helvetica", 12, "bold"))
        self.chart_canvas.create_rectangle(margin, margin, w - margin, h - margin, outline="white")

    def buy_order(self):
        amt = self.amount_var.get()
        if amt:
            now = datetime.now().strftime("%H:%M:%S")
            self.trade_history.insert("end", f"{now} | Bought {amt} BTC")
            self.amount_var.set("")
            self.populate_orders()

    def sell_order(self):
        amt = self.amount_var.get()
        if amt:
            now = datetime.now().strftime("%H:%M:%S")
            self.trade_history.insert("end", f"{now} | Sold {amt} BTC")
            self.amount_var.set("")
            self.populate_orders()

if __name__ == "__main__":
    app = VybekidTradeView()
    app.mainloop()
