import customtkinter
from tkinter import messagebox
from db_connection import get_connection
from db_connection import get_connection, log_action
import datetime

class DoctorFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = customtkinter.CTkFrame(self, width=180, fg_color="#2e3f4f")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        customtkinter.CTkLabel(self.sidebar, text="Doctor", font=("Arial", 18, "bold"),
                               fg_color="#2e3f4f", text_color="white").pack(pady=(30, 20))
        customtkinter.CTkButton(self.sidebar, text="Dashboard Home", command=self.show_welcome).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="View Patients", command=self.show_patients).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="Today's Patients", command=self.show_todays_patients).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="Logout", command=self.logout).pack(side="bottom", fill="x", padx=20, pady=20)

        self.content = customtkinter.CTkFrame(self, fg_color="white")
        self.content.grid(row=0, column=1, sticky="nsew")

        # Check if doctor exists, else show registration form
        self.check_and_register_doctor()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def check_and_register_doctor(self):
        self.cursor.execute("SELECT id FROM doctors WHERE firstname=%s", (self.username,))
        doctor_row = self.cursor.fetchone()
        if not doctor_row:
            self.show_register_doctor()
        else:
            self.doctor_id = doctor_row[0]
            self.show_welcome()

    def show_register_doctor(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Register Doctor Profile", font=("Arial", 20, "bold")).pack(pady=20)
        fname_entry = customtkinter.CTkEntry(self.content, placeholder_text="First Name")
        fname_entry.pack(pady=5)
        lname_entry = customtkinter.CTkEntry(self.content, placeholder_text="Last Name")
        lname_entry.pack(pady=5)
        natid_entry = customtkinter.CTkEntry(self.content, placeholder_text="National ID")
        natid_entry.pack(pady=5)
        qual_entry = customtkinter.CTkEntry(self.content, placeholder_text="Qualification")
        qual_entry.pack(pady=5)
        spec_combo = customtkinter.CTkComboBox(self.content, values=[
            'Surgeon', 'Optician', 'Psychian', 'Neurologuist', 'Medicine', 'Hematologist'
        ])
        spec_combo.pack(pady=5)
        spec_combo.set('Medicine')

        def register():
            fname = fname_entry.get().strip()
            lname = lname_entry.get().strip()
            natid = natid_entry.get().strip()
            qual = qual_entry.get().strip()
            spec = spec_combo.get().strip()
            if not (fname and lname and natid and qual and spec):
                messagebox.showerror("Error", "All fields are required.")
                return
            try:
                self.cursor.execute(
                    "INSERT INTO doctors (firstname, lastname, national_id, qualification, specialization) VALUES (%s, %s, %s, %s, %s)",
                    (fname, lname, natid, qual, spec)
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Doctor registered successfully!")
                self.username = fname  # Update username to match registration
                self.check_and_register_doctor()
            except Exception as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        customtkinter.CTkButton(self.content, text="Register", command=register).pack(pady=15)

    def show_welcome(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text=f"Welcome, Dr. {self.username}!", font=("Arial", 22, "bold")).pack(pady=40)
        customtkinter.CTkLabel(self.content, text="Use the sidebar to view and treat patients.", font=("Arial", 14)).pack(pady=10)

    def show_patients(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Current Patients", font=("Arial", 18, "bold")).pack(pady=10)
        try:
            self.cursor.execute("SELECT patient_id, name, date_of_birth, gender, blood_type FROM patients ORDER BY date_registered DESC")
            patients = self.cursor.fetchall()
            if not patients:
                customtkinter.CTkLabel(self.content, text="No patients found.").pack()
                return
            # Listbox for patients
            patient_listbox = customtkinter.CTkComboBox(self.content, values=[f"{p[0]} - {p[1]}" for p in patients])
            patient_listbox.pack(pady=10)
            details_frame = customtkinter.CTkFrame(self.content, fg_color="white")
            details_frame.pack(fill="x", padx=10, pady=10)

            def on_select(event=None):
                for widget in details_frame.winfo_children():
                    widget.destroy()
                selection = patient_listbox.get()
                if not selection:
                    return
                pid = selection.split(" - ")[0]
                # Show patient info
                self.cursor.execute("SELECT name, date_of_birth, gender, blood_type FROM patients WHERE patient_id=%s", (pid,))
                info = self.cursor.fetchone()
                if info:
                    customtkinter.CTkLabel(details_frame, text=f"Name: {info[0]}, DOB: {info[1]}, Gender: {info[2]}, Blood Type: {info[3]}", font=("Arial", 14)).pack(anchor="w", pady=2)
                # Show latest vitals (from treatments table, if any)
                self.cursor.execute(
                    "SELECT treatment_id, blood_pressure, temperature, weight, date, symptoms, treatment FROM treatments WHERE patient_id=%s ORDER BY date DESC LIMIT 1",
                    (pid,)
                )
                vitals = self.cursor.fetchone()
                if vitals and (vitals[1] or vitals[2] or vitals[3]):
                    customtkinter.CTkLabel(details_frame, text=f"Latest Vitals - BP: {vitals[1]}, Temp: {vitals[2]}, Weight: {vitals[3]} (at {vitals[4]})", font=("Arial", 13, "italic")).pack(anchor="w", pady=2)
                    # Show existing symptoms/treatment if any
                    if vitals[5] or vitals[6]:
                        customtkinter.CTkLabel(details_frame, text=f"Symptoms: {vitals[5] or 'N/A'}", font=("Arial", 13)).pack(anchor="w", pady=2)
                        customtkinter.CTkLabel(details_frame, text=f"Treatment: {vitals[6] or 'N/A'}", font=("Arial", 13)).pack(anchor="w", pady=2)
                else:
                    customtkinter.CTkLabel(details_frame, text="No vitals recorded yet.", font=("Arial", 13, "italic")).pack(anchor="w", pady=2)
                    return  # Don't allow adding symptoms/treatment if no vitals

                # Add symptoms and treatment form
                customtkinter.CTkLabel(details_frame, text="Add/Update Symptoms and Treatment", font=("Arial", 14, "bold")).pack(pady=(10, 2))
                symptoms_entry = customtkinter.CTkEntry(details_frame, placeholder_text="Symptoms")
                symptoms_entry.pack(pady=2, fill="x")
                treatment_entry = customtkinter.CTkEntry(details_frame, placeholder_text="Treatment")
                treatment_entry.pack(pady=2, fill="x")

                def save_treatment():
                    symptoms = symptoms_entry.get().strip()
                    treatment = treatment_entry.get().strip()
                    if not (symptoms and treatment):
                        messagebox.showerror("Error", "Please enter both symptoms and treatment.")
                        return
                    try:
                        # Get doctor_id from doctors table
                        self.cursor.execute("SELECT id FROM doctors WHERE firstname=%s", (self.username,))
                        doctor_row = self.cursor.fetchone()
                        if not doctor_row:
                            messagebox.showerror("Error", "Doctor not found in database. Please contact admin.")
                            return
                        doctor_id = doctor_row[0]
                        # Update the latest treatment row for this patient
                        self.cursor.execute(
                            "UPDATE treatments SET doctor_id=%s, symptoms=%s, treatment=%s WHERE treatment_id=%s",
                            (doctor_id, symptoms, treatment, vitals[0])
                        )
                        self.conn.commit()
                        messagebox.showinfo("Success", "Symptoms and treatment saved.")
                        symptoms_entry.delete(0, 'end')
                        treatment_entry.delete(0, 'end')
                        log_action(self.username, "Doctor", f"Updated symptoms/treatment for patient ID: {pid}")
                    except Exception as err:
                        messagebox.showerror("Database Error", f"Error: {err}")

                customtkinter.CTkButton(details_frame, text="Save", command=save_treatment).pack(pady=5)

                # Show patient history
                self.show_patient_history(pid, details_frame)
                # Add symptoms and treatment form for the latest record
                self.cursor.execute(
                    "SELECT treatment_id FROM treatments WHERE patient_id=%s ORDER BY date DESC LIMIT 1",
                    (pid,)
                )
                vitals = self.cursor.fetchone()
                if not vitals:
                    customtkinter.CTkLabel(details_frame, text="No vitals recorded yet.", font=("Arial", 13, "italic")).pack(anchor="w", pady=2)
                    return  # Don't allow adding symptoms/treatment if no vitals

                # Add symptoms and treatment form
                customtkinter.CTkLabel(details_frame, text="Add/Update Symptoms and Treatment", font=("Arial", 14, "bold")).pack(pady=(10, 2))
                symptoms_entry = customtkinter.CTkEntry(details_frame, placeholder_text="Symptoms")
                symptoms_entry.pack(pady=2, fill="x")
                treatment_entry = customtkinter.CTkEntry(details_frame, placeholder_text="Treatment")
                treatment_entry.pack(pady=2, fill="x")

                def save_treatment():
                    symptoms = symptoms_entry.get().strip()
                    treatment = treatment_entry.get().strip()
                    if not (symptoms and treatment):
                        messagebox.showerror("Error", "Please enter both symptoms and treatment.")
                        return
                    try:
                        # Get doctor_id from doctors table
                        self.cursor.execute("SELECT id FROM doctors WHERE firstname=%s", (self.username,))
                        doctor_row = self.cursor.fetchone()
                        if not doctor_row:
                            messagebox.showerror("Error", "Doctor not found in database. Please contact admin.")
                            return
                        doctor_id = doctor_row[0]
                        # Update the latest treatment row for this patient
                        self.cursor.execute(
                            "UPDATE treatments SET doctor_id=%s, symptoms=%s, treatment=%s WHERE treatment_id=%s",
                            (doctor_id, symptoms, treatment, vitals[0])
                        )
                        self.conn.commit()
                        messagebox.showinfo("Success", "Symptoms and treatment saved.")
                        symptoms_entry.delete(0, 'end')
                        treatment_entry.delete(0, 'end')
                        log_action(self.username, "Doctor", f"Updated symptoms/treatment for patient ID: {pid}")
                    except Exception as err:
                        messagebox.showerror("Database Error", f"Error: {err}")

                customtkinter.CTkButton(details_frame, text="Save", command=save_treatment).pack(pady=5)

                # Show patient history
                self.show_patient_history(pid, details_frame)

            patient_listbox.bind("<<ComboboxSelected>>", on_select)
            # Optionally, show first patient by default
            if patients:
                patient_listbox.set(f"{patients[0][0]} - {patients[0][1]}")
                on_select()
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_todays_patients(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Today's Treated Patients", font=("Arial", 18, "bold")).pack(pady=10)
        today = datetime.date.today()
        try:
            # Get doctor_id from doctors table
            self.cursor.execute("SELECT id FROM doctors WHERE firstname=%s", (self.username,))
            doctor_row = self.cursor.fetchone()
            doctor_id = doctor_row[0] if doctor_row else 0
            self.cursor.execute(
                "SELECT DISTINCT patient_id FROM treatments WHERE doctor_id=%s AND DATE(date)=%s",
                (doctor_id, today)
            )
            patients = self.cursor.fetchall()
            count = len(patients)
            customtkinter.CTkLabel(self.content, text=f"Total patients treated today: {count}", font=("Arial", 14)).pack(pady=5)
            if not patients:
                customtkinter.CTkLabel(self.content, text="No patients treated today.").pack()
            else:
                for p in patients:
                    self.cursor.execute("SELECT name FROM patients WHERE patient_id=%s", (p[0],))
                    patient_name = self.cursor.fetchone()
                    name_str = patient_name[0] if patient_name else "Unknown"
                    customtkinter.CTkLabel(
                        self.content,
                        text=f"Patient ID: {p[0]}, Name: {name_str}"
                    ).pack(anchor="w", padx=40)
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def check_emergencies(self):
        # Show emergency notes for all patients
        self.cursor.execute("""
            SELECT n.patient_id, p.name, n.note, n.date
            FROM patient_notes n
            JOIN patients p ON n.patient_id = p.patient_id
            WHERE n.emergency=1
            ORDER BY n.date DESC
        """)
        emergencies = self.cursor.fetchall()
        if emergencies:
            msg = "EMERGENCY ALERT!\n\n"
            for e in emergencies:
                msg += f"Patient: {e[1]} (ID: {e[0]})\nNote: {e[2]}\nDate: {e[3]}\n\n"
            messagebox.showwarning("Emergency Alert", msg)

    def logout(self):
        self.conn.close()
        self.master.destroy()

    def show_patient_history(self, pid, parent_frame):
        # Show all previous vitals, symptoms, treatments, and emergency notes
        customtkinter.CTkLabel(parent_frame, text="Patient History", font=("Arial", 13, "bold")).pack(anchor="w", pady=(8, 2))
        self.cursor.execute(
            "SELECT date, blood_pressure, temperature, weight, symptoms, treatment FROM treatments WHERE patient_id=%s ORDER BY date DESC",
            (pid,)
        )
        records = self.cursor.fetchall()
        if not records:
            customtkinter.CTkLabel(parent_frame, text="No previous records.", font=("Arial", 12, "italic")).pack(anchor="w")
        else:
            for rec in records:
                customtkinter.CTkLabel(
                    parent_frame,
                    text=f"Date: {rec[0]} | BP: {rec[1]}, Temp: {rec[2]}°C, Weight: {rec[3]}kg | Symptoms: {rec[4] or 'N/A'} | Treatment: {rec[5] or 'N/A'}",
                    font=("Arial", 12)
                ).pack(anchor="w", padx=10, pady=1)
        # Show emergency notes for this patient
        self.cursor.execute(
            "SELECT note, author, date FROM patient_notes WHERE patient_id=%s AND emergency=1 ORDER BY date DESC",
            (pid,)
        )
        notes = self.cursor.fetchall()
        if notes:
            customtkinter.CTkLabel(parent_frame, text="Emergency Notes:", font=("Arial", 12, "bold"), text_color="red").pack(anchor="w", pady=(8, 2))
            for n in notes:
                customtkinter.CTkLabel(
                    parent_frame,
                    text=f"{n[2]} by {n[1]}: {n[0]}",
                    font=("Arial", 12), text_color="red"
                ).pack(anchor="w", padx=20)