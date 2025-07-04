import customtkinter
from tkinter import messagebox
from db_connection import get_connection
import datetime

class NurseFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # Layout: Sidebar and Main Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = customtkinter.CTkFrame(self, width=180, fg_color="#2e3f4f")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        customtkinter.CTkLabel(self.sidebar, text="Nurse", font=("Arial", 18, "bold"), fg_color="#2e3f4f", text_color="white").pack(pady=(30, 20))
        customtkinter.CTkButton(self.sidebar, text="Dashboard Home", command=self.show_welcome).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="Record Vitals", command=self.show_record_vitals).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="View Patient Vitals", command=self.show_view_vitals).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="Logout", command=self.logout).pack(side="bottom", fill="x", padx=20, pady=20)

        # Main content area
        self.content = customtkinter.CTkFrame(self, fg_color="white")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.show_welcome()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text=f"Welcome, Nurse {self.username}!", font=("Arial", 22, "bold")).pack(pady=40)
        customtkinter.CTkLabel(self.content, text="Use the sidebar to record or view patient vitals.", font=("Arial", 14)).pack(pady=10)

    def show_record_vitals(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Record Patient Vitals", font=("Arial", 18, "bold")).pack(pady=10)
        # Get all patients
        self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
        patients = self.cursor.fetchall()
        if not patients:
            customtkinter.CTkLabel(self.content, text="No patients found.").pack()
            return
        patient_combo = customtkinter.CTkComboBox(self.content, values=[f"{p[0]} - {p[1]}" for p in patients])
        patient_combo.pack(pady=5)
        bp_entry = customtkinter.CTkEntry(self.content, placeholder_text="Blood Pressure (e.g. 120/80)")
        bp_entry.pack(pady=5)
        temp_entry = customtkinter.CTkEntry(self.content, placeholder_text="Temperature (°C)")
        temp_entry.pack(pady=5)
        weight_entry = customtkinter.CTkEntry(self.content, placeholder_text="Weight (kg)")
        weight_entry.pack(pady=5)

        def submit():
            selection = patient_combo.get()
            if not selection:
                messagebox.showerror("Error", "Please select a patient.")
                return
            pid = selection.split(" - ")[0].strip()
            try:
                pid = int(pid)
            except ValueError:
                messagebox.showerror("Error", "Invalid patient ID selected.")
                return
            bp = bp_entry.get().strip()
            temp = temp_entry.get().strip()
            weight = weight_entry.get().strip()
            if not (bp and temp and weight):
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                temp_val = float(temp)
                weight_val = float(weight)
            except ValueError:
                messagebox.showerror("Error", "Temperature and Weight must be numbers.")
                return
            # Check patient exists
            self.cursor.execute("SELECT 1 FROM patients WHERE patient_id=%s", (pid,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "Selected patient does not exist in the database.")
                return
            try:
                self.cursor.execute(
                    "INSERT INTO treatments (patient_id, blood_pressure, temperature, weight) VALUES (%s, %s, %s, %s)",
                    (pid, bp, temp_val, weight_val)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Vitals recorded successfully.")
                bp_entry.delete(0, 'end')
                temp_entry.delete(0, 'end')
                weight_entry.delete(0, 'end')
            except Exception as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        customtkinter.CTkButton(self.content, text="Record Vitals", command=submit).pack(pady=10)

    def show_view_vitals(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Patient Vitals History", font=("Arial", 18, "bold")).pack(pady=10)
        # Get all patients
        self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
        patients = self.cursor.fetchall()
        if not patients:
            customtkinter.CTkLabel(self.content, text="No patients found.").pack()
            return
        patient_combo = customtkinter.CTkComboBox(self.content, values=[f"{p[0]} - {p[1]}" for p in patients])
        patient_combo.pack(pady=5)
        vitals_frame = customtkinter.CTkFrame(self.content, fg_color="white")
        vitals_frame.pack(fill="x", padx=10, pady=10)

        def on_select(event=None):
            for widget in vitals_frame.winfo_children():
                widget.destroy()
            selection = patient_combo.get()
            if not selection:
                return
            pid = selection.split(" - ")[0]
            self.cursor.execute(
                "SELECT blood_pressure, temperature, weight, date FROM treatments WHERE patient_id=%s AND (blood_pressure IS NOT NULL OR temperature IS NOT NULL OR weight IS NOT NULL) ORDER BY date DESC",
                (pid,)
            )
            vitals = self.cursor.fetchall()
            if not vitals:
                customtkinter.CTkLabel(vitals_frame, text="No vitals recorded yet.").pack()
            else:
                for v in vitals:
                    customtkinter.CTkLabel(
                        vitals_frame,
                        text=f"BP: {v[0]}, Temp: {v[1]}°C, Weight: {v[2]}kg (at {v[3]})"
                    ).pack(anchor="w", padx=20)

        patient_combo.bind("<<ComboboxSelected>>", on_select)
        # Optionally, show first patient's vitals by default
        if patients:
            patient_combo.set(f"{patients[0][0]} - {patients[0][1]}")
            on_select()

    def logout(self):
        self.conn.close()
        self.master.destroy()