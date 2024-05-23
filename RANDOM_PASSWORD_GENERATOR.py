import tkinter as tk
import random
import string
import pyperclip

class PasswordCreator:
    def __init__(self, master):
        # Initialize the Tkinter window
        self.master = master
        self.master.title("Password Creator")
        self.master.geometry("400x300")
        
        # Create labels, entry fields, checkboxes, buttons, and a label for displaying password
        self.length_label = tk.Label(master, text="Password Length:")
        self.length_label.pack()
        self.length_entry = tk.Entry(master)
        self.length_entry.pack()
        
        # Define a dictionary to store the character sets
        self.char_sets = {
            "Capital Letters": string.ascii_uppercase,
            "Lowercase Letters": string.ascii_lowercase,
            "Numbers": string.digits,
            "Special Characters": string.punctuation
        }
        
        # Create a dictionary to store the checkbox variables
        self.checkbox_vars = {}
        for i, (text, chars) in enumerate(self.char_sets.items()):
            # Create a checkbox variable
            var = tk.IntVar()
            # Create a checkbox with the corresponding text and variable
            checkbox = tk.Checkbutton(master, text=text, variable=var)
            checkbox.pack()
            # Store the checkbox variable in the dictionary
            self.checkbox_vars[text] = var
        
        # Create a button to generate the password
        self.generate_button = tk.Button(master, text="Create Password", command=self.generate_password)
        self.generate_button.pack()
        
        # Create a label to display the generated password
        self.password_label = tk.Label(master, text="")
        self.password_label.pack()
        
        # Create a button to copy the password to the clipboard
        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack()
    
    def generate_password(self):
        # Get the desired password length from the entry field
        length = int(self.length_entry.get())
        # Initialize an empty string for the password
        password_chars = ""
        
        # Iterate over the checkbox variables and add the corresponding character sets to the password
        for text, var in self.checkbox_vars.items():
            if var.get():
                password_chars += self.char_sets[text]
        
        # If no checkboxes are selected, include all character sets
        if not password_chars:
            password_chars = string.ascii_letters + string.digits + string.punctuation
        
        # Generate the password by selecting random characters from the selected sets
        password = ''.join(random.choices(password_chars, k=length))
        # Shuffle the characters in the password for better security
        password_list = list(password)
        random.shuffle(password_list)
        password = ''.join(password_list)
        
        # Display the generated password in the label
        self.password_label.config(text=password)
    
    def copy_to_clipboard(self):
        # Get the password displayed in the label
        password = self.password_label.cget("text")
        # Copy the password to the clipboard
        pyperclip.copy(password)
        # Update the label to indicate successful copying
        self.password_label.config(text="Copied to Clipboard!")

if __name__ == "__main__":
    # Create a Tkinter root window
    root = tk.Tk()
    # Create an instance of the PasswordCreator class
    app = PasswordCreator(root)
    # Start the Tkinter event loop
    root.mainloop()
