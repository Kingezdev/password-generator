import tkinter
import string
import random
from tkinter import filedialog

class Window():

    MAX_CHARS = 15
    MIN_CHARS = 3
    CHARS_OPTIONS = ["Alphanumeric", 
                    "Numeric", 
                    "Alpha",
                    "Alphanumeric with Special"]
    GRID_PADY = (10, 10)

    def __init__(self):
        self.initUI()

    def initUI(self):

        # Construction of the root element
        self.master = tkinter.Tk()
        self.master.title("Password Generator")
        self.master.geometry("600x350")
        
        self.ptype = tkinter.StringVar(self.master, 
                                    value=Window.CHARS_OPTIONS[0])
        self.n_chars = tkinter.IntVar(self.master, 
                                    value=Window.MIN_CHARS)
        
        self.label_chars = tkinter.Label(self.master, 
                text="Character Type: ")
        self.option_menu_chars = tkinter.OptionMenu(self.master, self.ptype ,*Window.CHARS_OPTIONS)
        
        self.frame_n_chars = tkinter.Frame(self.master) 
        self.label_num_chars = tkinter.Label(self.master, text="Password Length:")
        self.option_menu_n_chars = tkinter.OptionMenu(self.master, self.n_chars, *range(Window.MIN_CHARS, Window.MAX_CHARS+1))
        
        # Grid positioning for password type and length
        self.label_chars.grid(row=0, column=0, padx=10, pady=Window.GRID_PADY, sticky="W")
        self.option_menu_chars.grid(row=0, column=1, padx=10, pady=Window.GRID_PADY, sticky="W")
        self.label_num_chars.grid(row=0, column=2, padx=10, pady=Window.GRID_PADY, sticky="W" )
        self.option_menu_n_chars.grid(row=0, column=3, padx=10, pady=Window.GRID_PADY, sticky="W",)

        #password output object
        self.text_password_out = tkinter.Text(self.master, border=2, height=2, width=40)
        

        # Grid positioning for password output
        self.text_password_out.grid(row=1, column=0, columnspan=4, padx=10, pady=Window.GRID_PADY, sticky="W",)

        # Grid positioning for password strength
        self.label_strength = tkinter.Label(self.master, text="Password Strength: Weak")
        self.label_strength.grid(row=2, columnspan=4, padx=10, pady=Window.GRID_PADY, sticky="W",)

        self.frame_buttons = tkinter.Frame()
        self.button_generate = tkinter.Button(self.frame_buttons, text="Generate", width=8, command=lambda: self.set_password())
        self.button_close = tkinter.Button(self.frame_buttons, text="Close", command=self.master.quit, width=8)
        self.button_copy = tkinter.Button(self.frame_buttons, text="Copy", width=8, command=self.copy_to_clipboard)
        self.button_save = tkinter.Button(self.frame_buttons, text="Save", width=8, command=self.save_to_file)

        #Grid positioning for save,close,generate, and copy buttons 
        self.frame_buttons.grid(row=3, column=0, columnspan=4, padx=10, pady=Window.GRID_PADY, sticky="W",)
        
         
        self.button_generate.pack(side=tkinter.LEFT, padx=5)
        self.button_copy.pack(side=tkinter.LEFT, padx=5)
        self.button_save.pack(side=tkinter.LEFT, padx=5)
        self.button_close.pack(side=tkinter.LEFT, pady=Window.GRID_PADY, padx=5)
        self.frame_buttons.grid(row=3, column=1, columnspan=2)

        
        self.master.mainloop()

    def set_password(self):
        chars = ""
        ptype = self.ptype.get().lower()
        if ptype == "numeric":
            chars = string.digits
        elif ptype == "alpha":
            chars = string.ascii_letters
        elif ptype == "alphanumeric with special":
            chars = string.digits + string.ascii_letters + string.punctuation
        else:
            chars = string.digits + string.ascii_letters   

        password = "".join(random.choices(chars, k=self.n_chars.get()))
        
        self.text_password_out.delete("1.0", tkinter.END)
        self.text_password_out.insert("1.0", password)
        
        self.update_strength(password)

    def update_strength(self, password):
        length = len(password)
        has_digits = any(char.isdigit() for char in password)
        has_letters = any(char.isalpha() for char in password)
        has_special = any(char in string.punctuation for char in password)

        # Determine strength based on length and character diversity
        if length >= 12 and has_digits and has_letters and has_special:
            strength = "Strong"
        elif length >= 8 and has_digits and has_letters:
            strength = "Medium"
        else:
            strength = "Weak"
        
        self.label_strength.config(text=f"Password Strength: {strength}")
    
    def copy_to_clipboard(self):
        password = self.text_password_out.get("1.0", tkinter.END).strip()
        self.master.clipboard_clear()
        self.master.clipboard_append(password)
        self.master.update()  # Keeps the clipboard content after the window is closed

    def save_to_file(self):
        password = self.text_password_out.get("1.0", tkinter.END).strip()
        if password:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                     filetypes=[("Text files", "*.txt")],
                                                     title="Save Password")
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(f"Generated Password: {password}\n")
                tkinter.messagebox.showinfo("Saved", "Password saved successfully!")
        else:
            tkinter.messagebox.showwarning("No Password", "Generate a password first before saving!")

if __name__=="__main__":
    Window()
