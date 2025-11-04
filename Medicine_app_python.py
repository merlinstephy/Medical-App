import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd


try:
    info_df = pd.read_excel("medicinedataset.xlsx") 
    risk_df = pd.read_excel("medicinedata.xlsx")     
except FileNotFoundError as e:
    messagebox.showerror("Error", f"Excel file not found: {e.filename}")
    exit()

# Medicine Information page
def open_medicine_info():
    info_window = tk.Toplevel(root)
    info_window.title("💊 Medicine Information")
    info_window.geometry("800x600")
    info_window.config(bg="light blue")

    tk.Label(info_window, text="💊 Medicine Information", font=("Arial", 18, "bold"),
             bg="light blue", fg="black").pack(pady=15)

    frame = tk.Frame(info_window, bg="light blue")
    frame.pack(pady=10)

    tk.Label(frame, text="Select Medicine:", bg="light blue", fg="black", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    medicine_var = tk.StringVar()
    medicine_dropdown = ttk.Combobox(frame, textvariable=medicine_var, values=list(info_df["Medicine_Name"]), width=40)
    medicine_dropdown.grid(row=0, column=1)

    info_frame = tk.LabelFrame(info_window, text="Medicine Information", font=("Arial", 12, "bold"), 
                               bg="light blue", fg="black", padx=10, pady=10)
    info_frame.pack(pady=15, fill="both", expand=True)

    info_text = tk.Text(info_frame, height=15, wrap="word", font=("Arial", 11), bg="light blue", fg="black")
    info_text.pack(fill="both", expand=True)

    def show_info():
        med = medicine_var.get()
        info_text.delete("1.0", tk.END)
        if not med:
            messagebox.showwarning("Warning", "Please select a medicine!")
            return
        filtered = info_df[info_df["Medicine_Name"] == med]
        if not filtered.empty:
            med_info = filtered.iloc[0]
            info_text.insert(tk.END, f" Medicine: {med_info['Medicine_Name']}\n\n")
            info_text.insert(tk.END, f" Uses: {med_info['Uses']}\n")
            info_text.insert(tk.END, f" Dosage: {med_info['Dosage']}\n\n")
            info_text.insert(tk.END, f" Composition:\n{med_info['Composition']}\n\n")
            info_text.insert(tk.END, f" Side Effects: {med_info['Side_Effects']}\n")
        else:
            info_text.insert(tk.END, "No information found for this medicine.")

    def clear_info():
        medicine_var.set('')
        info_text.delete("1.0", tk.END)

    # Buttons side by side and centered
    button_frame = tk.Frame(info_window, bg="light blue")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Show Information", font=("Arial", 12, "bold"),
              bg="light blue", fg="black", command=show_info).pack(side="left", padx=10)
    tk.Button(button_frame, text="Clear", font=("Arial", 12, "bold"),
              bg="light blue", fg="black", command=clear_info).pack(side="left", padx=10)


# Medicine Risk Detection page
def open_medicine_risk():
    risk_window = tk.Toplevel(root)
    risk_window.title("⚠️ Medicine Risk Detection")
    risk_window.geometry("800x600")
    risk_window.config(bg="light blue")

    tk.Label(risk_window, text="⚠️ Medicine Risk Detection", font=("Arial", 18, "bold"),
             bg="light blue", fg="black").pack(pady=15)

    frame = tk.Frame(risk_window, bg="light blue")
    frame.pack(pady=10)

    tk.Label(frame, text="Select Medicine:", bg="light blue", fg="black", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    medicine_var = tk.StringVar()
    medicine_dropdown = ttk.Combobox(frame, textvariable=medicine_var, values=list(risk_df["Medicine Name"].unique()), width=40)
    medicine_dropdown.grid(row=0, column=1)

    tk.Label(frame, text="Select Age Group:", bg="light blue", fg="black", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    age_var = tk.StringVar()
    age_dropdown = ttk.Combobox(frame, textvariable=age_var, values=list(risk_df["Age Group"].unique()), width=40)
    age_dropdown.grid(row=1, column=1)

    result_frame = tk.LabelFrame(risk_window, text="Risk Information", font=("Arial", 12, "bold"),
                                 bg="light blue", fg="black", padx=10, pady=10)
    result_frame.pack(pady=15, fill="both", expand=True)

    result_text = tk.Text(result_frame, height=15, wrap="word", font=("Arial", 11), bg="light blue", fg="black")
    result_text.pack(fill="both", expand=True)

    def show_info():
        med = medicine_var.get()
        age = age_var.get()
        result_text.delete("1.0", tk.END)
        if not med :
            messagebox.showwarning("Warning", "Please select Medicine!")
            return
        if not age:
            messagebox.showwarning("Warning", "Please select Age Group!")
            return
        filtered = risk_df[(risk_df["Medicine Name"] == med) & (risk_df["Age Group"] == age)]
        if not filtered.empty:
            med_info = filtered.iloc[0]
            result_text.insert(tk.END, f" Medicine: {med_info['Medicine Name']}\n")
            result_text.insert(tk.END, f" Age Group: {med_info['Age Group']}\n")
            result_text.insert(tk.END, f" Uses: {med_info['Uses']}\n")
            result_text.insert(tk.END, f" Dosage: {med_info['Dosage']}\n")
            result_text.insert(tk.END, f" Composition: {med_info['Composition']}\n")
            result_text.insert(tk.END, f" Side Effects: {med_info['Side Effects']}\n")
            result_text.insert(tk.END, f" Risk Level: {med_info['Risk Level']}\n")
            result_text.insert(tk.END, f" Risk Explanation: {med_info['Risk Explanation']}\n")
        else:
            result_text.insert(tk.END, "No risk information found for this selection.")

    def clear_risk():
        medicine_var.set('')
        age_var.set('')
        result_text.delete("1.0", tk.END)

    # Buttons side by side and centered
    button_frame = tk.Frame(risk_window, bg="light blue")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Show Information", font=("Arial", 12, "bold"),
              bg="light blue", fg="black", command=show_info).pack(side="left", padx=10)
    tk.Button(button_frame, text="Clear", font=("Arial", 12, "bold"),
              bg="light blue", fg="black", command=clear_risk).pack(side="left", padx=10)


# First page
root = tk.Tk()
root.title("💊 Medicine App")
root.geometry("400x300")
root.config(bg="#f0f4f7")

# Background image 
bg_img = Image.open("C:\\Users\\Dell\\OneDrive\\Documents\\pythonproject\\medicinebg.jpg")
bg_img = bg_img.resize((1400, 1400))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(root, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(root, text="💊 Welcome to Medicine App", font=("Arial", 18, "bold"), bg="#f0f4f7", fg="#2c3e50").pack(pady=30)

tk.Button(root, text="Medicine Information", font=("Arial", 14, "bold"), bg="#3498db", fg="white",
          width=20, command=open_medicine_info).pack(pady=20)

tk.Button(root, text="Medicine Risk Detection", font=("Arial", 14, "bold"), bg="#e67e22", fg="white",
          width=20, command=open_medicine_risk).pack(pady=20)

root.mainloop()
