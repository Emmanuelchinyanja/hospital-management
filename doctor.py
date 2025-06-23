import customtkinter
from tkinter import messagebox
from db_connection import get_connection
import datetime

class DoctorFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        label = customtkinter.CTkLabel(self, text=f"Doctor Dashboard - {self.username}", font=("Arial", 20))
        label.pack(pady=20)

        # Example: Today's Patients Button
        btn = customtkinter.CTkButton(self, text="Today's Patients", command=self.show_todays_patients)
        btn.pack(pady=10)

        self.result_frame = customtkinter.CTkFrame(self)
        self.result_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def show_todays_patients(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        today = datetime.date.today()
        try:
            self.cursor.execute(
                "SELECT DISTINCT patient_id FROM treatments WHERE doctor=%s AND DATE(created_at)=%s",
                (self.username, today)
            )
            patients = self.cursor.fetchall()
            count = len(patients)
            customtkinter.CTkLabel(self.result_frame, text=f"Total patients treated today: {count}", font=("Arial", 14)).pack(pady=5)
            if not patients:
                customtkinter.CTkLabel(self.result_frame, text="No patients treated today.").pack()
            else:
                for p in patients:
                    self.cursor.execute("SELECT name FROM patients WHERE patient_id=%s", (p[0],))
                    patient_name = self.cursor.fetchone()
                    name_str = patient_name[0] if patient_name else "Unknown"
                    customtkinter.CTkLabel(
                        self.result_frame,
                        text=f"Patient ID: {p[0]}, Name: {name_str}"
                    ).pack(anchor="w", padx=20)
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")