import tkinter as tk

label_clr = "#1E686E"
gray = "#DBD9D9"
sml_font_style = ("Arial", 40)
lrg_font_style = ("Arial", 60, "bold")
button_clr = "#000000"  # black color for the numbers
off_white = "#F8FAFF"
lgt_blue = "#CCEDFF"
default_font = ("Arial", 45)
button_digit_font = ("Arial", 45)

orange = "#FFA500"
red = "#990000"
Blue = "#4A22E6"


# ^ colors and fonts that will be used within the calculator

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("376x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        # ^ unicode values that print the symbols for '/' and '*'

        self.total_labels, self.label = self.create_display_labels()
        self.buttons_frame = self.create_buttons_frame()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            ".": (4, 1), 0: (4, 2)
        }

        self.buttons_frame.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(i, weight=1)

        self.create_digit_buttons()
        self.create_operator_button()
        self.create_special_buttons()
        self.key_binds()

    def key_binds(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for keys in self.digits:
            self.window.bind(str(keys), lambda event, digit=keys: self.add_to_expression(digit))
        for keys in self.operations:
            self.window.bind(keys, lambda event, operator=keys: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_labels = tk.Label(self.display_frame, text=self.total_expression,
                                anchor=tk.E, bg=gray, fg=label_clr, padx=25, font=sml_font_style)
        total_labels.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression,
                         anchor=tk.E, bg=gray, fg=label_clr, padx=25, font=lrg_font_style)
        label.pack(expand=True, fill="both")

        return total_labels, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=gray)
        frame.pack(expand=True, fill="both")
        return frame

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=button_clr, fg=label_clr, font=button_digit_font,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_button(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=off_white, fg=red, font=default_font,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=off_white, fg=orange, font=default_font,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=off_white, fg=red, font=default_font,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=off_white, fg=red, font=default_font,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_label()

        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""

        except Exception as e:
            self.current_expression = "Error"

        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=lgt_blue, fg=red, font=default_font,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ")
        self.total_labels.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:6])

    def run(self) -> object:
        self.window.mainloop()


if __name__ == '__main__':
    calc = Calculator()
    calc.run()
