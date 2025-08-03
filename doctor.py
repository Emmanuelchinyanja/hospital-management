import customtkinter
from tkinter import messagebox, ttk
from db_connection import get_connection, log_action
import datetime

class DoctorFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor(buffered=True)
        self.on_logout = None  # Add this line
        
        # Professional color scheme
        self.colors = {
            'primary': '#1e3a5f',      # Deep blue
            'secondary': '#2c5f41',     # Forest green  
            'accent': '#d4af37',        # Gold
            'light_blue': '#e8f4f8',    # Light blue
            'white': '#ffffff',
            'light_gray': '#f5f5f5',
            'text_dark': '#2c3e50',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#3498db'
        }
        
        # Configure main layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create header
        self.create_header()
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.content = customtkinter.CTkScrollableFrame(self, fg_color=self.colors['light_gray'])
        self.content.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        # Create footer
        self.create_footer()
        
        # Check if doctor exists, else show registration
        self.check_and_register_doctor()

    def create_header(self):
        """Create professional hospital header"""
        header = customtkinter.CTkFrame(self, height=80, fg_color=self.colors['primary'])
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)
        
        # Hospital info
        logo_frame = customtkinter.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)
        
        customtkinter.CTkLabel(
            logo_frame,
            text="🏥 QUEEN ELIZABETH CENTRAL HOSPITAL",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(side="left")
        
        customtkinter.CTkLabel(
            logo_frame,
            text="Medical Excellence • Blantyre, Malawi",
            font=("Arial", 12),
            text_color=self.colors['light_blue']
        ).pack(side="left", padx=(10, 0))
        
        # Doctor info and time
        user_frame = customtkinter.CTkFrame(header, fg_color="transparent")
        user_frame.pack(side="right", padx=20, pady=10)

        current_time = datetime.datetime.now().strftime("%H:%M - %B %d, %Y")
        customtkinter.CTkLabel(
            user_frame,
            text=f"👨‍⚕️ Dr. {self.username}",
            font=("Arial", 14, "bold"),
            text_color="white"
        ).pack(anchor="e")

        customtkinter.CTkLabel(
            user_frame,
            text=current_time,
            font=("Arial", 11),
            text_color=self.colors['light_blue']
        ).pack(anchor="e")

        # Add logout button to header (top right)
        logout_btn = customtkinter.CTkButton(
            user_frame,
            text="🚪 Logout",
            command=self.logout,
            height=35,
            font=("Arial", 12, "bold"),
            fg_color=self.colors['danger'],
            hover_color="#c0392b",
            text_color="white"
        )
        logout_btn.pack(anchor="e", pady=(10, 0))

    def create_sidebar(self):
        """Create enhanced sidebar"""
        self.sidebar = customtkinter.CTkFrame(self, width=250, fg_color=self.colors['secondary'])
        self.sidebar.grid(row=1, column=0, sticky="ns", padx=(10, 5), pady=10)
        self.sidebar.grid_propagate(False)
        
        # Sidebar title
        title_frame = customtkinter.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=(20, 30))
        
        customtkinter.CTkLabel(
            title_frame,
            text="🩺 MEDICAL STATION",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack()
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Dashboard", self.show_welcome),
            ("👥 All Patients", self.show_patients),
            ("📅 Today's Patients", self.show_todays_patients),
            ("🚨 Emergency Cases", self.show_emergency_cases),
            ("📊 Patient Statistics", self.show_statistics),
            ("🔍 Search Patient", self.show_search_patient),
            ("⚙️ Doctor Profile", self.show_doctor_profile)
        ]
        
        for text, command in nav_buttons:
            btn = customtkinter.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=45,
                font=("Arial", 13, "bold"),
                fg_color="transparent",
                hover_color=self.colors['primary'],
                text_color="white",
                anchor="w"
            )
            btn.pack(fill="x", padx=15, pady=3)
        
        # Emergency alert button
        emergency_btn = customtkinter.CTkButton(
            self.sidebar,
            text="🚨 Check Emergencies",
            command=self.check_emergencies,
            height=50,
            font=("Arial", 12, "bold"),
            fg_color=self.colors['danger'],
            hover_color="#c0392b",
            text_color="white"
        )
        emergency_btn.pack(fill="x", padx=15, pady=10)
        
        # Logout button
        logout_btn = customtkinter.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            command=self.logout,
            height=50,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['text_dark'],
            hover_color="#1a252f",
            text_color="white"
        )
        logout_btn.pack(side="bottom", fill="x", padx=15, pady=20)

    def create_footer(self):
        """Create professional footer"""
        footer = customtkinter.CTkFrame(self, height=50, fg_color=self.colors['text_dark'])
        footer.grid(row=2, column=0, columnspan=2, sticky="ew")
        footer.grid_propagate(False)
        
        contact_frame = customtkinter.CTkFrame(footer, fg_color="transparent")
        contact_frame.pack(expand=True)
        
        customtkinter.CTkLabel(
            contact_frame,
            text="📞 Medical Emergency: +265 1 871 911 | 📧 medical@qech.gov.mw",
            font=("Arial", 11),
            text_color="white"
        ).pack(pady=5)
        
        customtkinter.CTkLabel(
            contact_frame,
            text="© 2025 Queen Elizabeth Central Hospital • Licensed Medical System",
            font=("Arial", 10),
            text_color="#bdc3c7"
        ).pack()

    def clear_content(self):
        """Clear main content area"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def check_and_register_doctor(self):
        """Check if doctor exists in database"""
        try:
            self.cursor.execute("SELECT id, specialization FROM doctors WHERE firstname=%s", (self.username,))
            doctor_row = self.cursor.fetchone()
            if not doctor_row:
                self.show_register_doctor()
            else:
                self.doctor_id = doctor_row[0]
                self.doctor_specialization = doctor_row[1]
                self.show_welcome()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error checking doctor: {str(e)}")
            self.show_register_doctor()

    def show_register_doctor(self):
        """Enhanced doctor registration"""
        self.clear_content()
        
        # Title
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="👨‍⚕️ Doctor Registration",
            font=("Arial", 24, "bold"),
            text_color=self.colors['text_dark']
        ).pack()
        
        customtkinter.CTkLabel(
            title_frame,
            text="Please complete your profile to access the medical system",
            font=("Arial", 14),
            text_color="#7f8c8d"
        ).pack(pady=(5, 0))
        
        # Registration form
        form_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        fields = [
            ("First Name", "firstname"),
            ("Last Name", "lastname"),
            ("National ID", "national_id"),
            ("Medical Qualification", "qualification")
        ]
        
        entries = {}
        
        for label_text, field_name in fields:
            customtkinter.CTkLabel(
                form_frame,
                text=f"{label_text}:",
                font=("Arial", 12, "bold"),
                text_color=self.colors['text_dark']
            ).pack(anchor="w", padx=30, pady=(20, 5))
            
            entry = customtkinter.CTkEntry(
                form_frame,
                placeholder_text=f"Enter {label_text.lower()}",
                height=35,
                width=400,
                font=("Arial", 11)
            )
            entry.pack(anchor="w", padx=30, pady=(0, 10))
            entries[field_name] = entry
        
        # Specialization dropdown
        customtkinter.CTkLabel(
            form_frame,
            text="Medical Specialization:",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=30, pady=(20, 5))
        
        specializations = [
            'General Medicine', 'Surgery', 'Pediatrics', 'Obstetrics & Gynecology',
            'Internal Medicine', 'Cardiology', 'Neurology', 'Orthopedics',
            'Ophthalmology', 'Dermatology', 'Psychiatry', 'Radiology',
            'Emergency Medicine', 'Family Medicine', 'Anesthesiology'
        ]
        
        spec_combo = customtkinter.CTkComboBox(
            form_frame,
            values=specializations,
            height=35,
            width=400,
            font=("Arial", 11)
        )
        spec_combo.pack(anchor="w", padx=30, pady=(0, 30))
        spec_combo.set('General Medicine')
        
        def register():
            """Register new doctor"""
            # Get all field values
            fname = entries['firstname'].get().strip()
            lname = entries['lastname'].get().strip()
            natid = entries['national_id'].get().strip()
            qual = entries['qualification'].get().strip()
            spec = spec_combo.get().strip()
            
            # Validation
            if not all([fname, lname, natid, qual, spec]):
                messagebox.showerror("❌ Error", "All fields are required.")
                return
            
            try:
                self.cursor.execute(
                    """INSERT INTO doctors (firstname, lastname, national_id, qualification, specialization) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (fname, lname, natid, qual, spec)
                )
                self.conn.commit()
                
                messagebox.showinfo("✅ Success", f"Welcome Dr. {fname}! Your profile has been registered successfully.")
                
                self.username = fname
                log_action(self.username, "Doctor", "Registered new doctor profile")
                
                # After registering a doctor
                self.cursor.execute("SELECT id FROM doctors WHERE firstname=%s AND lastname=%s", (fname, lname))
                row = self.cursor.fetchone()
                if row:
                    self.doctor_id = row[0]
                
                self.check_and_register_doctor()
                
            except Exception as err:
                messagebox.showerror("❌ Database Error", f"Registration failed: {str(err)}")
        
        # Register button
        register_btn = customtkinter.CTkButton(
            form_frame,
            text="👨‍⚕️ Register Doctor Profile",
            command=register,
            height=50,
            width=250,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['success'],
            hover_color="#219a52"
        )
        register_btn.pack(pady=30)

    def show_welcome(self):
        """Enhanced dashboard with medical statistics"""
        self.clear_content()
        
        # Welcome header
        welcome_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            welcome_frame,
            text=f"Welcome back, Dr. {self.username}! 👨‍⚕️",
            font=("Arial", 24, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        if hasattr(self, 'doctor_specialization'):
            customtkinter.CTkLabel(
                welcome_frame,
                text=f"Specialization: {self.doctor_specialization} • Queen Elizabeth Central Hospital",
                font=("Arial", 14),
                text_color="#7f8c8d"
            ).pack(anchor="w", pady=(5, 0))
        
        # Statistics cards
        stats_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        try:
            # Get statistics
            self.cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = self.cursor.fetchone()[0]
            
            self.cursor.execute(
                "SELECT COUNT(DISTINCT patient_id) FROM treatments WHERE doctor_id=%s AND DATE(date) = CURDATE()",
                (getattr(self, 'doctor_id', 0),)
            )
            today_patients = self.cursor.fetchone()[0]
            
            self.cursor.execute(
                "SELECT COUNT(*) FROM patient_notes WHERE emergency = TRUE AND DATE(date) = CURDATE()"
            )
            emergencies = self.cursor.fetchone()[0]
            
            self.cursor.execute(
                "SELECT COUNT(DISTINCT patient_id) FROM treatments WHERE doctor_id=%s",
                (getattr(self, 'doctor_id', 0),)
            )
            total_treated = self.cursor.fetchone()[0]
            
        except:
            total_patients = today_patients = emergencies = total_treated = 0
        
        # Create stat cards
        stats = [
            ("👥 Total Patients", total_patients, self.colors['info']),
            ("📅 Today's Patients", today_patients, self.colors['success']),
            ("🚨 Emergency Cases", emergencies, self.colors['danger']),
            ("🩺 Patients Treated", total_treated, self.colors['primary'])
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = customtkinter.CTkFrame(stats_frame, fg_color=color, width=180, height=120)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            customtkinter.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 28, "bold"),
                text_color="white"
            ).pack(pady=(20, 5))
            
            customtkinter.CTkLabel(
                card,
                text=title,
                font=("Arial", 12),
                text_color="white"
            ).pack()
        
        # Quick actions
        actions_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        actions_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        customtkinter.CTkLabel(
            actions_frame,
            text="⚡ Quick Medical Actions",
            font=("Arial", 18, "bold"),
            text_color=self.colors['text_dark']
        ).pack(pady=20)
        
        # Quick action buttons
        quick_frame = customtkinter.CTkFrame(actions_frame, fg_color="transparent")
        quick_frame.pack(expand=True, fill="both", padx=40, pady=20)
        
        actions = [
            ("👥 View All Patients", self.show_patients, self.colors['primary']),
            ("📅 Today's Schedule", self.show_todays_patients, self.colors['success']),
            ("🚨 Emergency Alert", self.check_emergencies, self.colors['danger']),
            ("🔍 Search Patient", self.show_search_patient, self.colors['info'])
        ]
        
        for i, (text, command, color) in enumerate(actions):
            btn = customtkinter.CTkButton(
                quick_frame,
                text=text,
                command=command,
                width=200,
                height=60,
                font=("Arial", 14, "bold"),
                fg_color=color,
                hover_color=color
            )
            btn.grid(row=i//2, column=i%2, padx=20, pady=15, sticky="ew")

    def show_patients(self):
        """Enhanced patient management interface"""
        self.clear_content()
        
        # Title
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="👥 Patient Management System",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        try:
            self.cursor.execute(
                "SELECT patient_id, name, date_of_birth, gender, blood_type FROM patients ORDER BY date_registered DESC"
            )
            patients = self.cursor.fetchall()
            
            if not patients:
                customtkinter.CTkLabel(
                    self.content,
                    text="📋 No patients found in the system.",
                    font=("Arial", 16),
                    text_color=self.colors['text_dark']
                ).pack(pady=50)
                return
            
            # Patient selection
            selection_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
            selection_frame.pack(fill="x", padx=20, pady=20)
            
            customtkinter.CTkLabel(
                selection_frame,
                text="Select Patient:",
                font=("Arial", 14, "bold"),
                text_color=self.colors['text_dark']
            ).pack(anchor="w", padx=20, pady=(20, 5))
            
            patient_combo = customtkinter.CTkComboBox(
                selection_frame,
                values=[f"{p[0]} - {p[1]}" for p in patients],
                width=500,
                height=35,
                font=("Arial", 12),
                command=lambda _: show_patient_details()  # This ensures the details update on selection
            )
            patient_combo.pack(anchor="w", padx=20, pady=(0, 20))
            
            # Patient details area
            details_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['light_gray'])
            details_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            def show_patient_details():
                """Display comprehensive patient information"""
                for widget in details_frame.winfo_children():
                    widget.destroy()
                
                selection = patient_combo.get()
                if not selection:
                    return
                
                pid = selection.split(" - ")[0]
                
                # Get patient info
                self.cursor.execute(
                    "SELECT name, date_of_birth, gender, blood_type FROM patients WHERE patient_id=%s",
                    (pid,)
                )
                patient_info = self.cursor.fetchone()
                
                if not patient_info:
                    return
                
                # Patient info header
                info_header = customtkinter.CTkFrame(details_frame, fg_color=self.colors['primary'])
                info_header.pack(fill="x", padx=20, pady=20)
                
                customtkinter.CTkLabel(
                    info_header,
                    text=f"👤 {patient_info[0]} (ID: {pid})",
                    font=("Arial", 18, "bold"),
                    text_color="white"
                ).pack(pady=15)
                
                patient_details = f"📅 DOB: {patient_info[1]} | ⚥ Gender: {patient_info[2]} | 🩸 Blood Type: {patient_info[3]}"
                customtkinter.CTkLabel(
                    info_header,
                    text=patient_details,
                    font=("Arial", 12),
                    text_color="white"
                ).pack(pady=(0, 15))
                
                # Latest vitals
                self.cursor.execute(
                    """SELECT treatment_id, blood_pressure, temperature, weight, date, symptoms, treatment
                       FROM treatments WHERE patient_id=%s ORDER BY date DESC LIMIT 1""",
                    (pid,)
                )
                latest_vitals = self.cursor.fetchone()
                
                vitals_frame = customtkinter.CTkFrame(details_frame, fg_color=self.colors['white'])
                vitals_frame.pack(fill="x", padx=20, pady=10)
                
                if latest_vitals and any(latest_vitals[1:4]):  # If any vitals exist
                    customtkinter.CTkLabel(
                        vitals_frame,
                        text="🩺 Latest Vital Signs",
                        font=("Arial", 16, "bold"),
                        text_color=self.colors['text_dark']
                    ).pack(pady=(15, 10))
                    
                    # Vitals display
                    vitals_grid = customtkinter.CTkFrame(vitals_frame, fg_color="transparent")
                    vitals_grid.pack(fill="x", padx=20, pady=10)
                    
                    vital_data = [
                        ("🫀 Blood Pressure", latest_vitals[1] or "Not recorded"),
                        ("🌡️ Temperature", f"{latest_vitals[2]}°C" if latest_vitals[2] else "Not recorded"),
                        ("⚖️ Weight", f"{latest_vitals[3]} kg" if latest_vitals[3] else "Not recorded"),
                    ]
                    
                    for i, (label, value) in enumerate(vital_data):
                        row = i // 2
                        col = i % 2
                        
                        vital_card = customtkinter.CTkFrame(vitals_grid, fg_color=self.colors['light_blue'])
                        vital_card.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
                        
                        customtkinter.CTkLabel(
                            vital_card,
                            text=label,
                            font=("Arial", 11, "bold")
                        ).pack(pady=(8, 0))
                        
                        customtkinter.CTkLabel(
                            vital_card,
                            text=str(value),
                            font=("Arial", 12)
                        ).pack(pady=(0, 8))
                    
                    vitals_grid.grid_columnconfigure(0, weight=1)
                    vitals_grid.grid_columnconfigure(1, weight=1)
                    
                    # Show existing diagnosis/treatment
                    if latest_vitals[5] or latest_vitals[6]:
                        customtkinter.CTkLabel(
                            vitals_frame,
                            text=f"🔍 Current Symptoms: {latest_vitals[5] or 'Not recorded'}",
                            font=("Arial", 12),
                            text_color=self.colors['text_dark']
                        ).pack(anchor="w", padx=20, pady=(10, 5))
                        
                        customtkinter.CTkLabel(
                            vitals_frame,
                            text=f"💊 Current Treatment: {latest_vitals[6] or 'Not prescribed'}",
                            font=("Arial", 12),
                            text_color=self.colors['text_dark']
                        ).pack(anchor="w", padx=20, pady=(0, 15))
                    
                    # Medical treatment form
                    treatment_frame = customtkinter.CTkFrame(details_frame, fg_color=self.colors['white'])
                    treatment_frame.pack(fill="x", padx=20, pady=10)
                    
                    customtkinter.CTkLabel(
                        treatment_frame,
                        text="📋 Update Medical Assessment",
                        font=("Arial", 16, "bold"),
                        text_color=self.colors['text_dark']
                    ).pack(pady=(15, 10))
                    
                    # Symptoms input
                    customtkinter.CTkLabel(
                        treatment_frame,
                        text="🔍 Symptoms & Diagnosis:",
                        font=("Arial", 12, "bold")
                    ).pack(anchor="w", padx=20, pady=(10, 5))
                    
                    symptoms_text = customtkinter.CTkTextbox(
                        treatment_frame,
                        height=80,
                        width=500,
                        font=("Arial", 11)
                    )
                    symptoms_text.pack(anchor="w", padx=20, pady=(0, 10))
                    
                    # Treatment input
                    customtkinter.CTkLabel(
                        treatment_frame,
                        text="💊 Treatment & Prescription:",
                        font=("Arial", 12, "bold")
                    ).pack(anchor="w", padx=20, pady=(10, 5))
                    
                    treatment_text = customtkinter.CTkTextbox(
                        treatment_frame,
                        height=80,
                        width=500,
                        font=("Arial", 11)
                    )
                    treatment_text.pack(anchor="w", padx=20, pady=(0, 20))
                    
                    def save_medical_assessment():
                        """Save symptoms and treatment"""
                        symptoms = symptoms_text.get("1.0", "end-1c").strip()
                        treatment = treatment_text.get("1.0", "end-1c").strip()
                        
                        if not symptoms and not treatment:
                            messagebox.showerror("❌ Error", "Please enter symptoms or treatment.")
                            return
                        
                        try:
                            # Update the latest treatment record
                            self.cursor.execute(
                                """UPDATE treatments SET doctor_id=%s, symptoms=%s, treatment=%s, date=CURRENT_TIMESTAMP
                                   WHERE treatment_id=%s""",
                                (self.doctor_id, symptoms, treatment, latest_vitals[0])
                            )
                            self.conn.commit()
                            
                            messagebox.showinfo("✅ Success", "Medical assessment saved successfully!")
                            
                            # Clear form
                            symptoms_text.delete("1.0", "end")
                            treatment_text.delete("1.0", "end")
                            
                            log_action(self.username, "Doctor", f"Updated medical assessment for patient ID: {pid}")
                            
                            # Refresh display
                            show_patient_details()
                            
                        except Exception as err:
                            messagebox.showerror("❌ Database Error", f"Error saving assessment: {str(err)}")
                    
                    # Save button
                    save_btn = customtkinter.CTkButton(
                        treatment_frame,
                        text="💾 Save Medical Assessment",
                        command=save_medical_assessment,
                        height=45,
                        width=250,
                        font=("Arial", 14, "bold"),
                        fg_color=self.colors['success'],
                        hover_color="#219a52"
                    )
                    save_btn.pack(pady=(0, 20))
                    
                else:
                    customtkinter.CTkLabel(
                        vitals_frame,
                        text="📊 No vitals recorded yet. Please ask a nurse to record vitals first.",
                        font=("Arial", 14),
                        text_color=self.colors['warning']
                    ).pack(pady=30)
                
                # Patient history
                self.show_patient_medical_history(pid, details_frame)
            
            # Bind selection event
            patient_combo.bind("<<ComboboxSelected>>", lambda e: show_patient_details())
            
            # Show first patient by default
            if patients:
                patient_combo.set(f"{patients[0][0]} - {patients[0][1]}")
                show_patient_details()
                
        except Exception as err:
            messagebox.showerror("❌ Database Error", f"Error loading patients: {str(err)}")

    def show_patient_medical_history(self, patient_id, parent_frame):
        """Display comprehensive patient medical history"""
        history_frame = customtkinter.CTkFrame(parent_frame, fg_color=self.colors['white'])
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        customtkinter.CTkLabel(
            history_frame,
            text="📚 Complete Medical History",
            font=("Arial", 16, "bold"),
            text_color=self.colors['text_dark']
        ).pack(pady=(15, 10))
        
        try:
            # Get all treatment records
            self.cursor.execute(
                """SELECT date, blood_pressure, temperature, weight, symptoms, treatment, heart_rate
                   FROM treatments WHERE patient_id=%s ORDER BY date DESC""",
                (patient_id,)
            )
            records = self.cursor.fetchall()
            
            if records:
                # Create scrollable history
                history_scroll = customtkinter.CTkScrollableFrame(history_frame, height=300)
                history_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                
                for i, record in enumerate(records):
                    record_frame = customtkinter.CTkFrame(history_scroll, fg_color=self.colors['light_blue'])
                    record_frame.pack(fill="x", pady=5)
                    
                    # Record header
                    customtkinter.CTkLabel(
                        record_frame,
                        text=f"📅 Visit #{i+1} - {record[0].strftime('%Y-%m-%d %H:%M')}",
                        font=("Arial", 12, "bold"),
                        text_color=self.colors['text_dark']
                    ).pack(anchor="w", padx=15, pady=(10, 5))
                    
                    # Vitals
                    vitals_text = "🩺 Vitals: "
                    vitals_parts = []
                    if record[1]: vitals_parts.append(f"BP: {record[1]}")
                    if record[2]: vitals_parts.append(f"Temp: {record[2]}°C")
                    if record[3]: vitals_parts.append(f"Weight: {record[3]}kg")
                    
                    if vitals_parts:
                        vitals_text += " | ".join(vitals_parts)
                    else:
                        vitals_text += "Not recorded"
                    
                    customtkinter.CTkLabel(
                        record_frame,
                        text=vitals_text,
                        font=("Arial", 11),
                        text_color=self.colors['text_dark']
                    ).pack(anchor="w", padx=15, pady=2)
                    
                    # Medical info
                    if record[4]:  # Symptoms
                        customtkinter.CTkLabel(
                            record_frame,
                            text=f"🔍 Symptoms: {record[4]}",
                            font=("Arial", 11),
                            text_color=self.colors['text_dark'],
                            wraplength=400
                        ).pack(anchor="w", padx=15, pady=2)
                    
                    if record[5]:  # Treatment
                        customtkinter.CTkLabel(
                            record_frame,
                            text=f"💊 Treatment: {record[5]}",
                            font=("Arial", 11),
                            text_color=self.colors['text_dark'],
                            wraplength=400
                        ).pack(anchor="w", padx=15, pady=(2, 10))
            else:
                customtkinter.CTkLabel(
                    history_frame,
                    text="📋 No medical history available.",
                    font=("Arial", 12),
                    text_color="#777"
                ).pack(pady=20)
            
            # Emergency notes
            self.cursor.execute(
                """SELECT note, author, date FROM patient_notes 
                   WHERE patient_id=%s AND emergency=1 ORDER BY date DESC""",
                (patient_id,)
            )
            emergency_notes = self.cursor.fetchall()
            
            if emergency_notes:
                customtkinter.CTkLabel(
                    history_frame,
                    text="🚨 Emergency Notes:",
                    font=("Arial", 14, "bold"),
                    text_color=self.colors['danger']
                ).pack(anchor="w", padx=20, pady=(10, 5))
                
                for note, author, date in emergency_notes:
                    emergency_frame = customtkinter.CTkFrame(history_frame, fg_color=self.colors['danger'])
                    emergency_frame.pack(fill="x", padx=20, pady=5)
                    
                    customtkinter.CTkLabel(
                        emergency_frame,
                        text=f"🚨 {date.strftime('%Y-%m-%d %H:%M')} by {author}:",
                        font=("Arial", 11, "bold"),
                        text_color="white"
                    ).pack(anchor="w", padx=15, pady=(10, 5))
                    
                    customtkinter.CTkLabel(
                        emergency_frame,
                        text=note,
                        font=("Arial", 11),
                        text_color="white",
                        wraplength=400
                    ).pack(anchor="w", padx=15, pady=(0, 10))
                    
        except Exception as e:
            customtkinter.CTkLabel(
                history_frame,
                text=f"Error loading medical history: {str(e)}",
                font=("Arial", 12),
                text_color=self.colors['danger']
            ).pack(pady=20)

    def show_todays_patients(self):
        """Enhanced today's patients view"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="📅 Today's Patient Schedule",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        today = datetime.date.today()
        
        try:
            # Get today's patients treated by this doctor
            self.cursor.execute(
                """SELECT DISTINCT t.patient_id, p.name, COUNT(t.treatment_id) as visits
                   FROM treatments t
                   JOIN patients p ON t.patient_id = p.patient_id
                   WHERE t.doctor_id = %s AND DATE(t.date) = CURDATE()
                   GROUP BY t.patient_id, p.name
                   ORDER BY MAX(t.date) DESC
                """,
                (self.doctor_id,)
            )
            patients = self.cursor.fetchall()
            
            # Statistics
            stats_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
            stats_frame.pack(fill="x", padx=20, pady=20)
            
            customtkinter.CTkLabel(
                stats_frame,
                text=f"📊 Total Patients Treated Today: {len(patients)}",
                font=("Arial", 16, "bold"),
                text_color=self.colors['success']
            ).pack(pady=20)
            
            if not patients:
                customtkinter.CTkLabel(
                    self.content,
                    text="📋 No patients treated today yet.",
                    font=("Arial", 16),
                    text_color=self.colors['text_dark']
                ).pack(pady=50)
                return
            
            # Patient list
            patients_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['light_gray'])
            patients_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            customtkinter.CTkLabel(
                patients_frame,
                text="👥 Today's Treated Patients",
                font=("Arial", 18, "bold"),
                text_color=self.colors['text_dark']
            ).pack(pady=20)
            
            # Scrollable patient list
            patients_scroll = customtkinter.CTkScrollableFrame(patients_frame)
            patients_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            for patient_id, name, visit_count in patients:
                patient_card = customtkinter.CTkFrame(patients_scroll, fg_color=self.colors['primary'])
                patient_card.pack(fill="x", pady=10)
                
                customtkinter.CTkLabel(
                    patient_card,
                    text=f"👤 {name} (ID: {patient_id})",
                    font=("Arial", 14, "bold"),
                    text_color="white"
                ).pack(anchor="w", padx=20, pady=(15, 5))
                
                customtkinter.CTkLabel(
                    patient_card,
                    text=f"📊 Visits Today: {visit_count}",
                    font=("Arial", 12),
                    text_color="white"
                ).pack(anchor="w", padx=20, pady=(0, 15))
                
        except Exception as err:
            messagebox.showerror("❌ Database Error", f"Error loading today's patients: {str(err)}")

    def show_emergency_cases(self):
        """Enhanced emergency cases display"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="🚨 Emergency Cases Management",
            font=("Arial", 22, "bold"),
            text_color=self.colors['danger']
        ).pack(anchor="w")
        
        try:
            # Get all emergency notes
            self.cursor.execute(
                """SELECT n.patient_id, p.name, n.note, n.date, n.author
                   FROM patient_notes n
                   JOIN patients p ON n.patient_id = p.patient_id
                   WHERE n.emergency=1
                   ORDER BY n.date DESC"""
            )
            emergencies = self.cursor.fetchall()
            
            # Statistics
            stats_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
            stats_frame.pack(fill="x", padx=20, pady=20)
            
            today_count = sum(1 for e in emergencies if e[3].date() == datetime.date.today())
            total_count = len(emergencies)
            
            customtkinter.CTkLabel(
                stats_frame,
                text=f"🚨 Emergency Cases: {today_count} today | {total_count} total",
                font=("Arial", 16, "bold"),
                text_color=self.colors['danger']
            ).pack(pady=20)
            
            if not emergencies:
                customtkinter.CTkLabel(
                    self.content,
                    text="✅ No emergency cases reported.",
                    font=("Arial", 16),
                    text_color=self.colors['success']
                ).pack(pady=50)
                return
            
            # Emergency cases list
            emergency_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['light_gray'])
            emergency_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            customtkinter.CTkLabel(
                emergency_frame,
                text="🚨 Active Emergency Cases",
                font=("Arial", 18, "bold"),
                text_color=self.colors['danger']
            ).pack(pady=20)
            
            # Scrollable emergency list
            emergency_scroll = customtkinter.CTkScrollableFrame(emergency_frame)
            emergency_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            for patient_id, name, note, date, author in emergencies:
                is_today = date.date() == datetime.date.today()
                card_color = self.colors['danger'] if is_today else "#e67e22"
                
                emergency_card = customtkinter.CTkFrame(emergency_scroll, fg_color=card_color)
                emergency_card.pack(fill="x", pady=10)
                
                priority_text = "🚨 HIGH PRIORITY - " if is_today else "⚠️ "
                
                customtkinter.CTkLabel(
                    emergency_card,
                    text=f"{priority_text}{name} (ID: {patient_id})",
                    font=("Arial", 14, "bold"),
                    text_color="white"
                ).pack(anchor="w", padx=20, pady=(15, 5))
                
                customtkinter.CTkLabel(
                    emergency_card,
                    text=f"📅 {date.strftime('%Y-%m-%d %H:%M')} | 👤 Reported by: {author}",
                    font=("Arial", 11),
                    text_color="white"
                ).pack(anchor="w", padx=20, pady=2)
                
                customtkinter.CTkLabel(
                    emergency_card,
                    text=f"📝 {note}",
                    font=("Arial", 12),
                    text_color="white",
                    wraplength=500
                ).pack(anchor="w", padx=20, pady=(5, 15))
                
        except Exception as err:
            messagebox.showerror("❌ Database Error", f"Error loading emergency cases: {str(err)}")

    def show_statistics(self):
        """Medical statistics dashboard"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="📊 Medical Statistics & Analytics",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        stats_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        try:
            # Personal statistics
            doctor_id = getattr(self, 'doctor_id', 0)
            
            self.cursor.execute(
                "SELECT COUNT(DISTINCT patient_id) FROM treatments WHERE doctor_id=%s",
                (doctor_id,)
            )
            total_patients_treated = self.cursor.fetchone()[0]
            
            self.cursor.execute(
                "SELECT COUNT(*) FROM treatments WHERE doctor_id=%s",
                (doctor_id,)
            )
            total_treatments = self.cursor.fetchone()[0]
            
            # Hospital statistics
            self.cursor.execute("SELECT COUNT(*) FROM patients")
            total_hospital_patients = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM doctors")
            total_doctors = self.cursor.fetchone()[0]
            
            # Display statistics
            personal_frame = customtkinter.CTkFrame(stats_frame, fg_color=self.colors['light_blue'])
            personal_frame.pack(fill="x", padx=20, pady=20)
            
            customtkinter.CTkLabel(
                personal_frame,
                text=f"👨‍⚕️ Your Medical Practice Statistics",
                font=("Arial", 16, "bold"),
                text_color=self.colors['text_dark']
            ).pack(pady=15)
            
            personal_stats = [
                f"👥 Patients Treated: {total_patients_treated}",
                f"🩺 Total Treatments: {total_treatments}",
                f"📊 Average Treatments per Patient: {total_treatments/max(total_patients_treated, 1):.1f}"
            ]
            
            for stat in personal_stats:
                customtkinter.CTkLabel(
                    personal_frame,
                    text=stat,
                    font=("Arial", 12),
                    text_color=self.colors['text_dark']
                ).pack(anchor="w", padx=20, pady=5)
            
            # Hospital statistics
            hospital_frame = customtkinter.CTkFrame(stats_frame, fg_color=self.colors['secondary'])
            hospital_frame.pack(fill="x", padx=20, pady=20)
            
            customtkinter.CTkLabel(
                hospital_frame,
                text="🏥 Hospital Statistics",
                font=("Arial", 16, "bold"),
                text_color="white"
            ).pack(pady=15)
            
            hospital_stats = [
                f"👥 Total Hospital Patients: {total_hospital_patients}",
                f"👨‍⚕️ Total Doctors: {total_doctors}",
                f"📊 Your Patient Load: {(total_patients_treated/max(total_hospital_patients, 1)*100):.1f}%"
            ]
            
            for stat in hospital_stats:
                customtkinter.CTkLabel(
                    hospital_frame,
                    text=stat,
                    font=("Arial", 12),
                    text_color="white"
                ).pack(anchor="w", padx=20, pady=(5, 15))
                
        except Exception as e:
            customtkinter.CTkLabel(
                stats_frame,
                text=f"Error loading statistics: {str(e)}",
                font=("Arial", 14),
                text_color=self.colors['danger']
            ).pack(pady=50)

    def show_search_patient(self):
        """Patient search functionality"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="🔍 Patient Search System",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        search_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        search_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            search_frame,
            text="Search by Patient Name or ID:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        search_entry = customtkinter.CTkEntry(
            search_frame,
            placeholder_text="Enter patient name or ID...",
            width=400,
            height=35
        )
        search_entry.pack(anchor="w", padx=20, pady=(0, 20))
        
        results_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['light_gray'])
        results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        def search_patients():
            """Search for patients"""
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            query = search_entry.get().strip()
            if not query:
                customtkinter.CTkLabel(
                    results_frame,
                    text="Please enter a search term.",
                    font=("Arial", 14),
                    text_color=self.colors['text_dark']
                ).pack(pady=20)
                return
            
            try:
                # Search by name or ID
                self.cursor.execute(
                    """SELECT patient_id, name, date_of_birth, gender 
                       FROM patients 
                       WHERE name LIKE %s OR patient_id LIKE %s
                       ORDER BY name""",
                    (f"%{query}%", f"%{query}%")
                )
                results = self.cursor.fetchall()
                
                if results:
                    customtkinter.CTkLabel(
                        results_frame,
                        text=f"🔍 Search Results ({len(results)} found):",
                        font=("Arial", 16, "bold"),
                        text_color=self.colors['text_dark']
                    ).pack(pady=20)
                    
                    # Results list
                    results_scroll = customtkinter.CTkScrollableFrame(results_frame)
                    results_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                    
                    for patient_id, name, dob, gender in results:
                        result_card = customtkinter.CTkFrame(results_scroll, fg_color=self.colors['white'])
                        result_card.pack(fill="x", pady=5)
                        
                        customtkinter.CTkLabel(
                            result_card,
                            text=f"👤 {name} (ID: {patient_id})",
                            font=("Arial", 14, "bold"),
                            text_color=self.colors['text_dark']
                        ).pack(anchor="w", padx=20, pady=(15, 5))
                        
                        customtkinter.CTkLabel(
                            result_card,
                            text=f"📅 DOB: {dob} | ⚥ Gender: {gender}",
                            font=("Arial", 12),
                            text_color=self.colors['text_dark']
                        ).pack(anchor="w", padx=20, pady=(0, 15))
                else:
                    customtkinter.CTkLabel(
                        results_frame,
                        text=f"❌ No patients found matching '{query}'",
                        font=("Arial", 14),
                        text_color=self.colors['danger']
                    ).pack(pady=50)
                    
            except Exception as e:
                customtkinter.CTkLabel(
                    results_frame,
                    text=f"Error searching patients: {str(e)}",
                    font=("Arial", 14),
                    text_color=self.colors['danger']
                ).pack(pady=20)
        
        # Search button
        search_btn = customtkinter.CTkButton(
            search_frame,
            text="🔍 Search Patients",
            command=search_patients,
            height=35,
            width=150,
            font=("Arial", 12, "bold"),
            fg_color=self.colors['info']
        )
        search_btn.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Bind Enter key to search
        search_entry.bind("<Return>", lambda e: search_patients())

    def show_doctor_profile(self):
        """Display doctor profile and settings"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="👨‍⚕️ Doctor Profile & Settings",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        try:
            # Get doctor info
            self.cursor.execute(
                """SELECT firstname, lastname, national_id, qualification, specialization
                   FROM doctors WHERE firstname=%s""",
                (self.username,)
            )
            doctor_info = self.cursor.fetchone()
            
            if doctor_info:
                profile_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
                profile_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Profile header
                header_frame = customtkinter.CTkFrame(profile_frame, fg_color=self.colors['primary'])
                header_frame.pack(fill="x", padx=20, pady=20)
                
                customtkinter.CTkLabel(
                    header_frame,
                    text=f"👨‍⚕️ Dr. {doctor_info[0]} {doctor_info[1]}",
                    font=("Arial", 20, "bold"),
                    text_color="white"
                ).pack(pady=15)
                
                # Profile details
                details_frame = customtkinter.CTkFrame(profile_frame, fg_color=self.colors['light_blue'])
                details_frame.pack(fill="x", padx=20, pady=20)
                
                profile_details = [
                    ("🆔 National ID", doctor_info[2]),
                    ("🎓 Qualification", doctor_info[3]),
                    ("🩺 Specialization", doctor_info[4]),
                    ("🏥 Department", "Medical"),
                    ("📧 Email", f"{doctor_info[0].lower()}.{doctor_info[1].lower()}@qech.gov.mw")
                ]
                
                customtkinter.CTkLabel(
                    details_frame,
                    text="👤 Professional Information",
                    font=("Arial", 16, "bold"),
                    text_color=self.colors['text_dark']
                ).pack(pady=(15, 10))
                
                for label, value in profile_details:
                    customtkinter.CTkLabel(
                        details_frame,
                        text=f"{label}: {value}",
                        font=("Arial", 12),
                        text_color=self.colors['text_dark']
                    ).pack(anchor="w", padx=20, pady=5)
                
                customtkinter.CTkLabel(
                    details_frame,
                    text=" ",
                    font=("Arial", 12)
                ).pack(pady=(0, 15))
                
            else:
                customtkinter.CTkLabel(
                    self.content,
                    text="No doctor profile found. Please register.",
                    font=("Arial", 14),
                    text_color=self.colors['danger']
                ).pack(pady=50)
                
        except Exception as e:
            customtkinter.CTkLabel(
                self.content,
                text=f"Error loading profile: {str(e)}",
                font=("Arial", 14),
                text_color=self.colors['danger']
            ).pack(pady=50)

    def check_emergencies(self):
        """Enhanced emergency alert system"""
        try:
            self.cursor.execute(
                """SELECT n.patient_id, p.name, n.note, n.date, n.author
                   FROM patient_notes n
                   JOIN patients p ON n.patient_id = p.patient_id
                   WHERE n.emergency=1 AND DATE(n.date) = CURDATE()
                   ORDER BY n.date DESC"""
            )
            today_emergencies = self.cursor.fetchall()
            
            if today_emergencies:
                msg = "🚨 EMERGENCY ALERT - TODAY'S CASES!\n\n"
                for patient_id, name, note, date, author in today_emergencies:
                    msg += f"👤 Patient: {name} (ID: {patient_id})\n"
                    msg += f"📝 Note: {note}\n"
                    msg += f"🕒 Time: {date.strftime('%H:%M')}\n"
                    msg += f"👤 Reported by: {author}\n"
                    msg += "-" * 50 + "\n\n"
                
                messagebox.showwarning("🚨 Emergency Alert", msg)
                
                # Also show emergency cases page
                self.show_emergency_cases()
            else:
                messagebox.showinfo("✅ No Emergencies", "No emergency cases reported today.")
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error checking emergencies: {str(e)}")

    def logout(self):
        result = messagebox.askyesno(
            "🚪 Logout Confirmation",
            f"Are you sure you want to logout, Dr. {self.username}?\n\nAll unsaved work will be lost."
        )
        if result:
            try:
                log_action(self.username, "Doctor", "Logged out from medical system")
                self.conn.close()
            except:
                pass
            messagebox.showinfo("👋 Goodbye", f"Thank you for your service, Dr. {self.username}!")
            self.master.destroy()
            if self.on_logout:
                self.on_logout()