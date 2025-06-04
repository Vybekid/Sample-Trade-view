import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

class VybekidTradeView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vybekid TradeView")
        self.geometry("1100x650")
        self.configure(bg="#1e1e1e")

        # Data for chart simulation
        self.prices = [100.0]
        self.times = [datetime.now().strftime("%H:%M:%S")]

        self.create_widgets()

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

        # Create and embed matplotlib chart
        self.fig, self.ax = plt.subplots(figsize=(7, 4), facecolor="#2e2e2e")
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.ax.set_facecolor("black")
        self.ax.tick_params(colors="white")
        self.ax.set_title("Live Price Chart", color="white")

        # Right panel: Order Book + Trade History
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

        # Buy/Sell Section
        bottom_frame = tk.Frame(main_frame, bg="#2e2e2e", bd=2, relief="groove")
        bottom_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.amount_var = tk.StringVar()
        ttk.Label(bottom_frame, text="Amount:", background="#2e2e2e", foreground="white").pack(pady=2)
        ttk.Entry(bottom_frame, textvariable=self.amount_var).pack(pady=2)

        ttk.Button(bottom_frame, text="Buy", command=self.buy_order).pack(pady=5)
        ttk.Button(bottom_frame, text="Sell", command=self.sell_order).pack(pady=5)

        # Animate chart
        self.ani = animation.FuncAnimation(self.fig, self.update_chart, interval=1000)

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

    def update_chart(self, i):
        # Simulate new price
        new_price = self.prices[-1] + random.uniform(-0.3, 0.3)
        self.prices.append(round(new_price, 2))
        self.times.append(datetime.now().strftime("%H:%M:%S"))

        # Limit history to last 20
        self.prices = self.prices[-20:]
        self.times = self.times[-20:]

        self.ax.clear()
        self.ax.plot(self.times, self.prices, color='lime', linewidth=2)
        self.ax.set_facecolor("black")
        self.ax.tick_params(colors="white", rotation=45)
        self.ax.set_title("Live Price Chart", color="white")
        self.fig.tight_layout()
        self.canvas.draw()

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
