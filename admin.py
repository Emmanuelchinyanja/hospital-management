import customtkinter
from tkinter import messagebox, ttk
import tkinter as tk
from datetime import datetime, date
from db_connection import get_connection

class AdminFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.on_logout = None  # Add this line

        # Layout: Sidebar and Main Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar with Queen Elizabeth Hospital branding
        self.sidebar = customtkinter.CTkFrame(self, width=220, fg_color="#1a472a")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # Hospital Logo/Title
        customtkinter.CTkLabel(
            self.sidebar, 
            text="Queen Elizabeth\nCentral Hospital", 
            font=("Arial", 16, "bold"),
            fg_color="#1a472a", 
            text_color="white",
            justify="center"
        ).pack(pady=(20, 10))
        
        customtkinter.CTkLabel(
            self.sidebar, 
            text="Administrator Portal", 
            font=("Arial", 12),
            fg_color="#1a472a", 
            text_color="#cccccc"
        ).pack(pady=(0, 20))

        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("User Management", self.show_user_management),
            ("Staff Management", self.show_staff_management),
            ("Patient Records", self.show_patient_records),
            ("Treatment Records", self.show_treatment_records),
            ("System Reports", self.show_system_reports),
            ("System Logs", self.show_logs),
            ("Database Backup", self.show_backup_options)
        ]
        
        for text, command in nav_items:
            btn = customtkinter.CTkButton(
                self.sidebar, 
                text=text, 
                command=command,
                height=35,
                font=("Arial", 12)
            )
            btn.pack(fill="x", padx=15, pady=3)
            self.nav_buttons[text] = btn

        # Logout button at bottom
        customtkinter.CTkButton(
            self.sidebar, 
            text="Logout", 
            command=self.logout,
            fg_color="#8B0000",
            hover_color="#A52A2A",
            height=40,
            font=("Arial", 12, "bold")
        ).pack(side="bottom", fill="x", padx=15, pady=20)

        # Main content area
        self.content = customtkinter.CTkFrame(self, fg_color="white")
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.show_dashboard()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text=f"Welcome, Admin {self.username}!", font=("Arial", 22, "bold")).pack(pady=40)
        customtkinter.CTkLabel(self.content, text="Use the sidebar to navigate the admin portal.", font=("Arial", 14)).pack(pady=10)

    def show_logs(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="System Logs", font=("Arial", 18, "bold")).pack(pady=10)

        # Filter section
        filter_frame = customtkinter.CTkFrame(self.content)
        filter_frame.pack(fill="x", padx=10, pady=5)
        dept_combo = customtkinter.CTkComboBox(filter_frame, values=["All", "Receptionist", "Nurse", "Doctor"])
        dept_combo.set("All")
        dept_combo.pack(side="left", padx=5)
        date_entry = customtkinter.CTkEntry(filter_frame, placeholder_text="YYYY-MM-DD (optional)")
        date_entry.pack(side="left", padx=5)
        filter_btn = customtkinter.CTkButton(filter_frame, text="Filter", command=lambda: self.show_logs_filtered(dept_combo.get(), date_entry.get()))
        filter_btn.pack(side="left", padx=5)

        self.show_logs_filtered("All", "")

    def show_logs_filtered(self, department, date_str):
        for widget in self.content.winfo_children():
            if isinstance(widget, customtkinter.CTkFrame) and widget != self.sidebar:
                widget.destroy()
        try:
            query = "SELECT log_id, user, department, action, log_date, timestamp FROM logs"
            params = []
            filters = []
            if department != "All":
                filters.append("department=%s")
                params.append(department)
            if date_str:
                filters.append("log_date=%s")
                params.append(date_str)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            query += " ORDER BY timestamp DESC"
            self.cursor.execute(query, tuple(params))
            logs = self.cursor.fetchall()
            if not logs:
                customtkinter.CTkLabel(self.content, text="No logs found.").pack()
                return

            # Table header
            header = customtkinter.CTkFrame(self.content, fg_color="#e0e0e0")
            header.pack(fill="x", padx=10, pady=(10,2))
            for col, w in zip(["ID", "User", "Department", "Action", "Date", "Time", "Delete"], [5, 15, 15, 40, 10, 15, 10]):
                customtkinter.CTkLabel(header, text=col, width=w*10, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=2)

            for log in logs:
                frame = customtkinter.CTkFrame(self.content, fg_color="white")
                frame.pack(fill="x", padx=10, pady=1)
                for val, w in zip(log[:-1], [5, 15, 15, 40, 10]):
                    customtkinter.CTkLabel(frame, text=str(val), width=w*10, anchor="w").pack(side="left", padx=2)
                customtkinter.CTkLabel(frame, text=str(log[-1]).split()[1][:8], width=15*10, anchor="w").pack(side="left", padx=2)
                del_btn = customtkinter.CTkButton(frame, text="Delete", width=60,
                                                  command=lambda log_id=log[0]: self.delete_log(log_id))
                del_btn.pack(side="left", padx=2)
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def delete_log(self, log_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this log?"):
            try:
                self.cursor.execute("DELETE FROM logs WHERE log_id=%s", (log_id,))
                self.conn.commit()
                messagebox.showinfo("Deleted", "Log entry deleted.")
                self.show_logs()
            except Exception as err:
                messagebox.showerror("Database Error", f"Error: {err}")

    def logout(self):
        self.conn.close()
        self.master.destroy()
        if self.on_logout:
            self.on_logout()

    def show_user_management(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="User Management", font=("Arial", 20, "bold")).pack(pady=20)

        # Add user section
        add_frame = customtkinter.CTkFrame(self.content)
        add_frame.pack(fill="x", padx=20, pady=10)
        customtkinter.CTkLabel(add_frame, text="Add New User", font=("Arial", 16, "bold")).pack(pady=10)
        form_frame = customtkinter.CTkFrame(add_frame, fg_color="transparent")
        form_frame.pack(pady=10)
        customtkinter.CTkLabel(form_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        username_entry = customtkinter.CTkEntry(form_frame, width=200)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        customtkinter.CTkLabel(form_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        password_entry = customtkinter.CTkEntry(form_frame, width=200, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)
        customtkinter.CTkLabel(form_frame, text="Role:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        role_combo = customtkinter.CTkComboBox(form_frame, values=["Receptionist", "Nurse", "Doctor", "Admin"], width=200)
        role_combo.grid(row=2, column=1, padx=10, pady=5)
        customtkinter.CTkButton(
            form_frame, text="Add User",
            command=lambda: self.add_user(username_entry.get(), password_entry.get(), role_combo.get())
        ).grid(row=3, column=1, padx=10, pady=15)

        # Users list
        list_frame = customtkinter.CTkFrame(self.content)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        customtkinter.CTkLabel(list_frame, text="Current Users", font=("Arial", 16, "bold")).pack(pady=10)
        self.show_users_list(list_frame)

    def add_user(self, username, password, role):
        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            self.cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Username already exists!")
                return
            self.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role)
            )
            self.conn.commit()
            messagebox.showinfo("Success", "User added successfully!")
            self.show_user_management()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error adding user: {e}")

    def show_users_list(self, parent_frame):
        try:
            self.cursor.execute("SELECT id, username, role, timestamp FROM users ORDER BY id")
            users = self.cursor.fetchall()
            if users:
                scrollable_frame = customtkinter.CTkScrollableFrame(parent_frame, height=300)
                scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
                header_frame = customtkinter.CTkFrame(scrollable_frame, fg_color="#e0e0e0")
                header_frame.pack(fill="x", pady=(0, 5))
                headers = ["ID", "Username", "Role", "Date Created", "Actions"]
                for i, header in enumerate(headers):
                    customtkinter.CTkLabel(header_frame, text=header, font=("Arial", 12, "bold"), width=120).grid(row=0, column=i, padx=5, pady=5)
                for user in users:
                    user_frame = customtkinter.CTkFrame(scrollable_frame)
                    user_frame.pack(fill="x", pady=2)
                    customtkinter.CTkLabel(user_frame, text=str(user[0]), width=120).grid(row=0, column=0, padx=5, pady=5)
                    customtkinter.CTkLabel(user_frame, text=user[1], width=120).grid(row=0, column=1, padx=5, pady=5)
                    customtkinter.CTkLabel(user_frame, text=user[2], width=120).grid(row=0, column=2, padx=5, pady=5)
                    customtkinter.CTkLabel(user_frame, text=str(user[3]).split()[0], width=120).grid(row=0, column=3, padx=5, pady=5)
                    if user[1] != 'admin':
                        customtkinter.CTkButton(
                            user_frame, text="Delete", width=80, fg_color="#ff4444",
                            command=lambda uid=user[0]: self.delete_user(uid)
                        ).grid(row=0, column=4, padx=5, pady=5)
                    else:
                        customtkinter.CTkLabel(user_frame, text="Protected", width=120).grid(row=0, column=4, padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading users: {e}")

    def delete_user(self, user_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
            try:
                self.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "User deleted successfully!")
                self.show_user_management()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error deleting user: {e}")

    def show_staff_management(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Doctor Management", font=("Arial", 20, "bold")).pack(pady=20)
        # Add doctor section
        add_frame = customtkinter.CTkFrame(self.content)
        add_frame.pack(fill="x", padx=20, pady=10)
        customtkinter.CTkLabel(add_frame, text="Register New Doctor", font=("Arial", 16, "bold")).pack(pady=10)
        form_frame = customtkinter.CTkFrame(add_frame, fg_color="transparent")
        form_frame.pack(pady=10)
        fields = {
            "First Name": customtkinter.CTkEntry(form_frame, width=200),
            "Last Name": customtkinter.CTkEntry(form_frame, width=200),
            "National ID": customtkinter.CTkEntry(form_frame, width=200),
            "Qualification": customtkinter.CTkEntry(form_frame, width=200),
            "Specialization": customtkinter.CTkComboBox(
                form_frame, values=["Surgeon", "Optician", "Physician", "Neurologist", "Medicine", "Hematologist"], width=200
            )
        }
        for i, (label, widget) in enumerate(fields.items()):
            customtkinter.CTkLabel(form_frame, text=f"{label}:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            widget.grid(row=i, column=1, padx=10, pady=5)
        customtkinter.CTkButton(
            form_frame, text="Register Doctor",
            command=lambda: self.add_doctor(fields)
        ).grid(row=len(fields), column=1, padx=10, pady=15)
        # Doctors list
        list_frame = customtkinter.CTkFrame(self.content)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        customtkinter.CTkLabel(list_frame, text="Registered Doctors", font=("Arial", 16, "bold")).pack(pady=10)
        self.show_doctors_list(list_frame)

    def add_doctor(self, fields):
        values = {k: v.get() for k, v in fields.items()}
        if not all(values.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        try:
            self.cursor.execute(
                "INSERT INTO doctors (firstname, lastname, national_id, qualification, specialization) VALUES (%s, %s, %s, %s, %s)",
                (values["First Name"], values["Last Name"], values["National ID"], values["Qualification"], values["Specialization"])
            )
            self.conn.commit()
            messagebox.showinfo("Success", "Doctor registered successfully!")
            self.show_staff_management()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error registering doctor: {e}")

    def show_doctors_list(self, parent_frame):
        try:
            self.cursor.execute("SELECT * FROM doctors ORDER BY id")
            doctors = self.cursor.fetchall()
            if doctors:
                scrollable_frame = customtkinter.CTkScrollableFrame(parent_frame, height=300)
                scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
                header_frame = customtkinter.CTkFrame(scrollable_frame, fg_color="#e0e0e0")
                header_frame.pack(fill="x", pady=(0, 5))
                headers = ["ID", "Name", "National ID", "Qualification", "Specialization", "Date Registered", "Actions"]
                for i, header in enumerate(headers):
                    customtkinter.CTkLabel(header_frame, text=header, font=("Arial", 10, "bold"), width=100).grid(row=0, column=i, padx=2, pady=5)
                for doctor in doctors:
                    doctor_frame = customtkinter.CTkFrame(scrollable_frame)
                    doctor_frame.pack(fill="x", pady=2)
                    full_name = f"{doctor[1]} {doctor[2]}"
                    data = [doctor[0], full_name, doctor[3], doctor[4], doctor[5], str(doctor[6]).split()[0]]
                    for i, value in enumerate(data):
                        customtkinter.CTkLabel(doctor_frame, text=str(value), width=100, font=("Arial", 9)).grid(row=0, column=i, padx=2, pady=5)
                    customtkinter.CTkButton(
                        doctor_frame, text="Delete", width=60, height=25, fg_color="#ff4444",
                        command=lambda did=doctor[0]: self.delete_doctor(did)
                    ).grid(row=0, column=6, padx=2, pady=5)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading doctors: {e}")

    def delete_doctor(self, doctor_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?\nThis will also affect treatment records."):
            try:
                self.cursor.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Doctor deleted successfully!")
                self.show_staff_management()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error deleting doctor: {e}")

    def show_patient_records(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Patient Records Overview", font=("Arial", 20, "bold")).pack(pady=20)
        # Search functionality
        search_frame = customtkinter.CTkFrame(self.content)
        search_frame.pack(fill="x", padx=20, pady=10)
        customtkinter.CTkLabel(search_frame, text="Search Patients:", font=("Arial", 14, "bold")).pack(pady=10)
        search_controls = customtkinter.CTkFrame(search_frame, fg_color="transparent")
        search_controls.pack(pady=10)
        search_entry = customtkinter.CTkEntry(search_controls, placeholder_text="Enter patient name or ID", width=300)
        search_entry.pack(side="left", padx=10)
        customtkinter.CTkButton(
            search_controls, text="Search",
            command=lambda: self.search_patients(search_entry.get())
        ).pack(side="left", padx=5)
        customtkinter.CTkButton(
            search_controls, text="Show All",
            command=self.show_all_patients
        ).pack(side="left", padx=5)
        # Results frame
        self.patients_results_frame = customtkinter.CTkFrame(self.content)
        self.patients_results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.show_all_patients()

    def show_all_patients(self):
        for widget in self.patients_results_frame.winfo_children():
            widget.destroy()
        try:
            self.cursor.execute("SELECT * FROM patients ORDER BY patient_id DESC LIMIT 50")
            patients = self.cursor.fetchall()
            customtkinter.CTkLabel(
                self.patients_results_frame,
                text=f"Recent Patients (Showing {len(patients)} records)",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            if patients:
                scrollable_frame = customtkinter.CTkScrollableFrame(self.patients_results_frame, height=400)
                scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
                header_frame = customtkinter.CTkFrame(scrollable_frame, fg_color="#e0e0e0")
                header_frame.pack(fill="x", pady=(0, 5))
                headers = ["Patient ID", "Name", "Gender", "Blood Type", "Date Registered", "Actions"]
                for i, header in enumerate(headers):
                    customtkinter.CTkLabel(header_frame, text=header, font=("Arial", 12, "bold"), width=120).grid(row=0, column=i, padx=5, pady=5)
                for patient in patients:
                    patient_frame = customtkinter.CTkFrame(scrollable_frame)
                    patient_frame.pack(fill="x", pady=2)
                    data = [patient[0], patient[1], patient[3], patient[4], str(patient[5]).split()[0]]
                    for i, value in enumerate(data):
                        customtkinter.CTkLabel(patient_frame, text=str(value), width=120).grid(row=0, column=i, padx=5, pady=5)
                    customtkinter.CTkButton(
                        patient_frame, text="View Treatments", width=100,
                        command=lambda pid=patient[0]: self.view_patient_treatments(pid)
                    ).grid(row=0, column=5, padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading patients: {e}")

    def search_patients(self, search_term):
        if not search_term:
            self.show_all_patients()
            return
        for widget in self.patients_results_frame.winfo_children():
            widget.destroy()
        try:
            if search_term.isdigit():
                self.cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (search_term,))
            else:
                self.cursor.execute("SELECT * FROM patients WHERE name LIKE %s", (f"%{search_term}%",))
            patients = self.cursor.fetchall()
            customtkinter.CTkLabel(
                self.patients_results_frame,
                text=f"Search Results ({len(patients)} found)",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            if patients:
                scrollable_frame = customtkinter.CTkScrollableFrame(self.patients_results_frame, height=400)
                scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
                for patient in patients:
                    patient_frame = customtkinter.CTkFrame(scrollable_frame)
                    patient_frame.pack(fill="x", pady=5)
                    info_text = f"ID: {patient[0]} | Name: {patient[1]} | Gender: {patient[3]} | Blood Type: {patient[4]} | Registered: {str(patient[5]).split()[0]}"
                    customtkinter.CTkLabel(patient_frame, text=info_text, font=("Arial", 12)).pack(side="left", padx=10, pady=10)
                    customtkinter.CTkButton(
                        patient_frame, text="View Treatments",
                        command=lambda pid=patient[0]: self.view_patient_treatments(pid)
                    ).pack(side="right", padx=10, pady=5)
            else:
                customtkinter.CTkLabel(
                    self.patients_results_frame,
                    text="No patients found matching your search.",
                    font=("Arial", 14)
                ).pack(pady=20)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error searching patients: {e}")

    def view_patient_treatments(self, patient_id):
        try:
            self.cursor.execute("""
                SELECT t.treatment_id, t.symptoms, t.treatment, t.blood_pressure, 
                       t.temperature, t.weight, t.date, d.firstname, d.lastname
                FROM treatments t
                LEFT JOIN doctors d ON t.doctor_id = d.id
                WHERE t.patient_id = %s
                ORDER BY t.date DESC
            """, (patient_id,))
            treatments = self.cursor.fetchall()
            treatment_window = customtkinter.CTkToplevel(self)
            treatment_window.title(f"Treatment History - Patient ID: {patient_id}")
            treatment_window.geometry("800x600")
            customtkinter.CTkLabel(
                treatment_window,
                text=f"Treatment History for Patient ID: {patient_id}",
                font=("Arial", 18, "bold")
            ).pack(pady=20)
            if treatments:
                scrollable_frame = customtkinter.CTkScrollableFrame(treatment_window, height=500)
                scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
                for treatment in treatments:
                    treatment_frame = customtkinter.CTkFrame(scrollable_frame)
                    treatment_frame.pack(fill="x", pady=10, padx=10)
                    doctor_name = f"{treatment[7]} {treatment[8]}" if treatment[7] else "Unknown Doctor"
                    treatment_info = f"""
Treatment ID: {treatment[0]}
Date: {treatment[6]}
Doctor: {doctor_name}
Symptoms: {treatment[1] or 'Not specified'}
Treatment: {treatment[2] or 'Not specified'}
Vitals: BP: {treatment[3]}, Temp: {treatment[4]}°C, Weight: {treatment[5]}kg
"""
                    customtkinter.CTkLabel(
                        treatment_frame,
                        text=treatment_info,
                        font=("Arial", 11),
                        justify="left"
                    ).pack(pady=10, padx=10, anchor="w")
            else:
                customtkinter.CTkLabel(
                    treatment_window,
                    text="No treatment records found for this patient.",
                    font=("Arial", 14)
                ).pack(pady=50)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading treatments: {e}")

    def show_treatment_records(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Treatment Records Overview", font=("Arial", 20, "bold")).pack(pady=20)
        filter_frame = customtkinter.CTkFrame(self.content)
        filter_frame.pack(fill="x", padx=20, pady=10)
        customtkinter.CTkLabel(filter_frame, text="Filter by Date:", font=("Arial", 14, "bold")).pack(pady=10)
        date_controls = customtkinter.CTkFrame(filter_frame, fg_color="transparent")
        date_controls.pack(pady=10)
        date_entry = customtkinter.CTkEntry(date_controls, placeholder_text="YYYY-MM-DD (optional)", width=200)
        date_entry.pack(side="left", padx=10)
        customtkinter.CTkButton(
            date_controls, text="Filter",
            command=lambda: self.filter_treatments_by_date(date_entry.get())
        ).pack(side="left", padx=5)
        customtkinter.CTkButton(
            date_controls, text="Show All",
            command=lambda: self.filter_treatments_by_date("")
        ).pack(side="left", padx=5)
        self.treatments_results_frame = customtkinter.CTkFrame(self.content)
        self.treatments_results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.filter_treatments_by_date("")

    def filter_treatments_by_date(self, date_str):
        for widget in self.treatments_results_frame.winfo_children():
            widget.destroy()
        try:
            if date_str:
                self.cursor.execute("""
                    SELECT t.treatment_id, p.name, t.symptoms, t.treatment, 
                           t.date, d.firstname, d.lastname
                    FROM treatments t
                    JOIN patients p ON t.patient_id = p.patient_id
                    LEFT JOIN doctors d ON t.doctor_id = d.id
                    WHERE DATE(t.date) = %s
                    ORDER BY t.date DESC
                """, (date_str,))
            else:
                self.cursor.execute("""
                    SELECT t.treatment_id, p.name, t.symptoms, t.treatment, 
                           t.date, d.firstname, d.lastname
                    FROM treatments t
                    JOIN patients p ON t.patient_id = p.patient_id
                    LEFT JOIN doctors d ON t.doctor_id = d.id
                    ORDER BY t.date DESC
                    LIMIT 100
                """)
            treatments = self.cursor.fetchall()
            customtkinter.CTkLabel(
                self.treatments_results_frame,
                text=f"Treatment Records ({len(treatments)} found)",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            if treatments:
                scrollable_frame = customtkinter.CTkScrollableFrame(self.treatments_results_frame, height=400)
                scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
                header_frame = customtkinter.CTkFrame(scrollable_frame, fg_color="#e0e0e0")
                header_frame.pack(fill="x", pady=(0, 5))
                headers = ["Treatment ID", "Patient", "Symptoms", "Treatment", "Date", "Doctor"]
                for i, header in enumerate(headers):
                    customtkinter.CTkLabel(header_frame, text=header, font=("Arial", 12, "bold"), width=120).grid(row=0, column=i, padx=5, pady=5)
                for treatment in treatments:
                    treatment_frame = customtkinter.CTkFrame(scrollable_frame)
                    treatment_frame.pack(fill="x", pady=2)
                    doctor_name = f"{treatment[5]} {treatment[6]}" if treatment[5] else "Unknown"
                    symptoms = treatment[2][:30] + "..." if treatment[2] and len(treatment[2]) > 30 else treatment[2] or "N/A"
                    treatment_desc = treatment[3][:30] + "..." if treatment[3] and len(treatment[3]) > 30 else treatment[3] or "N/A"
                    data = [
                        treatment[0],
                        treatment[1][:20] + "..." if len(treatment[1]) > 20 else treatment[1],
                        symptoms,
                        treatment_desc,
                        str(treatment[4]).split()[0] if treatment[4] else "N/A",
                        doctor_name[:20] + "..." if len(doctor_name) > 20 else doctor_name
                    ]
                    for i, value in enumerate(data):
                        customtkinter.CTkLabel(
                            treatment_frame, text=str(value), width=120, font=("Arial", 10)
                        ).grid(row=0, column=i, padx=5, pady=5)
            else:
                customtkinter.CTkLabel(
                    self.treatments_results_frame,
                    text="No treatment records found.",
                    font=("Arial", 14)
                ).pack(pady=20)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading treatments: {e}")

    def show_system_reports(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="System Reports & Analytics", font=("Arial", 20, "bold")).pack(pady=20)
        reports_frame = customtkinter.CTkFrame(self.content)
        reports_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # Monthly statistics
        monthly_frame = customtkinter.CTkFrame(reports_frame)
        monthly_frame.pack(fill="x", padx=20, pady=10)
        customtkinter.CTkLabel(monthly_frame, text="Monthly Statistics", font=("Arial", 16, "bold")).pack(pady=10)
        customtkinter.CTkButton(
            monthly_frame, text="Generate Monthly Report",
            command=self.generate_monthly_report
        ).pack(pady=10)
        # Department statistics
        dept_frame = customtkinter.CTkFrame(reports_frame)
        dept_frame.pack(fill="x", padx=20, pady=10)
        customtkinter.CTkLabel(dept_frame, text="Department Activity", font=("Arial", 16, "bold")).pack(pady=10)
        customtkinter.CTkButton(
            dept_frame, text="View Department Statistics",
            command=self.show_department_stats
        ).pack(pady=10)

    def generate_monthly_report(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Monthly Report", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        month_name = datetime.now().strftime("%B")
        
        customtkinter.CTkLabel(
            self.content,
            text=f"Report for {month_name} {current_year}",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Create a scrollable frame for the report
        report_frame = customtkinter.CTkScrollableFrame(self.content, width=700, height=400)
        report_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        try:
            # Get patient registrations for current month
            self.cursor.execute("""
                SELECT COUNT(*) FROM patients
                WHERE MONTH(date_registered) = %s AND YEAR(date_registered) = %s
            """, (current_month, current_year))
            patient_count = self.cursor.fetchone()[0]
            
            # Get treatment records for current month
            self.cursor.execute("""
                SELECT COUNT(*) FROM treatments
                WHERE MONTH(date) = %s AND YEAR(date) = %s
            """, (current_month, current_year))
            treatment_count = self.cursor.fetchone()[0]
            
            # Get doctor registrations for current month
            self.cursor.execute("""
                SELECT COUNT(*) FROM doctors
                WHERE MONTH(date_registered) = %s AND YEAR(date_registered) = %s
            """, (current_month, current_year))
            doctor_count = self.cursor.fetchone()[0]
            
            # Get user registrations for current month
            self.cursor.execute("""
                SELECT COUNT(*) FROM users
                WHERE MONTH(timestamp) = %s AND YEAR(timestamp) = %s
            """, (current_month, current_year))
            user_count = self.cursor.fetchone()[0]
            
            # Display statistics
            stats_frame = customtkinter.CTkFrame(report_frame)
            stats_frame.pack(fill="x", padx=10, pady=10)
            
            customtkinter.CTkLabel(
                stats_frame,
                text="Monthly Statistics",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            
            # Create a grid for statistics
            grid_frame = customtkinter.CTkFrame(stats_frame, fg_color="transparent")
            grid_frame.pack(fill="x", padx=20, pady=10)
            
            # Patient registrations
            patient_card = customtkinter.CTkFrame(grid_frame, width=200, height=100)
            patient_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            patient_card.grid_propagate(False)
            customtkinter.CTkLabel(
                patient_card,
                text="Patients Registered",
                font=("Arial", 12)
            ).pack(pady=(10, 5))
            customtkinter.CTkLabel(
                patient_card,
                text=str(patient_count),
                font=("Arial", 24, "bold")
            ).pack()
            
            # Treatment records
            treatment_card = customtkinter.CTkFrame(grid_frame, width=200, height=100)
            treatment_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            treatment_card.grid_propagate(False)
            customtkinter.CTkLabel(
                treatment_card,
                text="Treatment Records",
                font=("Arial", 12)
            ).pack(pady=(10, 5))
            customtkinter.CTkLabel(
                treatment_card,
                text=str(treatment_count),
                font=("Arial", 24, "bold")
            ).pack()
            
            # Doctor registrations
            doctor_card = customtkinter.CTkFrame(grid_frame, width=200, height=100)
            doctor_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
            doctor_card.grid_propagate(False)
            customtkinter.CTkLabel(
                doctor_card,
                text="Doctors Registered",
                font=("Arial", 12)
            ).pack(pady=(10, 5))
            customtkinter.CTkLabel(
                doctor_card,
                text=str(doctor_count),
                font=("Arial", 24, "bold")
            ).pack()
            
            # User registrations
            user_card = customtkinter.CTkFrame(grid_frame, width=200, height=100)
            user_card.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
            user_card.grid_propagate(False)
            customtkinter.CTkLabel(
                user_card,
                text="Users Registered",
                font=("Arial", 12)
            ).pack(pady=(10, 5))
            customtkinter.CTkLabel(
                user_card,
                text=str(user_count),
                font=("Arial", 24, "bold")
            ).pack()
            
            # Configure grid weights for responsive design
            grid_frame.grid_columnconfigure((0, 1, 2), weight=1)
            
            # Add a section for recent treatments
            recent_treatments_frame = customtkinter.CTkFrame(report_frame)
            recent_treatments_frame.pack(fill="x", padx=10, pady=(20, 10))
            customtkinter.CTkLabel(
                recent_treatments_frame,
                text="Recent Treatments This Month",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            
            # Fetch recent treatments
            self.cursor.execute("""
                SELECT t.treatment_id, p.name, t.symptoms, t.treatment, t.date, d.firstname, d.lastname
                FROM treatments t
                JOIN patients p ON t.patient_id = p.patient_id
                LEFT JOIN doctors d ON t.doctor_id = d.id
                WHERE MONTH(t.date) = %s AND YEAR(t.date) = %s
                ORDER BY t.date DESC
                LIMIT 10
            """, (current_month, current_year))
            treatments = self.cursor.fetchall()
            
            if treatments:
                # Create a table for treatments
                table_frame = customtkinter.CTkFrame(recent_treatments_frame)
                table_frame.pack(fill="x", padx=20, pady=10)
                
                # Table header
                header_frame = customtkinter.CTkFrame(table_frame, fg_color="#e0e0e0")
                header_frame.pack(fill="x", padx=5, pady=(0, 5))
                headers = ["ID", "Patient", "Symptoms", "Treatment", "Date", "Doctor"]
                for i, header in enumerate(headers):
                    customtkinter.CTkLabel(
                        header_frame,
                        text=header,
                        font=("Arial", 12, "bold"),
                        width=100
                    ).pack(side="left", padx=5, pady=5)
                
                # Table rows
                for treatment in treatments:
                    row_frame = customtkinter.CTkFrame(table_frame)
                    row_frame.pack(fill="x", padx=5, pady=2)
                    doctor_name = f"{treatment[5]} {treatment[6]}" if treatment[5] else "Unknown"
                    data = [
                        str(treatment[0]),
                        treatment[1][:15] + "..." if len(treatment[1]) > 15 else treatment[1],
                        treatment[2][:20] + "..." if treatment[2] and len(treatment[2]) > 20 else treatment[2] or "N/A",
                        treatment[3][:20] + "..." if treatment[3] and len(treatment[3]) > 20 else treatment[3] or "N/A",
                        str(treatment[4]).split()[0],
                        doctor_name[:15] + "..." if len(doctor_name) > 15 else doctor_name
                    ]
                    for value in data:
                        customtkinter.CTkLabel(
                            row_frame,
                            text=value,
                            font=("Arial", 10),
                            width=100
                        ).pack(side="left", padx=5, pady=5)
            else:
                customtkinter.CTkLabel(
                    recent_treatments_frame,
                    text="No treatments recorded this month.",
                    font=("Arial", 12)
                ).pack(pady=10)
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Error generating report: {e}")

    def show_department_stats(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Department Statistics", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Create a scrollable frame for the statistics
        stats_frame = customtkinter.CTkScrollableFrame(self.content, width=700, height=400)
        stats_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        try:
            # Get patient count by gender
            self.cursor.execute("SELECT gender, COUNT(*) FROM patients GROUP BY gender")
            patient_gender_data = self.cursor.fetchall()
            
            # Get patient count by blood type
            self.cursor.execute("SELECT blood_type, COUNT(*) FROM patients GROUP BY blood_type")
            patient_blood_data = self.cursor.fetchall()
            
            # Get treatment count by doctor
            self.cursor.execute("""
                SELECT d.firstname, d.lastname, COUNT(t.treatment_id) as treatment_count
                FROM doctors d
                LEFT JOIN treatments t ON d.id = t.doctor_id
                GROUP BY d.id, d.firstname, d.lastname
                ORDER BY treatment_count DESC
            """)
            doctor_treatment_data = self.cursor.fetchall()
            
            # Display patient gender statistics
            gender_frame = customtkinter.CTkFrame(stats_frame)
            gender_frame.pack(fill="x", padx=10, pady=10)
            customtkinter.CTkLabel(
                gender_frame,
                text="Patient Gender Distribution",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            
            if patient_gender_data:
                for gender, count in patient_gender_data:
                    customtkinter.CTkLabel(
                        gender_frame,
                        text=f"{gender.capitalize()}: {count}",
                        font=("Arial", 12)
                    ).pack(pady=2)
            else:
                customtkinter.CTkLabel(
                    gender_frame,
                    text="No patient gender data available",
                    font=("Arial", 12)
                ).pack(pady=2)
            
            # Display patient blood type statistics
            blood_frame = customtkinter.CTkFrame(stats_frame)
            blood_frame.pack(fill="x", padx=10, pady=10)
            customtkinter.CTkLabel(
                blood_frame,
                text="Patient Blood Type Distribution",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            
            if patient_blood_data:
                for blood_type, count in patient_blood_data:
                    customtkinter.CTkLabel(
                        blood_frame,
                        text=f"Blood Type {blood_type}: {count}",
                        font=("Arial", 12)
                    ).pack(pady=2)
            else:
                customtkinter.CTkLabel(
                    blood_frame,
                    text="No patient blood type data available",
                    font=("Arial", 12)
                ).pack(pady=2)
            
            # Display doctor treatment statistics
            doctor_frame = customtkinter.CTkFrame(stats_frame)
            doctor_frame.pack(fill="x", padx=10, pady=10)
            customtkinter.CTkLabel(
                doctor_frame,
                text="Treatments by Doctor",
                font=("Arial", 16, "bold")
            ).pack(pady=10)
            
            if doctor_treatment_data:
                for firstname, lastname, count in doctor_treatment_data:
                    doctor_name = f"{firstname} {lastname}" if firstname and lastname else "Unknown Doctor"
                    customtkinter.CTkLabel(
                        doctor_frame,
                        text=f"{doctor_name}: {count} treatments",
                        font=("Arial", 12)
                    ).pack(pady=2)
            else:
                customtkinter.CTkLabel(
                    doctor_frame,
                    text="No doctor treatment data available",
                    font=("Arial", 12)
                ).pack(pady=2)
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading department statistics: {e}")

    def show_backup_options(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Database Backup & Maintenance", font=("Arial", 20, "bold")).pack(pady=20)
        backup_frame = customtkinter.CTkFrame(self.content)
        backup_frame.pack(fill="x", padx=20, pady=10)
        customtkinter.CTkLabel(backup_frame, text="Database Backup", font=("Arial", 16, "bold")).pack(pady=15)
        customtkinter.CTkLabel(
            backup_frame,
            text="Create a backup of all hospital data including patients, treatments, and user records.",
            font=("Arial", 12)
        ).pack(pady=5)
        customtkinter.CTkButton(
            backup_frame, text="Create Backup",
            command=self.create_backup, height=40
        ).pack(pady=15)

    def create_backup(self):
        try:
            # Import required modules
            import subprocess
            import os
            from os.path import expanduser
            
            # Create backup directory
            user_home = expanduser("~")
            backup_dir = os.path.join(user_home, "hospital_backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate timestamp for backup file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"hospital_db_backup_{timestamp}.sql")
            
            # Get database connection details
            db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'hospital-management'
            }
            
            # Create backup using mysqldump command
            dump_command = [
                'mysqldump',
                f'--host={db_config["host"]}',
                f'--user={db_config["user"]}',
                f'--password={db_config["password"]}',
                db_config["database"]
            ]
            
            # Execute the mysqldump command and save to file
            with open(backup_file, 'w') as output_file:
                process = subprocess.run(
                    dump_command,
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
            # Check if the backup was successful
            if process.returncode == 0:
                messagebox.showinfo("Backup Successful", f"Database backup created:\n{backup_file}")
            else:
                # If mysqldump failed, try a simple file copy as fallback
                # This assumes the database file is accessible directly
                try:
                    # Try to locate the database file (this is a simplified approach)
                    # In a real application, you would need to know the exact path
                    db_file_path = "db/hospital-management.sql"  # Adjust path as needed
                    if os.path.exists(db_file_path):
                        import shutil
                        shutil.copyfile(db_file_path, backup_file)
                        messagebox.showinfo("Backup Successful", f"Database backup created (using file copy):\n{backup_file}")
                    else:
                        raise Exception("Database file not found for backup")
                except Exception as copy_error:
                    messagebox.showerror("Backup Error", f"Error creating backup:\n{process.stderr}\n\nFallback error: {copy_error}")
        except Exception as e:
            messagebox.showerror("Backup Error", f"Error creating backup: {e}")