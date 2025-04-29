import tkinter as tk
import math
import winsound

class RetroCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Retro Bilimsel Hesap Makinesi")
        self.geometry("360x540")
        self.resizable(False, False)
        self.configure(bg="#1a1a1a")  # Koyu retro arka plan

        self.is_on = True

        self.result_var = tk.StringVar()

        self.display = tk.Entry(self, textvariable=self.result_var, font=("Fixedsys", 24, "bold"), bg="#003300", fg="#00FF00", bd=8, insertbackground='#00FF00', justify='right', state='normal')
        self.display.grid(row=0, column=0, columnspan=4, padx=15, pady=15, sticky="nsew")

        self.create_buttons()
        self.create_power_button()

        self.startup_animation()

    def create_buttons(self):
        button_cfg = {
            'font': ("Fixedsys", 16, "bold"),
            'bg': "#666666",
            'fg': "white",
            'activebackground': "#999999",
            'activeforeground': "white",
            'bd': 4,
            'relief': "ridge",
            'width': 4,
            'height': 2,
        }

        self.buttons = []

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("sin", 5, 0), ("cos", 5, 1), ("tan", 5, 2), ("log", 5, 3),
            ("sqrt", 6, 0), ("^", 6, 1), ("C", 6, 2)
        ]

        for (text, row, col) in buttons:
            if text in ["sin", "cos", "tan", "log", "sqrt"]:
                command = lambda t=text: self.button_click(self.calculate, t)
            elif text == "=":
                command = lambda: self.button_click(self.evaluate)
            elif text == "C":
                command = lambda: self.button_click(self.clear)
            else:
                command = lambda t=text: self.button_click(self.insert, t)

            btn = tk.Button(self, text=text, command=command, **button_cfg)
            btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            self.buttons.append(btn)

        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def create_power_button(self):
        power_btn = tk.Button(self, text="ON/OFF", font=("Fixedsys", 14, "bold"), bg="red", fg="white", command=self.toggle_power)
        power_btn.grid(row=6, column=3, padx=8, pady=8, sticky="nsew")

    def toggle_power(self):
        if self.is_on:
            self.result_var.set("Shutting Down...")
            winsound.Beep(300, 150)
            self.after(1000, self.power_off)
        else:
            self.display.config(state='normal', bg="#003300", fg="#00FF00")
            for btn in self.buttons:
                btn.config(state='normal')
            self.is_on = True
            self.result_var.set("Ready")
            self.after(1000, lambda: self.result_var.set(""))

    def power_off(self):
        self.display.config(state='disabled', disabledbackground='#000000', disabledforeground='#333333')
        for btn in self.buttons:
            btn.config(state='disabled')
        self.is_on = False

    def startup_animation(self):
        self.result_var.set("Booting...")
        winsound.Beep(400, 100)
        self.after(1000, lambda: self.result_var.set("Ready"))
        self.after(2000, lambda: self.result_var.set(""))

    def button_click(self, func, *args):
        if self.is_on:
            winsound.Beep(600, 50)  # Bip sesi (600 Hz, 50 ms)
            self.flash()
            self.shake()
            func(*args)

    def flash(self):
        original_color = self.display.cget("bg")
        self.display.config(bg="#005500")
        self.after(100, lambda: self.display.config(bg=original_color))

    def shake(self):
        original_x = self.winfo_x()
        original_y = self.winfo_y()
        for _ in range(2):
            self.geometry(f"360x540+{original_x + 5}+{original_y}")
            self.update()
            self.geometry(f"360x540+{original_x - 5}+{original_y}")
            self.update()
        self.geometry(f"360x540+{original_x}+{original_y}")

    def insert(self, char):
        current = self.result_var.get()
        self.result_var.set(current + str(char))

    def clear(self):
        self.result_var.set("")

    def evaluate(self):
        try:
            expression = self.result_var.get().replace("^", "**")
            self.result_var.set(str(eval(expression)))
        except:
            self.result_var.set("Error")

    def calculate(self, func):
        try:
            value = float(self.result_var.get())
            if func == "sin":
                self.result_var.set(str(math.sin(math.radians(value))))
            elif func == "cos":
                self.result_var.set(str(math.cos(math.radians(value))))
            elif func == "tan":
                self.result_var.set(str(math.tan(math.radians(value))))
            elif func == "log":
                if value <= 0:
                    self.result_var.set("Error")
                else:
                    self.result_var.set(str(math.log10(value)))
            elif func == "sqrt":
                if value < 0:
                    self.result_var.set("Error")
                else:
                    self.result_var.set(str(math.sqrt(value)))
        except:
            self.result_var.set("Error")

if __name__ == "__main__":
    app = RetroCalculator()
    app.mainloop()
