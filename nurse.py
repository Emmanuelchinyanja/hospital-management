import customtkinter
from tkinter import messagebox, ttk
from db_connection import get_connection, log_action
import datetime
from PIL import Image, ImageTk
import tkinter as tk

class NurseFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        
        # Color scheme for Queen Elizabeth Hospital
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
            'danger': '#e74c3c'
        }
        
        # Configure main layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Sidebar
        self.create_sidebar()
        
        # Main content area
        self.content = customtkinter.CTkFrame(self, fg_color=self.colors['light_gray'])
        self.content.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        # Footer
        self.create_footer()
        
        # Show welcome screen
        self.show_dashboard()

    def create_header(self):
        """Create professional hospital header"""
        header = customtkinter.CTkFrame(self, height=80, fg_color=self.colors['primary'])
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)
        
        # Hospital logo and title
        logo_frame = customtkinter.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)
        
        # Hospital name and logo
        customtkinter.CTkLabel(
            logo_frame,
            text="🏥 QUEEN ELIZABETH HOSPITAL",
            font=("Arial", 20, "bold"),
            text_color="white"
        ).pack(side="left")
        
        customtkinter.CTkLabel(
            logo_frame,
            text="Central Hospital • Blantyre, Malawi",
            font=("Arial", 12),
            text_color=self.colors['light_blue']
        ).pack(side="left", padx=(10, 0))
        
        # User info and time
        user_frame = customtkinter.CTkFrame(header, fg_color="transparent")
        user_frame.pack(side="right", padx=20, pady=10)
        
        current_time = datetime.datetime.now().strftime("%H:%M - %B %d, %Y")
        customtkinter.CTkLabel(
            user_frame,
            text=f"👤 Nurse {self.username}",
            font=("Arial", 14, "bold"),
            text_color="white"
        ).pack(anchor="e")
        
        customtkinter.CTkLabel(
            user_frame,
            text=current_time,
            font=("Arial", 11),
            text_color=self.colors['light_blue']
        ).pack(anchor="e")

    def create_sidebar(self):
        """Create enhanced sidebar with icons and modern styling"""
        self.sidebar = customtkinter.CTkFrame(self, width=250, fg_color=self.colors['secondary'])
        self.sidebar.grid(row=1, column=0, sticky="ns", padx=(10, 5), pady=10)
        self.sidebar.grid_propagate(False)
        
        # Sidebar title
        title_frame = customtkinter.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=(20, 30))
        
        customtkinter.CTkLabel(
            title_frame,
            text="🩺 NURSING STATION",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack()
        
        # Navigation buttons with icons
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📊 Record Vitals", self.show_record_vitals),
            ("👁️ View Patient Data", self.show_view_vitals),
            ("📝 Patient Notes", self.show_patient_notes),
            ("🚨 Emergency Cases", self.show_emergency_cases),
            ("📈 Vital Trends", self.show_vital_trends),
            ("⚙️ Settings", self.show_settings)
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
        
        # Logout button at bottom
        logout_btn = customtkinter.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            command=self.logout,
            height=50,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['danger'],
            hover_color="#c0392b",
            text_color="white"
        )
        logout_btn.pack(side="bottom", fill="x", padx=15, pady=20)

    def create_footer(self):
        """Create professional footer"""
        footer = customtkinter.CTkFrame(self, height=60, fg_color=self.colors['text_dark'])
        footer.grid(row=2, column=0, columnspan=2, sticky="ew")
        footer.grid_propagate(False)
        
        contact_frame = customtkinter.CTkFrame(footer, fg_color="transparent")
        contact_frame.pack(expand=True)
        
        customtkinter.CTkLabel(
            contact_frame,
            text="📞 Emergency: +265 1 871 911 | 📧 nursing@qech.gov.mw | 🌐 www.qech.gov.mw",
            font=("Arial", 11),
            text_color="white"
        ).pack(pady=5)
        
        customtkinter.CTkLabel(
            contact_frame,
            text="© 2025 Queen Elizabeth Central Hospital • Licensed Healthcare Management System",
            font=("Arial", 10),
            text_color="#bdc3c7"
        ).pack()

    def clear_content(self):
        """Clear main content area"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        """Enhanced dashboard with statistics and quick actions"""
        self.clear_content()
        
        # Dashboard title
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text=f"Welcome back, Nurse {self.username}! 👋",
            font=("Arial", 24, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        customtkinter.CTkLabel(
            title_frame,
            text="Nursing Dashboard - Queen Elizabeth Central Hospital",
            font=("Arial", 14),
            text_color="#7f8c8d"
        ).pack(anchor="w", pady=(5, 0))
        
        # Statistics cards
        stats_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        # Get statistics from database
        try:
            # Total patients
            self.cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = self.cursor.fetchone()[0]
            
            # Patients with vitals today
            self.cursor.execute(
                "SELECT COUNT(DISTINCT patient_id) FROM treatments WHERE DATE(date) = CURDATE()"
            )
            vitals_today = self.cursor.fetchone()[0]
            
            # Emergency cases
            self.cursor.execute(
                "SELECT COUNT(*) FROM patient_notes WHERE emergency = TRUE AND DATE(date) = CURDATE()"
            )
            emergency_cases = self.cursor.fetchone()[0]
            
        except:
            total_patients = vitals_today = emergency_cases = 0
        
        # Create stat cards
        stats = [
            ("👥 Total Patients", total_patients, self.colors['primary']),
            ("📊 Vitals Recorded Today", vitals_today, self.colors['success']),
            ("🚨 Emergency Cases", emergency_cases, self.colors['danger']),
            ("🩺 Active Nursing Staff", "24/7", self.colors['secondary'])
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = customtkinter.CTkFrame(stats_frame, fg_color=color, width=200, height=120)
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
            text="⚡ Quick Actions",
            font=("Arial", 18, "bold"),
            text_color=self.colors['text_dark']
        ).pack(pady=20)
        
        # Quick action buttons
        quick_buttons_frame = customtkinter.CTkFrame(actions_frame, fg_color="transparent")
        quick_buttons_frame.pack(expand=True, fill="both", padx=40, pady=20)
        
        quick_actions = [
            ("📊 Record New Vitals", self.show_record_vitals, self.colors['primary']),
            ("👁️ View Patient Data", self.show_view_vitals, self.colors['secondary']),
            ("🚨 Emergency Alert", self.show_emergency_cases, self.colors['danger']),
            ("📝 Add Patient Note", self.show_patient_notes, self.colors['warning'])
        ]
        
        for i, (text, command, color) in enumerate(quick_actions):
            btn = customtkinter.CTkButton(
                quick_buttons_frame,
                text=text,
                command=command,
                width=200,
                height=60,
                font=("Arial", 14, "bold"),
                fg_color=color,
                hover_color=color
            )
            btn.grid(row=i//2, column=i%2, padx=20, pady=15, sticky="ew")

    def show_record_vitals(self):
        """Enhanced vitals recording with better UX"""
        self.clear_content()
        
        # Title
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="📊 Record Patient Vitals",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        # Main form
        form_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Patient selection
        patient_frame = customtkinter.CTkFrame(form_frame, fg_color="transparent")
        patient_frame.pack(fill="x", padx=30, pady=20)
        
        customtkinter.CTkLabel(
            patient_frame,
            text="👤 Select Patient:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", pady=(0, 5))
        
        # Get patients (remove age if not in your table)
        self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
        patients = self.cursor.fetchall()

        if not patients:
            customtkinter.CTkLabel(
                form_frame,
                text="❌ No patients found in the system.",
                font=("Arial", 16),
                text_color=self.colors['danger']
            ).pack(pady=50)
            return

        patient_combo = customtkinter.CTkComboBox(
            patient_frame,
            values=[f"{p[0]} - {p[1]}" for p in patients],
            width=400,
            height=35,
            font=("Arial", 12),
            command=lambda _: show_vitals_form()
        )
        patient_combo.pack(fill="x", pady=(0, 10))

        # Vitals input section (initially hidden)
        vitals_frame = customtkinter.CTkFrame(form_frame, fg_color=self.colors['light_gray'])
        # Don't pack yet

        # Input fields with labels
        inputs = {}
        vitals_data = [
            ("blood_pressure", "🫀 Blood Pressure", "e.g., 120/80 mmHg"),
            ("temperature", "🌡️ Temperature", "e.g., 36.5 °C"),
            ("weight", "⚖️ Weight", "e.g., 70.5 kg"),
            ("heart_rate", "💓 Heart Rate", "e.g., 72 bpm"),
            ("notes", "📝 Additional Notes", "Any observations...")
        ]

        for key, label, placeholder in vitals_data:
            field_frame = customtkinter.CTkFrame(vitals_frame, fg_color="transparent")
            field_frame.pack(fill="x", padx=20, pady=10)
            
            customtkinter.CTkLabel(
                field_frame,
                text=label,
                font=("Arial", 12, "bold"),
                text_color=self.colors['text_dark']
            ).pack(anchor="w")
            
            if key == "notes":
                entry = customtkinter.CTkTextbox(field_frame, height=80, font=("Arial", 11))
            else:
                entry = customtkinter.CTkEntry(
                    field_frame,
                    placeholder_text=placeholder,
                    height=35,
                    font=("Arial", 11)
                )
            entry.pack(fill="x", pady=(5, 0))
            inputs[key] = entry

        # Mode selection
        mode_frame = customtkinter.CTkFrame(vitals_frame, fg_color="transparent")
        mode_frame.pack(fill="x", padx=30, pady=20)
        
        mode_var = customtkinter.StringVar(value="add")
        
        customtkinter.CTkLabel(
            mode_frame,
            text="📋 Recording Mode:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", pady=(0, 10))
        
        radio_frame = customtkinter.CTkFrame(mode_frame, fg_color="transparent")
        radio_frame.pack(fill="x")
        
        add_radio = customtkinter.CTkRadioButton(
            radio_frame,
            text="➕ Add New Record",
            variable=mode_var,
            value="add",
            font=("Arial", 12)
        )
        add_radio.pack(side="left", padx=(0, 30))
        
        update_radio = customtkinter.CTkRadioButton(
            radio_frame,
            text="🔄 Update Latest Record",
            variable=mode_var,
            value="update",
            font=("Arial", 12)
        )
        update_radio.pack(side="left")
        
        # Submit button
        submit_btn = customtkinter.CTkButton(
            vitals_frame,
            text="💾 Save Vital Signs",
            command=lambda: self.submit_vitals(patient_combo, inputs, mode_var),
            height=50,
            width=200,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['success'],
            hover_color="#219a52"
        )
        submit_btn.pack(pady=30)

        def show_vitals_form():
            # Only show the vitals form after a patient is selected
            if not hasattr(vitals_frame, '_is_packed') or not vitals_frame._is_packed:
                vitals_frame.pack(fill="x", padx=30, pady=20)
                vitals_frame._is_packed = True

        # Optionally, show the form for the first patient by default
        if patients:
            patient_combo.set(f"{patients[0][0]} - {patients[0][1]}")
            show_vitals_form()

    def submit_vitals(self, patient_combo, inputs, mode_var):
        """Submit vital signs with enhanced validation"""
        selection = patient_combo.get()
        if not selection:
            messagebox.showerror("❌ Error", "Please select a patient.")
            return
        
        pid = selection.split(" - ")[0].strip()
        try:
            pid = int(pid)
        except ValueError:
            messagebox.showerror("❌ Error", "Invalid patient ID selected.")
            return
        
        # Get input values
        bp = inputs["blood_pressure"].get().strip()
        temp = inputs["temperature"].get().strip()
        weight = inputs["weight"].get().strip()
        heart_rate = inputs["heart_rate"].get().strip()
        
        if inputs["notes"].__class__.__name__ == "CTkTextbox":
            notes = inputs["notes"].get("1.0", "end-1c").strip()
        else:
            notes = inputs["notes"].get().strip()
        
        # Validation
        if not any([bp, temp, weight, heart_rate]):
            messagebox.showerror("❌ Error", "Please enter at least one vital sign.")
            return
        
        # Validate numeric fields
        try:
            temp_val = float(temp) if temp else None
            weight_val = float(weight) if weight else None
            hr_val = int(heart_rate) if heart_rate else None
        except ValueError:
            messagebox.showerror("❌ Error", "Temperature and Weight must be valid numbers.")
            return
        
        # Check patient exists
        self.cursor.execute("SELECT name FROM patients WHERE patient_id=%s", (pid,))
        patient = self.cursor.fetchone()
        if not patient:
            messagebox.showerror("❌ Error", "Selected patient does not exist.")
            return
        
        try:
            if mode_var.get() == "add":
                self.cursor.execute(
                    """INSERT INTO treatments (patient_id, blood_pressure, temperature, weight, heart_rate, notes) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (pid, bp or None, temp_val, weight_val, hr_val, notes or None)
                )
                self.conn.commit()
                messagebox.showinfo("✅ Success", f"Vitals recorded successfully for {patient[0]}!")
                log_action(self.username, "Nurse", f"Added vitals for patient ID: {pid}")
            else:  # update latest
                self.cursor.execute(
                    "SELECT treatment_id FROM treatments WHERE patient_id=%s ORDER BY date DESC LIMIT 1",
                    (pid,)
                )
                latest = self.cursor.fetchone()
                if not latest:
                    messagebox.showerror("❌ Error", "No previous record to update for this patient.")
                    return
                
                self.cursor.execute(
                    """UPDATE treatments SET blood_pressure=%s, temperature=%s, weight=%s, 
                       heart_rate=%s, notes=%s WHERE treatment_id=%s""",
                    (bp or None, temp_val, weight_val, hr_val, notes or None, latest[0])
                )
                self.conn.commit()
                messagebox.showinfo("✅ Success", f"Latest vitals updated for {patient[0]}!")
                log_action(self.username, "Nurse", f"Updated latest vitals for patient ID: {pid}")
            
            # Clear form
            for key, entry in inputs.items():
                if entry.__class__.__name__ == "CTkTextbox":
                    entry.delete("1.0", "end")
                else:
                    entry.delete(0, 'end')
                    
        except Exception as err:
            messagebox.showerror("❌ Database Error", f"Error: {err}")

    def show_view_vitals(self):
        """Enhanced patient vitals viewer with charts and history"""
        self.clear_content()
        
        # Title
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="👁️ Patient Vitals & History",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        # Patient selection
        selection_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        selection_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Get patients
        self.cursor.execute("SELECT patient_id, name, age FROM patients ORDER BY name")
        patients = self.cursor.fetchall()
        
        if not patients:
            customtkinter.CTkLabel(
                self.content,
                text="❌ No patients found in the system.",
                font=("Arial", 16),
                text_color=self.colors['danger']
            ).pack(pady=50)
            return
        
        customtkinter.CTkLabel(
            selection_frame,
            text="👤 Select Patient:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        patient_combo = customtkinter.CTkComboBox(
            selection_frame,
            values=[f"{p[0]} - {p[1]} (Age: {p[2]})" for p in patients],
            width=400,
            height=35,
            font=("Arial", 12)
        )
        patient_combo.pack(anchor="w", padx=20, pady=(0, 20))
        
        # Vitals display area
        vitals_display = customtkinter.CTkFrame(self.content, fg_color=self.colors['light_gray'])
        vitals_display.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        def display_patient_vitals():
            for widget in vitals_display.winfo_children():
                widget.destroy()
                
            selection = patient_combo.get()
            if not selection:
                return
                
            pid = selection.split(" - ")[0]
            patient_name = selection.split(" - ")[1].split(" (")[0]
            
            # Patient info header
            info_frame = customtkinter.CTkFrame(vitals_display, fg_color=self.colors['primary'])
            info_frame.pack(fill="x", padx=20, pady=20)
            
            customtkinter.CTkLabel(
                info_frame,
                text=f"📋 {patient_name} - Patient ID: {pid}",
                font=("Arial", 16, "bold"),
                text_color="white"
            ).pack(pady=15)
            
            # Get vitals
            self.cursor.execute(
                """SELECT blood_pressure, temperature, weight, heart_rate, notes, date 
                   FROM treatments WHERE patient_id=%s 
                   ORDER BY date DESC LIMIT 10""",
                (pid,)
            )
            vitals = self.cursor.fetchall()
            
            if not vitals:
                customtkinter.CTkLabel(
                    vitals_display,
                    text="📊 No vitals recorded for this patient yet.",
                    font=("Arial", 14),
                    text_color=self.colors['text_dark']
                ).pack(pady=50)
                return
            
            # Latest vitals summary
            latest = vitals[0]
            summary_frame = customtkinter.CTkFrame(vitals_display, fg_color=self.colors['white'])
            summary_frame.pack(fill="x", padx=20, pady=10)
            
            customtkinter.CTkLabel(
                summary_frame,
                text="🩺 Latest Vital Signs",
                font=("Arial", 16, "bold"),
                text_color=self.colors['text_dark']
            ).pack(pady=(15, 10))
            
            # Create vital signs grid
            vitals_grid = customtkinter.CTkFrame(summary_frame, fg_color="transparent")
            vitals_grid.pack(fill="x", padx=20, pady=10)
            
            vital_info = [
                ("🫀 Blood Pressure", latest[0] or "Not recorded"),
                ("🌡️ Temperature", f"{latest[1]}°C" if latest[1] else "Not recorded"),
                ("⚖️ Weight", f"{latest[2]} kg" if latest[2] else "Not recorded"),
                ("💓 Heart Rate", f"{latest[3]} bpm" if latest[3] else "Not recorded")
            ]
            
            for i, (label, value) in enumerate(vital_info):
                row = i // 2
                col = i % 2
                
                vital_card = customtkinter.CTkFrame(vitals_grid, fg_color=self.colors['light_blue'])
                vital_card.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
                
                customtkinter.CTkLabel(
                    vital_card,
                    text=label,
                    font=("Arial", 12, "bold"),
                    text_color=self.colors['text_dark']
                ).pack(pady=(10, 0))
                
                customtkinter.CTkLabel(
                    vital_card,
                    text=str(value),
                    font=("Arial", 14),
                    text_color=self.colors['primary']
                ).pack(pady=(0, 10))
            
            vitals_grid.grid_columnconfigure(0, weight=1)
            vitals_grid.grid_columnconfigure(1, weight=1)
            
            # Date and notes
            if latest[4]:  # If there are notes
                customtkinter.CTkLabel(
                    summary_frame,
                    text=f"📝 Notes: {latest[4]}",
                    font=("Arial", 11),
                    text_color=self.colors['text_dark']
                ).pack(anchor="w", padx=20, pady=(0, 10))
            
            customtkinter.CTkLabel(
                summary_frame,
                text=f"📅 Last Updated: {latest[5]}",
                font=("Arial", 11, "italic"),
                text_color="#7f8c8d"
            ).pack(anchor="w", padx=20, pady=(0, 15))
            
            # History
            if len(vitals) > 1:
                history_frame = customtkinter.CTkFrame(vitals_display, fg_color=self.colors['white'])
                history_frame.pack(fill="both", expand=True, padx=20, pady=10)
                
                customtkinter.CTkLabel(
                    history_frame,
                    text="📈 Vitals History",
                    font=("Arial", 16, "bold"),
                    text_color=self.colors['text_dark']
                ).pack(pady=(15, 10))
                
                # Create scrollable history
                history_scroll = customtkinter.CTkScrollableFrame(
                    history_frame,
                    fg_color=self.colors['light_gray']
                )
                history_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                
                for i, vital in enumerate(vitals[1:], 1):
                    record_frame = customtkinter.CTkFrame(history_scroll, fg_color="white")
                    record_frame.pack(fill="x", pady=5)
                    
                    date_str = vital[5].strftime("%Y-%m-%d %H:%M") if vital[5] else "Unknown"
                    
                    record_text = f"#{i+1} - {date_str}\n"
                    if vital[0]: record_text += f"BP: {vital[0]}, "
                    if vital[1]: record_text += f"Temp: {vital[1]}°C, "
                    if vital[2]: record_text += f"Weight: {vital[2]}kg, "
                    if vital[3]: record_text += f"HR: {vital[3]}bpm"
                    
                    customtkinter.CTkLabel(
                        record_frame,
                        text=record_text.rstrip(", "),
                        font=("Arial", 11),
                        text_color=self.colors['text_dark'],
                        justify="left"
                    ).pack(anchor="w", padx=15, pady=10)
        
        # Bind selection event
        patient_combo.bind("<<ComboboxSelected>>", lambda e: display_patient_vitals())
        
        # Set initial selection
        if patients:
            patient_combo.set(f"{patients[0][0]} - {patients[0][1]} (Age: {patients[0][2]})")
            display_patient_vitals()

    def show_patient_notes(self):
        """Enhanced patient notes interface"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="📝 Patient Notes & Observations",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        # Main content
        main_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Patient selection
        selection_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        selection_frame.pack(fill="x", padx=20, pady=20)
        
        self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
        patients = self.cursor.fetchall()
        
        if not patients:
            customtkinter.CTkLabel(
                main_frame,
                text="❌ No patients found.",
                font=("Arial", 16),
                text_color=self.colors['danger']
            ).pack(pady=50)
            return
        
        customtkinter.CTkLabel(
            selection_frame,
            text="👤 Select Patient:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", pady=(0, 5))
        
        patient_combo = customtkinter.CTkComboBox(
            selection_frame,
            values=[f"{p[0]} - {p[1]}" for p in patients],
            width=400,
            height=35
        )
        patient_combo.pack(anchor="w", pady=(0, 10))
        
        # Note input
        note_frame = customtkinter.CTkFrame(main_frame, fg_color=self.colors['light_gray'])
        note_frame.pack(fill="x", padx=20, pady=10)
        
        customtkinter.CTkLabel(
            note_frame,
            text="✍️ Write Note:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        notes_text = customtkinter.CTkTextbox(
            note_frame,
            height=120,
            font=("Arial", 12),
            placeholder_text="Enter your observations, care notes, or patient updates here..."
        )
        notes_text.pack(fill="x", padx=20, pady=(0, 20))
        
        # Options
        options_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        options_frame.pack(fill="x", padx=20, pady=10)
        
        emergency_var = customtkinter.BooleanVar()
        emergency_check = customtkinter.CTkCheckBox(
            options_frame,
            text="🚨 Mark as Emergency/Priority",
            variable=emergency_var,
            font=("Arial", 12, "bold"),
            text_color=self.colors['danger']
        )
        emergency_check.pack(anchor="w")
        
        # Save button
        save_btn = customtkinter.CTkButton(
            main_frame,
            text="💾 Save Note",
            command=lambda: self.save_patient_note(patient_combo, notes_text, emergency_var.get()),
            height=45,
            width=200,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['success']
        )
        save_btn.pack(pady=20)
        
        # Recent notes display
        recent_frame = customtkinter.CTkFrame(main_frame, fg_color=self.colors['light_gray'])
        recent_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        customtkinter.CTkLabel(
            recent_frame,
            text="📋 Recent Notes",
            font=("Arial", 16, "bold"),
            text_color=self.colors['text_dark']
        ).pack(pady=(20, 10))
        
        # Show recent notes
        try:
            self.cursor.execute(
                """SELECT pn.note, pn.date, p.name, pn.emergency 
                   FROM patient_notes pn 
                   JOIN patients p ON pn.patient_id = p.patient_id 
                   ORDER BY pn.date DESC LIMIT 5"""
            )
            recent_notes = self.cursor.fetchall()
            
            if recent_notes:
                notes_scroll = customtkinter.CTkScrollableFrame(recent_frame, height=200)
                notes_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                
                for note, date, patient_name, is_emergency in recent_notes:
                    note_card = customtkinter.CTkFrame(
                        notes_scroll, 
                        fg_color=self.colors['danger'] if is_emergency else "white"
                    )
                    note_card.pack(fill="x", pady=5)
                    
                    emergency_text = "🚨 EMERGENCY - " if is_emergency else ""
                    header_text = f"{emergency_text}{patient_name} - {date.strftime('%Y-%m-%d %H:%M')}"
                    
                    customtkinter.CTkLabel(
                        note_card,
                        text=header_text,
                        font=("Arial", 11, "bold"),
                        text_color="white" if is_emergency else self.colors['text_dark']
                    ).pack(anchor="w", padx=15, pady=(10, 5))
                    
                    customtkinter.CTkLabel(
                        note_card,
                        text=note,
                        font=("Arial", 10),
                        text_color="white" if is_emergency else "#555",
                        wraplength=400,
                        justify="left"
                    ).pack(anchor="w", padx=15, pady=(0, 10))
            
        except Exception as e:
            customtkinter.CTkLabel(
                recent_frame,
                text="No recent notes available.",
                font=("Arial", 12),
                text_color="#777"
            ).pack(pady=20)

    def show_emergency_cases(self):
        """Emergency cases dashboard"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="🚨 Emergency Cases Dashboard",
            font=("Arial", 22, "bold"),
            text_color=self.colors['danger']
        ).pack(anchor="w")
        
        # Emergency stats
        stats_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        try:
            # Today's emergencies
            self.cursor.execute(
                "SELECT COUNT(*) FROM patient_notes WHERE emergency = TRUE AND DATE(date) = CURDATE()"
            )
            today_emergencies = self.cursor.fetchone()[0]
            
            # This week's emergencies
            self.cursor.execute(
                "SELECT COUNT(*) FROM patient_notes WHERE emergency = TRUE AND date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
            )
            week_emergencies = self.cursor.fetchone()[0]
            
        except:
            today_emergencies = week_emergencies = 0
        
        customtkinter.CTkLabel(
            stats_frame,
            text=f"📊 Today: {today_emergencies} emergencies | This Week: {week_emergencies} emergencies",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(pady=20)
        
        # Emergency cases list
        emergency_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['light_gray'])
        emergency_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        customtkinter.CTkLabel(
            emergency_frame,
            text="🚨 Active Emergency Cases",
            font=("Arial", 18, "bold"),
            text_color=self.colors['danger']
        ).pack(pady=20)
        
        try:
            self.cursor.execute(
                """SELECT pn.note, pn.date, p.name, p.patient_id
                   FROM patient_notes pn 
                   JOIN patients p ON pn.patient_id = p.patient_id 
                   WHERE pn.emergency = TRUE 
                   ORDER BY pn.date DESC LIMIT 10"""
            )
            emergencies = self.cursor.fetchall()
            
            if emergencies:
                emergency_scroll = customtkinter.CTkScrollableFrame(emergency_frame)
                emergency_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                
                for note, date, patient_name, patient_id in emergencies:
                    emergency_card = customtkinter.CTkFrame(emergency_scroll, fg_color=self.colors['danger'])
                    emergency_card.pack(fill="x", pady=10)
                    
                    customtkinter.CTkLabel(
                        emergency_card,
                        text=f"🚨 EMERGENCY - {patient_name} (ID: {patient_id})",
                        font=("Arial", 14, "bold"),
                        text_color="white"
                    ).pack(anchor="w", padx=20, pady=(15, 5))
                    
                    customtkinter.CTkLabel(
                        emergency_card,
                        text=f"📅 {date.strftime('%Y-%m-%d %H:%M')}",
                        font=("Arial", 11),
                        text_color="white"
                    ).pack(anchor="w", padx=20)
                    
                    customtkinter.CTkLabel(
                        emergency_card,
                        text=note,
                        font=("Arial", 12),
                        text_color="white",
                        wraplength=500,
                        justify="left"
                    ).pack(anchor="w", padx=20, pady=(5, 15))
            else:
                customtkinter.CTkLabel(
                    emergency_frame,
                    text="✅ No active emergency cases.",
                    font=("Arial", 16),
                    text_color=self.colors['success']
                ).pack(pady=50)
                
        except Exception as e:
            customtkinter.CTkLabel(
                emergency_frame,
                text="Error loading emergency cases.",
                font=("Arial", 14),
                text_color=self.colors['danger']
            ).pack(pady=50)

    def show_vital_trends(self):
        """Vital signs trends and analytics"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="📈 Vital Signs Trends & Analytics",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        # Patient selection for trends
        selection_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        selection_frame.pack(fill="x", padx=20, pady=20)
        
        self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
        patients = self.cursor.fetchall()
        
        if not patients:
            return
        
        customtkinter.CTkLabel(
            selection_frame,
            text="👤 Select Patient for Trend Analysis:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        patient_combo = customtkinter.CTkComboBox(
            selection_frame,
            values=[f"{p[0]} - {p[1]}" for p in patients],
            width=400,
            height=35,
            command=lambda _: show_trends()  # This ensures show_trends runs on every selection
        )
        patient_combo.pack(anchor="w", padx=20, pady=(0, 20))
        
        trends_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['light_gray'])
        trends_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        def show_trends():
            for widget in trends_frame.winfo_children():
                widget.destroy()
                
            selection = patient_combo.get()
            if not selection:
                return
                
            pid = selection.split(" - ")[0]
            patient_name = selection.split(" - ")[1]
            
            customtkinter.CTkLabel(
                trends_frame,
                text=f"📊 Vital Trends for {patient_name}",
                font=("Arial", 18, "bold"),
                text_color=self.colors['text_dark']
            ).pack(pady=20)
            
            try:
                self.cursor.execute(
                    """SELECT temperature, weight, date 
                       FROM treatments WHERE patient_id=%s 
                       AND (temperature IS NOT NULL OR weight IS NOT NULL)
                       ORDER BY date DESC LIMIT 10""",
                    (pid,)
                )
                vitals = self.cursor.fetchall()
                
                if vitals:
                    trend_scroll = customtkinter.CTkScrollableFrame(trends_frame)
                    trend_scroll.pack(fill="both", expand=True, padx=20, pady=20)
                    
                    for i, (temp, weight, date) in enumerate(vitals):
                        trend_card = customtkinter.CTkFrame(trend_scroll, fg_color="white")
                        trend_card.pack(fill="x", pady=5)
                        
                        trend_text = f"📅 {date.strftime('%Y-%m-%d')}: "
                        if temp: trend_text += f"🌡️ {temp}°C "
                        if weight: trend_text += f"⚖️ {weight}kg"
                        
                        customtkinter.CTkLabel(
                            trend_card,
                            text=trend_text,
                            font=("Arial", 12),
                            text_color=self.colors['text_dark']
                        ).pack(anchor="w", padx=15, pady=10)
                        
                        # Simple trend indicators
                        if i < len(vitals) - 1:
                            prev_temp = vitals[i+1][0]
                            prev_weight = vitals[i+1][1]
                            
                            indicators = []
                            if temp and prev_temp:
                                if temp > prev_temp:
                                    indicators.append("🌡️↗️ Temp Rising")
                                elif temp < prev_temp:
                                    indicators.append("🌡️↘️ Temp Falling")
                            
                            if weight and prev_weight:
                                if weight > prev_weight:
                                    indicators.append("⚖️↗️ Weight Up")
                                elif weight < prev_weight:
                                    indicators.append("⚖️↘️ Weight Down")
                            
                            if indicators:
                                customtkinter.CTkLabel(
                                    trend_card,
                                    text=" | ".join(indicators),
                                    font=("Arial", 10, "italic"),
                                    text_color="#666"
                                ).pack(anchor="w", padx=15, pady=(0, 10))
                else:
                    customtkinter.CTkLabel(
                        trends_frame,
                        text="📊 No vital signs data available for trend analysis.",
                        font=("Arial", 14),
                        text_color="#666"
                    ).pack(pady=50)
                    
            except Exception as e:
                customtkinter.CTkLabel(
                    trends_frame,
                    text="Error loading trend data.",
                    font=("Arial", 14),
                    text_color=self.colors['danger']
                ).pack(pady=50)
        
        if patients:
            patient_combo.set(f"{patients[0][0]} - {patients[0][1]}")
            show_trends()

    def show_settings(self):
        """Settings and preferences"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="⚙️ Nursing Station Settings",
            font=("Arial", 22, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        settings_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # User info
        info_frame = customtkinter.CTkFrame(settings_frame, fg_color=self.colors['light_blue'])
        info_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            info_frame,
            text=f"👤 Current User: Nurse {self.username}",
            font=("Arial", 16, "bold"),
            text_color=self.colors['text_dark']
        ).pack(pady=15)
        
        customtkinter.CTkLabel(
            info_frame,
            text=f"🏥 Department: Nursing Station",
            font=("Arial", 14),
            text_color=self.colors['text_dark']
        ).pack(pady=(0, 15))
        
        # Quick stats
        stats_frame = customtkinter.CTkFrame(settings_frame, fg_color=self.colors['light_gray'])
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            stats_frame,
            text="📊 Your Activity Today",
            font=("Arial", 16, "bold"),
            text_color=self.colors['text_dark']
        ).pack(pady=(15, 10))
        
        try:
            # Count activities by this nurse today
            self.cursor.execute(
                "SELECT COUNT(*) FROM audit_log WHERE username=%s AND DATE(timestamp) = CURDATE()",
                (self.username,)
            )
            today_actions = self.cursor.fetchone()[0]
            
            customtkinter.CTkLabel(
                stats_frame,
                text=f"✅ Actions Performed Today: {today_actions}",
                font=("Arial", 12),
                text_color=self.colors['text_dark']
            ).pack(pady=(0, 15))
            
        except:
            customtkinter.CTkLabel(
                stats_frame,
                text="📊 Activity tracking unavailable",
                font=("Arial", 12),
                text_color="#666"
            ).pack(pady=(0, 15))
        
        # System info
        system_frame = customtkinter.CTkFrame(settings_frame, fg_color=self.colors['primary'])
        system_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            system_frame,
            text="🏥 Queen Elizabeth Central Hospital",
            font=("Arial", 16, "bold"),
            text_color="white"
        ).pack(pady=(15, 5))
        
        customtkinter.CTkLabel(
            system_frame,
            text="Hospital Management System v2.0",
            font=("Arial", 12),
            text_color="white"
        ).pack(pady=(0, 15))

    def save_patient_note(self, patient_combo, notes_entry, is_emergency):
        """Enhanced save patient note with better validation"""
        selection = patient_combo.get()
        
        if notes_entry.__class__.__name__ == "CTkTextbox":
            note = notes_entry.get("1.0", "end-1c").strip()
        else:
            note = notes_entry.get().strip()
            
        if not selection or not note:
            messagebox.showerror("❌ Error", "Please select a patient and write a note.")
            return
            
        pid = selection.split(" - ")[0]
        patient_name = selection.split(" - ")[1]
        
        try:
            self.cursor.execute(
                "INSERT INTO patient_notes (patient_id, note, author, date, emergency) VALUES (%s, %s, %s, %s, %s)",
                (pid, note, self.username, datetime.datetime.now(), is_emergency)
            )
            self.conn.commit()
            
            emergency_text = " (EMERGENCY)" if is_emergency else ""
            messagebox.showinfo(
                "✅ Success", 
                f"Note saved for {patient_name}{emergency_text}!"
            )
            
            # Clear the text box
            if notes_entry.__class__.__name__ == "CTkTextbox":
                notes_entry.delete("1.0", "end")
            else:
                notes_entry.delete(0, 'end')
                
            log_action(self.username, "Nurse", f"Added note for patient ID: {pid} (Emergency: {is_emergency})")
            
        except Exception as err:
            messagebox.showerror("❌ Database Error", f"Error: {err}")

    def logout(self):
        """Enhanced logout with confirmation"""
        result = messagebox.askyesno(
            "🚪 Logout Confirmation",
            f"Are you sure you want to logout, Nurse {self.username}?\n\nAll unsaved work will be lost."
        )
        
        if result:
            try:
                log_action(self.username, "Nurse", "Logged out from system")
                self.conn.close()
            except:
                pass
            
            messagebox.showinfo("👋 Goodbye", f"Thank you for your service, Nurse {self.username}!")
            self.master.destroy()