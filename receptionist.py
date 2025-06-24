import customtkinter
from tkinter import messagebox
from db_connection import get_connection

class ReceptionistFrame(customtkinter.CTkFrame):
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

        customtkinter.CTkLabel(self.sidebar, text="Receptionist", font=("Arial", 18, "bold"), fg_color="#2e3f4f", text_color="white").pack(pady=(30, 20))
        customtkinter.CTkButton(self.sidebar, text="Dashboard Home", command=self.show_welcome).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="Register Patient", command=self.show_register_patient).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="View Patients", command=self.show_view_patients).pack(fill="x", padx=20, pady=5)
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
        customtkinter.CTkLabel(self.content, text=f"Welcome, Receptionist {self.username}!", font=("Arial", 22, "bold")).pack(pady=40)
        customtkinter.CTkLabel(self.content, text="Use the sidebar to register or view patients.", font=("Arial", 14)).pack(pady=10)

    def show_register_patient(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Register Patient", font=("Arial", 18, "bold")).pack(pady=10)
        name_entry = customtkinter.CTkEntry(self.content, placeholder_text="Name")
        name_entry.pack(pady=5)
        dob_entry = customtkinter.CTkEntry(self.content, placeholder_text="Date of Birth (YYYY-MM-DD)")
        dob_entry.pack(pady=5)
        gender_entry = customtkinter.CTkEntry(self.content, placeholder_text="Gender (male/female)")
        gender_entry.pack(pady=5)

        def submit():
            name = name_entry.get().strip()
            dob = dob_entry.get().strip()
            gender = gender_entry.get().strip().lower()
            if not (name and dob and gender):
                messagebox.showerror("Error", "All fields are required.")
                return
            if gender not in ("male", "female"):
                messagebox.showerror("Error", "Gender must be 'male' or 'female'.")
                return
            # Validate date format
            try:
                import datetime
                datetime.datetime.strptime(dob, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Date of Birth must be in YYYY-MM-DD format.")
                return
            try:
                self.cursor.execute(
                    "INSERT INTO patients (name, date_of_birth, gender) VALUES (%s, %s, %s)",
                    (name, dob, gender)
                )
                self.conn.commit()
                self.cursor.execute("SELECT LAST_INSERT_ID()")
                new_id = self.cursor.fetchone()[0]
                messagebox.showinfo("Success", f"Patient {name} registered with ID: {new_id}")
                name_entry.delete(0, 'end')
                dob_entry.delete(0, 'end')
                gender_entry.delete(0, 'end')
            except Exception as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        customtkinter.CTkButton(self.content, text="Register", command=submit).pack(pady=10)

    def show_view_patients(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="Patients List", font=("Arial", 18, "bold")).pack(pady=10)
        try:
            self.cursor.execute("SELECT patient_id, name, date_of_birth, gender, date_registered FROM patients")
            patients = self.cursor.fetchall()
            if not patients:
                customtkinter.CTkLabel(self.content, text="No patient records found.").pack()
            else:
                for p in patients:
                    customtkinter.CTkLabel(
                        self.content,
                        text=f"ID: {p[0]}, Name: {p[1]}, DOB: {p[2]}, Gender: {p[3]}, Registered: {p[4]}"
                    ).pack(anchor="w", padx=20)
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def logout(self):
        self.conn.close()
        self.master.destroy()