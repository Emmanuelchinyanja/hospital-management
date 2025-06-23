import customtkinter
from tkinter import messagebox
import mysql.connector

class App(customtkinter.CTk):
    def __init__(self, username="User", role="User"):
        super().__init__()
        self.title("Hospital Management Dashboard")
        self.geometry("900x600")
        self.username = username
        self.role = role

        # Connect to MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hospital-management"
        )
        self.cursor = self.conn.cursor()

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Navigation
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        # Show menu based on role
        if self.role == "Receptionist":
            self.add_nav_button("Register Patient", self.show_register_patient, 0)
            self.add_nav_button("View Patients", self.show_view_patients, 1)
        elif self.role == "Nurse":
            self.add_nav_button("Record Vital Signs", self.show_record_vitals, 0)
        elif self.role == "Doctor":
            self.add_nav_button("Consult Patient", self.show_consult_patient, 0)
            self.add_nav_button("Set Disposition", self.show_set_disposition, 1)
        elif self.role == "Admin":
            self.add_nav_button("View Audit", self.show_view_audit, 0)

        self.add_nav_button("Logout", self.logout, 5)

        # Main content frame
        self.content_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="white")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.current_content = None

        self.show_welcome()

    def add_nav_button(self, text, command, row):
        btn = customtkinter.CTkButton(self.navigation_frame, text=text, command=command)
        btn.grid(row=row, column=0, padx=10, pady=10, sticky="ew")

    def clear_content(self):
        if self.current_content:
            self.current_content.destroy()
        self.current_content = customtkinter.CTkFrame(self.content_frame, fg_color="white")
        self.current_content.pack(fill="both", expand=True)

    def show_welcome(self):
        self.clear_content()
        label = customtkinter.CTkLabel(self.current_content, text=f"Welcome, {self.role} {self.username}!", font=("Arial", 24))
        label.pack(pady=40)

    # Receptionist: Register Patient
    def show_register_patient(self):
        self.clear_content()
        label = customtkinter.CTkLabel(self.current_content, text="Register Patient", font=("Arial", 18))
        label.pack(pady=10)
        pid_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Patient ID")
        pid_entry.pack(pady=5)
        name_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Name")
        name_entry.pack(pady=5)
        age_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Age")
        age_entry.pack(pady=5)
        gender_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Gender (male/female)")
        gender_entry.pack(pady=5)

        def submit():
            pid = pid_entry.get().strip()
            name = name_entry.get().strip()
            age = age_entry.get().strip()
            gender = gender_entry.get().strip().lower()
            if not (pid and name and age and gender):
                messagebox.showerror("Error", "All fields are required.")
                return
            if gender not in ("male", "female"):
                messagebox.showerror("Error", "Gender must be 'male' or 'female'.")
                return
            try:
                age = int(age)
            except ValueError:
                messagebox.showerror("Error", "Age must be a number.")
                return
            try:
                self.cursor.execute(
                    "INSERT INTO patients (patient_id, name, age, gender) VALUES (%s, %s, %s, %s)",
                    (pid, name, age, gender)
                )
                self.conn.commit()
                messagebox.showinfo("Success", f"Patient {name} registered.")
                # Optionally clear fields after success
                pid_entry.delete(0, 'end')
                name_entry.delete(0, 'end')
                age_entry.delete(0, 'end')
                gender_entry.delete(0, 'end')
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    messagebox.showerror("Error", "Patient ID already exists.")
                else:
                    messagebox.showerror("Database Error", f"Error: {err}")

        submit_btn = customtkinter.CTkButton(self.current_content, text="Register", command=submit)
        submit_btn.pack(pady=10)

    # Receptionist: View Patients
    def show_view_patients(self):
        self.clear_content()
        label = customtkinter.CTkLabel(self.current_content, text="Patients List", font=("Arial", 18))
        label.pack(pady=10)
        try:
            self.cursor.execute("SELECT patient_id, name, age, gender, date_registered FROM patients")
            patients = self.cursor.fetchall()
            if not patients:
                customtkinter.CTkLabel(self.current_content, text="No patient records found.").pack()
            else:
                for p in patients:
                    customtkinter.CTkLabel(
                        self.current_content,
                        text=f"ID: {p[0]}, Name: {p[1]}, Age: {p[2]}, Gender: {p[3]}, Registered: {p[4]}"
                    ).pack(anchor="w", padx=20)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Nurse: Record Vital Signs
    def show_record_vitals(self):
        self.clear_content()
        label = customtkinter.CTkLabel(self.current_content, text="Record Vital Signs", font=("Arial", 18))
        label.pack(pady=10)
        pid_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Patient ID")
        pid_entry.pack(pady=5)
        bp_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Blood Pressure")
        bp_entry.pack(pady=5)
        pulse_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Pulse Rate")
        pulse_entry.pack(pady=5)
        resp_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Respiratory Rate")
        resp_entry.pack(pady=5)
        oxygen_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Oxygen Saturation")
        oxygen_entry.pack(pady=5)

        def submit():
            pid = pid_entry.get()
            bp = bp_entry.get()
            pulse = pulse_entry.get()
            resp = resp_entry.get()
            oxygen = oxygen_entry.get()
            if not (pid and bp and pulse and resp and oxygen):
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                details = f"BP: {bp}, Pulse: {pulse}, Resp: {resp}, Oxygen: {oxygen}"
                self.cursor.execute(
                    "INSERT INTO treatments (patient_id, details) VALUES (%s, %s)",
                    (pid, details)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Vital signs recorded.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        submit_btn = customtkinter.CTkButton(self.current_content, text="Record", command=submit)
        submit_btn.pack(pady=10)

    # Doctor: Consult Patient
    def show_consult_patient(self):
        self.clear_content()
        label = customtkinter.CTkLabel(self.current_content, text="Consult Patient", font=("Arial", 18))
        label.pack(pady=10)
        pid_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Patient ID")
        pid_entry.pack(pady=5)
        symptoms_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Symptoms")
        symptoms_entry.pack(pady=5)
        treatment_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Treatment")
        treatment_entry.pack(pady=5)

        def submit():
            pid = pid_entry.get()
            symptoms = symptoms_entry.get()
            treatment = treatment_entry.get()
            if not (pid and symptoms and treatment):
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                details = f"Symptoms: {symptoms}, Treatment: {treatment}"
                self.cursor.execute(
                    "INSERT INTO treatments (patient_id, details) VALUES (%s, %s)",
                    (pid, details)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Consultation saved.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        submit_btn = customtkinter.CTkButton(self.current_content, text="Save", command=submit)
        submit_btn.pack(pady=10)

    # Doctor: Set Disposition
    def show_set_disposition(self):
        self.clear_content()
        label = customtkinter.CTkLabel(self.current_content, text="Set Disposition", font=("Arial", 18))
        label.pack(pady=10)
        pid_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Patient ID")
        pid_entry.pack(pady=5)
        disposition_entry = customtkinter.CTkEntry(self.current_content, placeholder_text="Disposition (Discharged, Admitted, etc.)")
        disposition_entry.pack(pady=5)

        def submit():
            pid = pid_entry.get()
            disposition = disposition_entry.get()
            if not (pid and disposition):
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                details = f"Disposition: {disposition}"
                self.cursor.execute(
                    "INSERT INTO treatments (patient_id, details) VALUES (%s, %s)",
                    (pid, details)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Disposition recorded.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        submit_btn = customtkinter.CTkButton(self.current_content, text="Set", command=submit)
        submit_btn.pack(pady=10)

    # Admin: View Audit (all patients and treatments)
    def show_view_audit(self):
        self.clear_content()
        label = customtkinter.CTkLabel(self.current_content, text="Audit Display", font=("Arial", 18))
        label.pack(pady=10)
        try:
            self.cursor.execute("SELECT patient_id, name, age, gender, date_registered FROM patients")
            patients = self.cursor.fetchall()
            if not patients:
                customtkinter.CTkLabel(self.current_content, text="No patients found.").pack()
            else:
                for p in patients:
                    customtkinter.CTkLabel(
                        self.current_content,
                        text=f"ID: {p[0]}, Name: {p[1]}, Age: {p[2]}, Gender: {p[3]}, Registered: {p[4]}"
                    ).pack(anchor="w", padx=20)
                    # Show treatments for each patient
                    self.cursor.execute("SELECT details, created_at FROM treatments WHERE patient_id=%s", (p[0],))
                    treatments = self.cursor.fetchall()
                    for t in treatments:
                        customtkinter.CTkLabel(
                            self.current_content,
                            text=f"    {t[1]} - {t[0]}"
                        ).pack(anchor="w", padx=40)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def logout(self):
        self.cursor.close()
        self.conn.close()
        self.destroy()

if __name__ == "__main__":
    app = App("receptionist", "Receptionist")
    app.mainloop()