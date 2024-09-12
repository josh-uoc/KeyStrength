import math
import json

import tkinter as tk
from tkinter import font as tkfont
import ttkbootstrap as tkb
from ttkbootstrap import Style
from ttkbootstrap.widgets import Meter
from PIL import Image
Image.CUBIC = Image.BICUBIC



###################
### KEYSTRENGTH ### 
###################



### CLI FIRST RUN ###


# Test loop
def console_check():

    print("\n\n### KeyStrength Password Checker ###")

    while True:
        
        # Prompt for password
        pw = input("\nType a password: ")
        length = len(pw)
        
        # Check if password empty
        if pw == "":
            print("Password cannot be empty.\n")
            continue
        
        # Length check
        if length < 8:
            print("Password is very weak.\nPassword needs more characters.\n")
        elif length < 12:
            print("Password is weak.\nPassword needs more characters.\n")
        elif length < 16:
            print("Password is moderate.\nTo strengthen, try using a password more than 15 characters in length.\n")
        else:
            print("Password is strong.\nWell done!\n")

        # Continue?
        yn = input("Try another password? (Y/N): ")
        if yn.upper() == "Y":
            continue
        else:
            break

    print("\nThanks for using KeyStrength!")
#console_check()



### PASSWORD CHECK FUNCTIONALITY ###

class Password():
    def __init__(self, password):
        self.password = password
        self.score = 0



    ### CHECKS ###

    # Length check (WORKING)
    def length_check(self):
        length = len(self.password)
        if length < 9:
            return -5
        elif length < 11:
            return 5
        elif length < 13:
            return 8
        elif length < 15:
            return 12
        elif length < 17:
            return 15
        elif length < 19:
            return 20
        elif length < 22:
            return 25
        elif length < 24:
            return 30
        elif length < 28:
            return 35
        else:
            return 40
    
    # Diversity check (WORKING)
    def diversity_check(self):
        
        categories = 0
        score = 0

        if any(c.islower() for c in self.password):
            categories += 1
        if any(c.isupper() for c in self.password):
            categories += 1
        if any(c.isdigit() for c in self.password):
            categories += 1
        if any(c in '''!@#$%^&*()-_=+{}[];:"\'<>,.?/''' for c in self.password):
            categories += 1

        score = categories * 3
        if categories == 4:
            score += 15

        return score
    
    # Common passwords (WORKING)
    def common_passwords_check(self):
        if len (self.password) >= 25:
            return 5
        if len (self.password) >= 20:
            return 3
        else:
            with open ("data/passwords.json", "r") as file:
                common_passwords = json.load(file)

            password_lower = self.password.lower()

            if any(word.lower() in password_lower for word in common_passwords):
                return -10
            else:
                return 10
    
    # Personal info (names, movies, etc) (WORKING)
    def common_names_check(self):
        if len (self.password) >= 15:
            return 5
        else:
            with open("data/names.json", "r") as file:
                common_names = json.load(file)
            
            password_lower = self.password.lower()
            
            if any(name.lower() in password_lower for name in common_names):
                return -5
            else:
                return 5

    # Dictionary words (WORKING)
    def dictionary_words_check(self):
        if len (self.password) >= 15:
            return 5
        else:
            with open("data/dictionarywords.json", "r") as file:
                common_words = json.load(file)

            longer_words = [word for word in common_words if len(word) >= 3]
            
            if any(word in self.password for word in longer_words):
                return -5
            else:
                return 5

    # Repeated characters (WORKING)
    def repeat_check(self):
        
        password_lower = self.password.lower()
        common = [
        # Alphabetic
        "abc", "bcd", "cde", "def", "efg", "fgh", "ghi", "hij",
        "ijk", "jkl", "klm", "lmn", "mno", "nop", "opq", "pqr",
        "qrs", "rst", "stu", "tuv", "uvw", "vwx", "wxy", "xyz",
        # Reverse
        "zyx", "yxw", "xwv", "wvu", "vut", "uts",
        # Numeric
        "123", "234", "345", "456", "567", "678", "789", "890",
        # Reverse numeric
        "987", "876", "765", "654", "543", "432", "321",
        # Keyboard patterns
        "qwe", "wer", "ert", "rty", "tyu", "yui", "uio", "iop",
        "asd", "sdf", "dfg", "fgh", "ghj", "hjk", "jkl",
        "zxc", "xcv", "cvb", "vbn", "bnm",
        # Keyboard patterns (AZERTY)
        "aze", "zer", "ert", "rty", "tyu", "yui", "uio", "iop",
        "qsd", "sdf", "dfg", "fgh", "ghj", "hjk", "jkl", "lm",
        "wxc", "xcv", "cvb", "vbn",
        # Common substitutions
        "!@#", "@#$", "#$%", "$%^", "%^&", "^&*", "&*(", "*()"]

        if any(password_lower.count(c) > 2 for c in set(password_lower)):
            return -3
        elif any(seq in password_lower for seq in common):
            return -3
        else:
            return 8
        
    # Entropy (randomness) (AI MADE THIS FUNCTION - TEST)
    def entropy_check(self):
        char_set = set(self.password)
        entropy = len(self.password) * math.log2(len(char_set))

        if entropy < 45:
            return 0
        elif entropy < 55:
            return 8
        elif entropy < 70:
            return 15
        elif entropy < 85:
            return 22
        elif entropy < 105:
            return 28
        else:
            return 35



    ### FINAL STRENGTH ###

    # Strength
    def strength(self):
        self.score = (
            self.length_check() +
            self.diversity_check() +
            self.common_passwords_check() +
            self.common_names_check() +
            self.dictionary_words_check() +
            self.repeat_check() +
            self.entropy_check() 
        )
        if self.score >= 50:
            self.score += 5
        if len(self.password) > 30:
            self.score += 5
        return max(0, min(100, self.score))    # 0-100



        
### GUI ###

# Main
if __name__ == "__main__":
    root = tk.Tk()
    root.title("KeyStrength")

    # Window styling
    root.geometry("850x450")
    root.resizable(False, False)

    # Styling
    bg_colour = "#f3f3f3"
    fg_colour = "#191919"
    accent_colour = "#f3f3f3"
    entry_bg_colour = "#ffffff"
    button_colour = "#0f6aff"
    button_hover_colour = "#0c55cc"

    title_font = tkfont.Font(family="Gadugi", size=30, weight="bold")
    subtitle_font = tkfont.Font(family="Gadugi", size=13)
    main_font = tkfont.Font(family="Gadugi", size=12)
    result_font = tkfont.Font(family="Gadugi", size=16)
    
    style = tkb.Style()
    style.theme_use("cosmo")
    style.configure("TFrame", background=bg_colour)
    style.configure("TLabel", background=bg_colour, foreground=fg_colour, font=main_font)
    style.configure("TEntry", fieldbackground=entry_bg_colour, foreground=fg_colour, font=main_font, relief="ridge")
    style.configure("TButton", background=button_colour, foreground=accent_colour, font=main_font)
    style.map("TButton", background=[('active', button_hover_colour)])
                      
    # Configure main frame
    frame = tkb.Frame(root, padding="10")
    frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
    frame.configure(border=0, relief="flat")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Header
    header_label = tkb.Label(frame, text="KeyStrength", font=title_font)
    subtitle_label = tkb.Label(frame, text="Assess the strength of your passwords at the click of a button.", font=subtitle_font, foreground="#494949")
    header_label.grid(column=0, row=0, sticky=(tk.W), padx=38, pady=5)    # Logo here? (Made space to left of header)
    subtitle_label.grid(column=0, row=1, sticky=(tk.W), padx=39)

    # Password input
    input_frame = tkb.Frame(frame)
    input_frame.grid(column=0, row=2, columnspan=3, pady=(0, 20), sticky=(tk.E, tk.W))
    password_entry = tkb.Entry(input_frame, justify="left", font=main_font, width=55)
    password_entry.grid(row=0, column=1, sticky=(tk.W), padx=40, pady=20)
    password_entry.configure(takefocus=1)
    password_entry.focus_set()

    # Check strength button
    check_strength = tkb.Button(frame, text="Check", width=10)
    check_strength.grid(column=0, row=2, pady=(65, 0), padx=40, sticky=(tk.W))

    # Strength meter
    meter = tkb.Meter(frame, 
                      subtext="Strength", 
                      interactive=False, 
                      metertype="semi", 
                      stripethickness=10, 
                      bootstyle="success",    # <25="danger", <75="warning", 76-100="success"
                      amountused=95,)
    meter.grid(column=1, row=0, rowspan=3, padx=(50, 10), pady=20, sticky=(tk.S, tk.E))

    # Feedback area
    feedback_frame = tkb.Frame(frame, borderwidth=2, relief="solid", padding="60")
    feedback_frame.grid(column=0, row=4, columnspan=4, pady=10, padx=39, sticky=(tk.W, tk.E, tk.N, tk.S))
    feedback = tkb.Label(feedback_frame, font=main_font)
    feedback.grid(row=3, column=0, columnspan=4)

    # Layout
    root.columnconfigure(1, weight=1)

    # Event loop
    root.configure(bg=bg_colour)
    root.mainloop()








