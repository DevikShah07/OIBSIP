import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS bmi_records
          (id INTEGER PRIMARY KEY, user TEXT, weight REAL, height REAL, bmi REAL, date TEXT)
          ''')
conn.commit()

# BMI categories
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# Save BMI data
def save_bmi(user, weight, height, bmi):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        c.execute("INSERT INTO bmi_records (user, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                  (user, weight, height, bmi, date))

# Fetch historical data
def fetch_bmi_data(user):
    c.execute("SELECT * FROM bmi_records WHERE user = ?", (user,))
    return c.fetchall()

# Plot BMI data
def plot_bmi_data(user):
    records = fetch_bmi_data(user)
    if not records:
        messagebox.showinfo("No Data", "No historical data found for this user.")
        return
    
    dates = [record[5] for record in records]
    bmis = [record[4] for record in records]
    
    plt.plot(dates, bmis, marker='o')
    plt.title(f'BMI Trend for {user}')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# GUI setup
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        
        self.user_label = tk.Label(root, text="User:")
        self.user_label.grid(row=0, column=0)
        self.user_entry = tk.Entry(root)
        self.user_entry.grid(row=0, column=1)
        
        self.weight_label = tk.Label(root, text="Weight (kg):")
        self.weight_label.grid(row=1, column=0)
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=1, column=1)
        
        self.height_label = tk.Label(root, text="Height (m):")
        self.height_label.grid(row=2, column=0)
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=2, column=1)
        
        self.calculate_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=3, column=0, columnspan=2)
        
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2)
        
        self.history_button = tk.Button(root, text="View History", command=self.view_history)
        self.history_button.grid(row=5, column=0, columnspan=2)

    def calculate_bmi(self):
        try:
            user = self.user_entry.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = calculate_bmi(weight, height)
            category = categorize_bmi(bmi)
            self.result_label.config(text=f"BMI: {bmi} ({category})")
            save_bmi(user, weight, height, bmi)
            messagebox.showinfo("Success", "BMI calculated and saved successfully.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and height.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_history(self):
        user = self.user_entry.get()
        if not user:
            messagebox.showerror("Invalid Input", "Please enter a user name.")
            return
        plot_bmi_data(user)

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
