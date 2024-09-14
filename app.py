import random

from customtkinter import *
from dependencies.config import *
import pyperclip
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class App(CTk):
    def __init__(self):

        # main setup
        super().__init__(fg_color=FOREST_GREEN)
        self.title('')
        self.iconbitmap('dependencies/empty.ico')
        self.geometry('350x300')
        self.resizable(width=False, height=False)
        self.change_title_bar_color()

        # layout
        self.columnconfigure(0, weight = 1)
        self.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1, uniform='a')

        # data
        self.amount_int = IntVar(value=20)
        self.num_bool = BooleanVar(value=False)
        self.sym_bool = BooleanVar(value=False)

        # functions
        def copy_password():
            password = self.result_field.get()
            pyperclip.copy(password)

        # tracing
        self.amount_int.trace('w', self.randomize_password)

        # widgets
        SmallTitle(self, 'Customize your password', 0)
        BlankLine(self, 1)
        CharactersSlider(self, self.amount_int)
        BlankLine(self, 3)
        Switches(self, self.num_bool, self.sym_bool)
        BlankLine(self, 5)
        SmallTitle(self, 'Generated Password', 6)
        ResultField(self)
        CopyButton(self, copy_password)
        BlankLine(self, 9)

        # run
        self.randomize_password(None, None, None)
        self.mainloop()

    def randomize_password(self, a, b, c):
        password = ''
        letters = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z'
        ]
        nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '@', '#', '$', '%', '^', '&', '*']

        combined_list = letters

        if self.num_bool.get():
            combined_list += nums

        if self.sym_bool.get():
            combined_list += symbols

        for i in range(0, self.amount_int.get()):
            password += random.choice(combined_list)

        self.result_field = ResultField(self)
        self.result_field.set_password(password)

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass


class SmallTitle(CTkLabel):
    def __init__(self, parent, text, c_row):
        font = CTkFont(family=FONT, size=TITLES_TEXT_SIZE, weight='bold')
        super().__init__(master=parent, text=text, font=font, text_color=MOSS_GREEN)
        self.grid(column=0, row=c_row, sticky='w', padx=15)


class BlankLine(CTkFrame):
    def __init__(self, parent, c_row):
        super().__init__(master=parent, fg_color=MOSS_GREEN)
        self.grid(column=0, row=c_row, sticky='nsew', padx=15, pady=14)


class CharactersSlider(CTkFrame):
    def __init__(self, parent, amount_int):
        super().__init__(master=parent, fg_color=FOREST_GREEN)
        self.grid(column=0, row=2, sticky='nsew', padx=10)

        title_text = CTkLabel(self, text='Characters', text_color=WHITE, font=CTkFont(family=FONT, size=TITLES_TEXT_SIZE))
        title_text.pack(side='left', padx=5)

        # widgets
        slider = CTkSlider(
            master=self,
            command=self.update_text,
            button_color=WHITE,
            button_hover_color=WHITE,
            progress_color=MOSS_GREEN,
            fg_color=LIGHT_GRAY,
            variable=amount_int,
            from_=4,
            to=35
        )
        slider.pack(side='left', expand=True)

        self.output_string = StringVar()
        self.update_text(amount_int.get())

        self.output_text = CTkLabel(self, textvariable=self.output_string, text='20', text_color=WHITE, font=CTkFont(family=FONT, size=INPUT_FONT_SIZE))
        self.output_text.pack(side='left', padx=5)

    def update_text(self, amount):
        text_string = str(int(amount))
        self.output_string.set(text_string)

    def get_output_text(self):
        return self.output_text.cget("text")


class Switches(CTkFrame):
    def __init__(self, parent, num_bool, sym_bool):
        super().__init__(master=parent, fg_color=FOREST_GREEN)
        self.grid(column=0, row=4, sticky='nsew', padx=10)

        num_switch = CTkSwitch(
            master=self,
            button_color=WHITE,
            button_hover_color=WHITE,
            progress_color=MOSS_GREEN,
            text='Numbers',
            text_color=WHITE,
            font=CTkFont(family=FONT, size=TITLES_TEXT_SIZE),
            fg_color=LIGHT_GRAY,
            variable=num_bool
        )
        num_switch.pack(side='left', padx=5)

        sym_switch = CTkSwitch(
            master=self,
            button_color=WHITE,
            button_hover_color=WHITE,
            progress_color=MOSS_GREEN,
            text='Symbols',
            text_color=WHITE,
            font=CTkFont(family=FONT, size=TITLES_TEXT_SIZE),
            fg_color=LIGHT_GRAY,
            variable=sym_bool
        )
        sym_switch.pack(side='left', padx=5)


class ResultField(CTkEntry):
    def __init__(self, parent):
        font = CTkFont(family=FONT, size=TITLES_TEXT_SIZE, weight='bold')
        super().__init__(master=parent, state='readonly', font=font, text_color=BLACK, border_color=FOREST_GREEN, fg_color=WHITE)
        self.grid(column=0, row=7, sticky='nsew', padx=12)

    def set_password(self, password):
        # Temporarily set state to 'normal' to insert the password
        self.configure(state='normal')
        self.delete(0, 'end')  # Clear any existing text
        self.insert(0, password)  # Insert the generated password
        # Set the state back to 'readonly' to prevent editing
        self.configure(state='readonly')


class CopyButton(CTkButton):
    def __init__(self, parent, copy_action):
        # Create a font object
        font = CTkFont(family=FONT, size=TITLES_TEXT_SIZE, weight='bold')
        # Initialize the button with given parameters
        super().__init__(
            master=parent,
            text="Copy Password",
            font=font,
            text_color=WHITE,
            hover_color=MOSS_GREEN,
            fg_color=MOSS_GREEN,
            command=self.on_click  # Set the button's command to on_click method
        )
        self.grid(column=0, row=8, sticky='nsew', padx=12, pady=2)
        self.copy_action = copy_action  # Store the copy action callback

    def on_click(self):
        # Call the copy action function passed during initialization
        self.copy_action()


App()
