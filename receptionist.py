import customtkinter
from tkinter import messagebox, ttk
from tkinter import *
from db_connection import get_connection, log_action
import datetime
from PIL import Image
import os

class ReceptionistFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.on_logout = None  # Add this line
        self.current_view = "dashboard"
        
        # Configure colors
        self.primary_color = "#1e3a5f"
        self.secondary_color = "#2d4a6b"
        self.accent_color = "#0066cc"
        self.success_color = "#28a745"
        self.warning_color = "#ffc107"
        self.danger_color = "#dc3545"
        self.light_bg = "#f8f9fa"
        
        self.setup_layout()
        self.show_dashboard()

    def setup_layout(self):
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Enhanced Sidebar
        self.sidebar = customtkinter.CTkFrame(self, width=280, fg_color=self.primary_color, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        
        # Sidebar Header
        header_frame = customtkinter.CTkFrame(self.sidebar, fg_color=self.secondary_color, height=100)
        header_frame.pack(fill="x", padx=10, pady=(20, 15))
        header_frame.pack_propagate(False)
        
        # Profile section
        profile_frame = customtkinter.CTkFrame(header_frame, fg_color="transparent")
        profile_frame.pack(expand=True, fill="both", padx=15, pady=10)
        
        customtkinter.CTkLabel(
            profile_frame, 
            text="👩‍💼", 
            font=("Arial", 32)
        ).pack()
        
        customtkinter.CTkLabel(
            profile_frame, 
            text=f"Receptionist", 
            font=("Arial", 14, "bold"), 
            text_color="white"
        ).pack()
        
        customtkinter.CTkLabel(
            profile_frame, 
            text=f"{self.username}", 
            font=("Arial", 12), 
            text_color="#a8c8ec"
        ).pack()

        # Navigation Buttons
        nav_frame = customtkinter.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=15, pady=10)
        
        # Navigation button style
        button_config = {
            "height": 45,
            "font": ("Arial", 13, "bold"),
            "corner_radius": 8,
            "fg_color": "transparent",
            "hover_color": self.secondary_color,
            "text_color": "white",
            "anchor": "w"
        }
        
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("➕ Register Patient", self.show_register_patient),
            ("📋 View Patients", self.show_view_patients),
            ("🔍 Search Patients", self.show_search_patients),
            ("📊 Daily Reports", self.show_daily_reports),
            ("⚙️ Quick Actions", self.show_quick_actions)
        ]
        
        for text, command in nav_items:
            btn = customtkinter.CTkButton(nav_frame, text=text, command=command, **button_config)
            btn.pack(fill="x", pady=3)
            self.nav_buttons[text] = btn

        # Quick stats
        stats_frame = customtkinter.CTkFrame(self.sidebar, fg_color=self.secondary_color, height=120)
        stats_frame.pack(fill="x", padx=15, pady=15)
        stats_frame.pack_propagate(False)
        
        customtkinter.CTkLabel(
            stats_frame, 
            text="📈 Today's Summary", 
            font=("Arial", 12, "bold"), 
            text_color="white"
        ).pack(pady=(10, 5))
        
        try:
            # Get today's registrations
            today = datetime.date.today()
            self.cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(date_registered) = %s", (today,))
            today_count = self.cursor.fetchone()[0]
            
            # Get total patients
            self.cursor.execute("SELECT COUNT(*) FROM patients")
            total_count = self.cursor.fetchone()[0]
            
            customtkinter.CTkLabel(
                stats_frame, 
                text=f"New Patients: {today_count}", 
                font=("Arial", 11), 
                text_color="#a8c8ec"
            ).pack()
            
            customtkinter.CTkLabel(
                stats_frame, 
                text=f"Total Patients: {total_count}", 
                font=("Arial", 11), 
                text_color="#a8c8ec"
            ).pack()
            
        except Exception as e:
            customtkinter.CTkLabel(
                stats_frame, 
                text="Stats unavailable", 
                font=("Arial", 11), 
                text_color="#a8c8ec"
            ).pack()

        # Logout button
        logout_btn = customtkinter.CTkButton(
            self.sidebar, 
            text="🚪 Logout", 
            command=self.logout,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color=self.danger_color,
            hover_color="#c82333",
            corner_radius=8
        )
        logout_btn.pack(side="bottom", fill="x", padx=15, pady=20)

        # Main content area
        self.content = customtkinter.CTkFrame(self, fg_color=self.light_bg, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")

    def update_nav_buttons(self, active_button):
        """Update navigation button styles"""
        for text, btn in self.nav_buttons.items():
            if text == active_button:
                btn.configure(fg_color=self.accent_color)
            else:
                btn.configure(fg_color="transparent")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def create_header(self, title, subtitle=""):
        """Create a consistent header for all pages"""
        header_frame = customtkinter.CTkFrame(self.content, fg_color=self.primary_color, height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        header_frame.pack_propagate(False)
        
        header_content = customtkinter.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(expand=True, fill="both", padx=20, pady=15)
        
        customtkinter.CTkLabel(
            header_content, 
            text=title, 
            font=("Arial", 24, "bold"), 
            text_color="white"
        ).pack(anchor="w")
        
        if subtitle:
            customtkinter.CTkLabel(
                header_content, 
                text=subtitle, 
                font=("Arial", 12), 
                text_color="#a8c8ec"
            ).pack(anchor="w")

    def show_dashboard(self):
        self.clear_content()
        self.current_view = "dashboard"
        self.update_nav_buttons("🏠 Dashboard")
        
        self.create_header("Reception Dashboard", "Queen Elizabeth Hospital - Patient Management")
        
        # Dashboard content
        main_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Quick action cards
        cards_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=10)
        
        # Configure grid for cards
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Card 1: Register Patient
        card1 = customtkinter.CTkFrame(cards_frame, fg_color="white", corner_radius=12, border_width=2, border_color="#e1e8ed")
        card1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        customtkinter.CTkLabel(card1, text="➕", font=("Arial", 32)).pack(pady=(20, 5))
        customtkinter.CTkLabel(card1, text="Register New Patient", font=("Arial", 16, "bold"), text_color=self.primary_color).pack()
        customtkinter.CTkLabel(card1, text="Add new patient to system", font=("Arial", 12), text_color="#666").pack()
        customtkinter.CTkButton(
            card1, 
            text="Register Now", 
            command=self.show_register_patient,
            fg_color=self.success_color,
            hover_color="#218838",
            height=35
        ).pack(pady=(10, 20))
        
        # Card 2: View Patients
        card2 = customtkinter.CTkFrame(cards_frame, fg_color="white", corner_radius=12, border_width=2, border_color="#e1e8ed")
        card2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        customtkinter.CTkLabel(card2, text="📋", font=("Arial", 32)).pack(pady=(20, 5))
        customtkinter.CTkLabel(card2, text="View Patients", font=("Arial", 16, "bold"), text_color=self.primary_color).pack()
        customtkinter.CTkLabel(card2, text="Browse patient records", font=("Arial", 12), text_color="#666").pack()
        customtkinter.CTkButton(
            card2, 
            text="View All", 
            command=self.show_view_patients,
            fg_color=self.accent_color,
            hover_color="#0056b3",
            height=35
        ).pack(pady=(10, 20))
        
        # Card 3: Search
        card3 = customtkinter.CTkFrame(cards_frame, fg_color="white", corner_radius=12, border_width=2, border_color="#e1e8ed")
        card3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        customtkinter.CTkLabel(card3, text="🔍", font=("Arial", 32)).pack(pady=(20, 5))
        customtkinter.CTkLabel(card3, text="Search Patients", font=("Arial", 16, "bold"), text_color=self.primary_color).pack()
        customtkinter.CTkLabel(card3, text="Find specific patients", font=("Arial", 12), text_color="#666").pack()
        customtkinter.CTkButton(
            card3, 
            text="Search", 
            command=self.show_search_patients,
            fg_color=self.warning_color,
            hover_color="#e0a800",
            text_color="black",
            height=35
        ).pack(pady=(10, 20))
        
        # Recent activity
        activity_frame = customtkinter.CTkFrame(main_frame, fg_color="white", corner_radius=12)
        activity_frame.pack(fill="both", expand=True, pady=10)
        
        customtkinter.CTkLabel(
            activity_frame, 
            text="📊 Recent Patient Registrations", 
            font=("Arial", 18, "bold"), 
            text_color=self.primary_color
        ).pack(pady=15)
        
        # Recent patients table
        self.show_recent_patients(activity_frame)

    def show_recent_patients(self, parent):
        """Show recent patient registrations with all fields in correct order"""
        try:
            self.cursor.execute("""
                SELECT patient_id, name, date_of_birth, gender, phone, address, date_registered 
                FROM patients 
                ORDER BY date_registered DESC 
                LIMIT 5
            """)
            recent_patients = self.cursor.fetchall()
            
            if recent_patients:
                # Create table header
                table_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
                table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
                
                headers = ["ID", "Name", "Date of Birth", "Gender", "Phone", "Address", "Registered"]
                header_frame = customtkinter.CTkFrame(table_frame, fg_color=self.light_bg)
                header_frame.pack(fill="x", pady=(0, 5))
                
                for i, header in enumerate(headers):
                    customtkinter.CTkLabel(
                        header_frame, 
                        text=header, 
                        font=("Arial", 12, "bold"),
                        text_color=self.primary_color
                    ).grid(row=0, column=i, padx=10, pady=8, sticky="w")
                
                # Table rows
                for i, patient in enumerate(recent_patients):
                    row_frame = customtkinter.CTkFrame(table_frame, fg_color="white" if i % 2 == 0 else "#f8f9fa")
                    row_frame.pack(fill="x", pady=1)
                    
                    for j, value in enumerate(patient):
                        display_value = str(value) if value else "N/A"
                        # Format date fields
                        if j == 2 and value:  # Date of Birth
                            display_value = value.strftime("%Y-%m-%d") if hasattr(value, 'strftime') else str(value)
                        if j == 6 and value:  # Registered
                            display_value = value.strftime("%Y-%m-%d %H:%M") if hasattr(value, 'strftime') else str(value)
                        customtkinter.CTkLabel(
                            row_frame, 
                            text=display_value, 
                            font=("Arial", 11),
                            text_color="#333"
                        ).grid(row=0, column=j, padx=10, pady=6, sticky="w")
            else:
                customtkinter.CTkLabel(
                    parent, 
                    text="No recent registrations found.", 
                    font=("Arial", 12), 
                    text_color="#666"
                ).pack(pady=20)
                
        except Exception as e:
            customtkinter.CTkLabel(
                parent, 
                text="Unable to load recent patients.", 
                font=("Arial", 12), 
                text_color=self.danger_color
            ).pack(pady=20)

    def show_register_patient(self):
        self.clear_content()
        self.current_view = "register"
        self.update_nav_buttons("➕ Register Patient")
        
        self.create_header("Register New Patient", "Add patient information to the hospital database")
        
        # Form container
        form_container = customtkinter.CTkFrame(self.content, fg_color="white", corner_radius=12)
        form_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Make the form scrollable
        form_frame = customtkinter.CTkScrollableFrame(form_container, fg_color="transparent", height=500)
        form_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Form title
        customtkinter.CTkLabel(
            form_frame, 
            text="👤 Patient Information", 
            font=("Arial", 20, "bold"), 
            text_color=self.primary_color
        ).pack(pady=(0, 20))
        
        # Form fields
        fields_frame = customtkinter.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", pady=10)
        
        # Name field
        name_frame = customtkinter.CTkFrame(fields_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=10)
        customtkinter.CTkLabel(name_frame, text="Full Name *", font=("Arial", 12, "bold"), text_color=self.primary_color).pack(anchor="w")
        self.name_entry = customtkinter.CTkEntry(
            name_frame, 
            placeholder_text="Enter patient's full name",
            height=40,
            font=("Arial", 12),
            corner_radius=8
        )
        self.name_entry.pack(fill="x", pady=(5, 0))
        
        # Date of birth field
        dob_frame = customtkinter.CTkFrame(fields_frame, fg_color="transparent")
        dob_frame.pack(fill="x", pady=10)
        customtkinter.CTkLabel(dob_frame, text="Date of Birth *", font=("Arial", 12, "bold"), text_color=self.primary_color).pack(anchor="w")
        self.dob_entry = customtkinter.CTkEntry(
            dob_frame, 
            placeholder_text="YYYY-MM-DD (e.g., 1990-01-15)",
            height=40,
            font=("Arial", 12),
            corner_radius=8
        )
        self.dob_entry.pack(fill="x", pady=(5, 0))
        
        # Gender field
        gender_frame = customtkinter.CTkFrame(fields_frame, fg_color="transparent")
        gender_frame.pack(fill="x", pady=10)
        customtkinter.CTkLabel(gender_frame, text="Gender *", font=("Arial", 12, "bold"), text_color=self.primary_color).pack(anchor="w")
        
        gender_radio_frame = customtkinter.CTkFrame(gender_frame, fg_color="transparent")
        gender_radio_frame.pack(fill="x", pady=(5, 0))
        
        self.gender_var = customtkinter.StringVar(value="")
        male_radio = customtkinter.CTkRadioButton(
            gender_radio_frame, 
            text="Male", 
            variable=self.gender_var, 
            value="male",
            font=("Arial", 12)
        )
        male_radio.pack(side="left", padx=(0, 20))
        
        female_radio = customtkinter.CTkRadioButton(
            gender_radio_frame, 
            text="Female", 
            variable=self.gender_var, 
            value="female",
            font=("Arial", 12)
        )
        female_radio.pack(side="left")
        
        # Phone field (optional)
        phone_frame = customtkinter.CTkFrame(fields_frame, fg_color="transparent")
        phone_frame.pack(fill="x", pady=10)
        customtkinter.CTkLabel(phone_frame, text="Phone Number (Optional)", font=("Arial", 12, "bold"), text_color=self.primary_color).pack(anchor="w")
        self.phone_entry = customtkinter.CTkEntry(
            phone_frame, 
            placeholder_text="e.g., +265 1 234 567",
            height=40,
            font=("Arial", 12),
            corner_radius=8
        )
        self.phone_entry.pack(fill="x", pady=(5, 0))
        
        # Address field (optional)
        address_frame = customtkinter.CTkFrame(fields_frame, fg_color="transparent")
        address_frame.pack(fill="x", pady=10)
        customtkinter.CTkLabel(address_frame, text="Address (Optional)", font=("Arial", 12, "bold"), text_color=self.primary_color).pack(anchor="w")
        self.address_entry = customtkinter.CTkTextbox(
            address_frame, 
            height=60,
            font=("Arial", 12),
            corner_radius=8
        )
        self.address_entry.pack(fill="x", pady=(5, 0))
        
        # Status message
        self.register_status = customtkinter.CTkLabel(
            form_frame, 
            text="", 
            font=("Arial", 12)
        )
        self.register_status.pack(pady=10)
        
        # Buttons
        button_frame = customtkinter.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        register_btn = customtkinter.CTkButton(
            button_frame, 
            text="✅ Register Patient", 
            command=self.register_patient,
            height=45,
            width=200,
            font=("Arial", 14, "bold"),
            fg_color=self.success_color,
            hover_color="#218838",
            corner_radius=8
        )
        register_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = customtkinter.CTkButton(
            button_frame, 
            text="🗑️ Clear Form", 
            command=self.clear_registration_form,
            height=45,
            width=150,
            font=("Arial", 14, "bold"),
            fg_color="#6c757d",
            hover_color="#5a6268",
            corner_radius=8
        )
        clear_btn.pack(side="left")

    def register_patient(self):
        name = self.name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        gender = self.gender_var.get()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get("1.0", "end-1c").strip()

        # Validation
        if not (name and dob and gender):
            self.register_status.configure(text="❌ Please fill in all required fields (*)", text_color=self.danger_color)
            return

        # Validate date format
        try:
            datetime.datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            self.register_status.configure(text="❌ Invalid date format. Use YYYY-MM-DD", text_color=self.danger_color)
            return

        # Phone number validation (if provided)
        if phone:
            if not (phone.isdigit() and len(phone) == 10):
                self.register_status.configure(
                    text="❌ Phone number must be exactly 10 digits (e.g., 0987425369)",
                    text_color=self.danger_color
                )
                return

        try:
            # Insert patient
            query = """
                INSERT INTO patients (name, date_of_birth, gender, phone, address) 
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, dob, gender, phone or None, address or None))
            self.conn.commit()

            # Get the new patient ID
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            new_id = self.cursor.fetchone()[0]

            # Success message
            self.register_status.configure(
                text=f"✅ Patient '{name}' registered successfully! ID: {new_id}", 
                text_color=self.success_color
            )

            # Log action
            log_action(self.username, "Receptionist", f"Registered patient: {name} (ID: {new_id})")

            # Clear form after successful registration
            self.master.after(2000, self.clear_registration_form)

        except Exception as err:
            self.register_status.configure(text=f"❌ Database Error: {str(err)}", text_color=self.danger_color)

    def clear_registration_form(self):
        self.name_entry.delete(0, 'end')
        self.dob_entry.delete(0, 'end')
        self.gender_var.set("")
        self.phone_entry.delete(0, 'end')
        self.address_entry.delete("1.0", "end")
        self.register_status.configure(text="")

    def show_view_patients(self):
        self.clear_content()
        self.current_view = "view_patients"
        self.update_nav_buttons("📋 View Patients")
        
        self.create_header("Patient Records", "Browse and manage patient information")
        
        # Main container
        main_container = customtkinter.CTkFrame(self.content, fg_color="white", corner_radius=12)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Controls frame
        controls_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=15)
        
        customtkinter.CTkLabel(
            controls_frame, 
            text="📋 All Patients", 
            font=("Arial", 18, "bold"), 
            text_color=self.primary_color
        ).pack(side="left")
        
        refresh_btn = customtkinter.CTkButton(
            controls_frame, 
            text="🔄 Refresh", 
            command=self.show_view_patients,
            height=35,
            width=100,
            fg_color=self.accent_color,
            hover_color="#0056b3"
        )
        refresh_btn.pack(side="right")
        
        # Table container
        table_container = customtkinter.CTkScrollableFrame(main_container, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        try:
            self.cursor.execute("""
                SELECT patient_id, name, date_of_birth, gender, phone, date_registered 
                FROM patients 
                ORDER BY date_registered DESC
            """)
            patients = self.cursor.fetchall()
            
            if patients:
                # Table header
                headers = ["ID", "Name", "Date of Birth", "Gender", "Phone", "Registered", "Actions"]
                header_frame = customtkinter.CTkFrame(table_container, fg_color=self.primary_color, height=40)
                header_frame.pack(fill="x", pady=(0, 5))
                
                for i, header in enumerate(headers):
                    customtkinter.CTkLabel(
                        header_frame, 
                        text=header, 
                        font=("Arial", 12, "bold"),
                        text_color="white"
                    ).grid(row=0, column=i, padx=10, pady=10, sticky="w")
                
                # Table rows
                for i, patient in enumerate(patients):
                    row_color = "white" if i % 2 == 0 else "#f8f9fa"
                    row_frame = customtkinter.CTkFrame(table_container, fg_color=row_color, height=50)
                    row_frame.pack(fill="x", pady=1)
                    row_frame.pack_propagate(False)
                    
                    # Patient data
                    for j, value in enumerate(patient):
                        display_value = str(value) if value else "N/A"
                        if j == 2 and value:  # Format date
                            display_value = value.strftime("%Y-%m-%d") if hasattr(value, 'strftime') else str(value)
                        
                        customtkinter.CTkLabel(
                            row_frame, 
                            text=display_value, 
                            font=("Arial", 11),
                            text_color="#333"
                        ).grid(row=0, column=j, padx=10, pady=10, sticky="w")
                    
                    # Action buttons
                    action_frame = customtkinter.CTkFrame(row_frame, fg_color="transparent")
                    action_frame.grid(row=0, column=len(headers)-1, padx=10, pady=5, sticky="w")
                    
                    def make_view_callback(patient_id=patient[0]):
                        return lambda: self.view_patient_details(patient_id)
                    
                    view_btn = customtkinter.CTkButton(
                        action_frame, 
                        text="👁️", 
                        width=30,
                        height=30,
                        font=("Arial", 12),
                        fg_color=self.accent_color,
                        hover_color="#0056b3",
                        command=make_view_callback()
                    )
                    view_btn.pack(side="left", padx=2)
            else:
                no_data_frame = customtkinter.CTkFrame(table_container, fg_color="transparent")
                no_data_frame.pack(fill="both", expand=True)
                
                customtkinter.CTkLabel(
                    no_data_frame, 
                    text="📝 No patient records found", 
                    font=("Arial", 16), 
                    text_color="#666"
                ).pack(expand=True)
                
        except Exception as err:
            error_frame = customtkinter.CTkFrame(table_container, fg_color="transparent")
            error_frame.pack(fill="both", expand=True)
            
            customtkinter.CTkLabel(
                error_frame, 
                text=f"❌ Error loading patients: {str(err)}", 
                font=("Arial", 14), 
                text_color=self.danger_color
            ).pack(expand=True)

    def view_patient_details(self, patient_id):
        """Show detailed patient information in a popup"""
        try:
            self.cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient_data = self.cursor.fetchone()
            
            if patient_data:
                # Create popup window
                detail_window = customtkinter.CTkToplevel(self)
                detail_window.title(f"Patient Details - ID: {patient_id}")
                detail_window.geometry("500x600")
                detail_window.resizable(False, False)
                
                # Window content
                content_frame = customtkinter.CTkScrollableFrame(detail_window)
                content_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Header
                customtkinter.CTkLabel(
                    content_frame, 
                    text=f"👤 Patient Information", 
                    font=("Arial", 20, "bold"), 
                    text_color=self.primary_color
                ).pack(pady=(0, 20))
                
                # Patient details
                fields = [
                    ("Patient ID", patient_data[0]),
                    ("Full Name", patient_data[1]),
                    ("Date of Birth", patient_data[2]),
                    ("Gender", patient_data[3].title() if patient_data[3] else "N/A"),
                    ("Phone", patient_data[4] if patient_data[4] else "Not provided"),
                    ("Address", patient_data[5] if patient_data[5] else "Not provided"),
                    ("Registration Date", patient_data[6])
                ]
                
                for label, value in fields:
                    field_frame = customtkinter.CTkFrame(content_frame, fg_color=self.light_bg)
                    field_frame.pack(fill="x", pady=5)
                    
                    customtkinter.CTkLabel(
                        field_frame, 
                        text=f"{label}:", 
                        font=("Arial", 12, "bold"), 
                        text_color=self.primary_color
                    ).pack(anchor="w", padx=15, pady=(10, 0))
                    
                    customtkinter.CTkLabel(
                        field_frame, 
                        text=str(value), 
                        font=("Arial", 12), 
                        text_color="#333"
                    ).pack(anchor="w", padx=15, pady=(0, 10))
                
                # Close button
                customtkinter.CTkButton(
                    content_frame, 
                    text="Close", 
                    command=detail_window.destroy,
                    height=35,
                    fg_color=self.secondary_color,
                    hover_color=self.primary_color
                ).pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient details: {str(e)}")

    def show_search_patients(self):
        self.clear_content()
        self.current_view = "search"
        self.update_nav_buttons("🔍 Search Patients")
        
        self.create_header("Search Patients", "Find patients by name, ID, or other criteria")
        
        # Search container
        search_container = customtkinter.CTkFrame(self.content, fg_color="white", corner_radius=12)
        search_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Search form
        search_form = customtkinter.CTkFrame(search_container, fg_color=self.light_bg, corner_radius=10)
        search_form.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            search_form, 
            text="🔍 Search Criteria", 
            font=("Arial", 16, "bold"), 
            text_color=self.primary_color
        ).pack(pady=15)
        
        # Search fields
        search_fields_frame = customtkinter.CTkFrame(search_form, fg_color="transparent")
        search_fields_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Search by name
        name_search_frame = customtkinter.CTkFrame(search_fields_frame, fg_color="transparent")
        name_search_frame.pack(fill="x", pady=5)
        
        customtkinter.CTkLabel(name_search_frame, text="Patient Name:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.search_name_entry = customtkinter.CTkEntry(
            name_search_frame, 
            placeholder_text="Enter patient name",
            height=35,
            font=("Arial", 12)
        )
        self.search_name_entry.pack(fill="x", pady=(5, 0))
        
        # Search by ID
        id_search_frame = customtkinter.CTkFrame(search_fields_frame, fg_color="transparent")
        id_search_frame.pack(fill="x", pady=5)
        
        customtkinter.CTkLabel(id_search_frame, text="Patient ID:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.search_id_entry = customtkinter.CTkEntry(
            id_search_frame, 
            placeholder_text="Enter patient ID",
            height=35,
            font=("Arial", 12)
        )
        self.search_id_entry.pack(fill="x", pady=(5, 0))
        
        # Search buttons
        search_btn_frame = customtkinter.CTkFrame(search_form, fg_color="transparent")
        search_btn_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        search_btn = customtkinter.CTkButton(
            search_btn_frame, 
            text="🔍 Search", 
            command=self.perform_search,
            height=40,
            width=120,
            font=("Arial", 12, "bold"),
            fg_color=self.accent_color,
            hover_color="#0056b3"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        clear_search_btn = customtkinter.CTkButton(
            search_btn_frame, 
            text="🗑️ Clear", 
            command=self.clear_search,
            height=40,
            width=100,
            font=("Arial", 12, "bold"),
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        clear_search_btn.pack(side="left")
        
        # Results area
        self.search_results_frame = customtkinter.CTkFrame(search_container, fg_color="transparent")
        self.search_results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Initial message
        customtkinter.CTkLabel(
            self.search_results_frame, 
            text="Enter search criteria above and click 'Search'", 
            font=("Arial", 14), 
            text_color="#666"
        ).pack(expand=True)

    def perform_search(self):
        # Clear previous results
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
        
        search_name = self.search_name_entry.get().strip()
        search_id = self.search_id_entry.get().strip()
        
        if not search_name and not search_id:
            customtkinter.CTkLabel(
                self.search_results_frame, 
                text="❌ Please enter search criteria", 
                font=("Arial", 14), 
                text_color=self.danger_color
            ).pack(expand=True)
            return
        
        try:
            # Build query
            query_parts = []
            params = []
            
            if search_name:
                query_parts.append("name LIKE %s")
                params.append(f"%{search_name}%")
            
            if search_id:
                query_parts.append("patient_id = %s")
                params.append(search_id)
            
            query = f"""
                SELECT patient_id, name, date_of_birth, gender, phone, date_registered 
                FROM patients 
                WHERE {' OR '.join(query_parts)}
                ORDER BY name
            """
            
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            
            if results:
                # Results header
                results_header = customtkinter.CTkLabel(
                    self.search_results_frame, 
                    text=f"📊 Search Results ({len(results)} found)", 
                    font=("Arial", 16, "bold"), 
                    text_color=self.primary_color
                )
                results_header.pack(pady=(10, 15))
                
                # Results table
                table_frame = customtkinter.CTkScrollableFrame(self.search_results_frame, height=300)
                table_frame.pack(fill="both", expand=True)
                
                # Table header
                headers = ["ID", "Name", "Date of Birth", "Gender", "Phone", "Registered", "Action"]
                header_frame = customtkinter.CTkFrame(table_frame, fg_color=self.primary_color, height=40)
                header_frame.pack(fill="x", pady=(0, 5))
                
                for i, header in enumerate(headers):
                    customtkinter.CTkLabel(
                        header_frame, 
                        text=header, 
                        font=("Arial", 12, "bold"),
                        text_color="white"
                    ).grid(row=0, column=i, padx=10, pady=10, sticky="w")
                
                # Results rows
                for i, patient in enumerate(results):
                    row_color = "white" if i % 2 == 0 else "#f8f9fa"
                    row_frame = customtkinter.CTkFrame(table_frame, fg_color=row_color, height=45)
                    row_frame.pack(fill="x", pady=1)
                    row_frame.pack_propagate(False)
                    
                    for j, value in enumerate(patient):
                        display_value = str(value) if value else "N/A"
                        if j == 2 and value:  # Format date
                            display_value = value.strftime("%Y-%m-%d") if hasattr(value, 'strftime') else str(value)
                        
                        customtkinter.CTkLabel(
                            row_frame, 
                            text=display_value, 
                            font=("Arial", 11),
                            text_color="#333"
                        ).grid(row=0, column=j, padx=10, pady=8, sticky="w")
                    
                    # View button
                    def make_view_callback(patient_id=patient[0]):
                        return lambda: self.view_patient_details(patient_id)
                    
                    view_btn = customtkinter.CTkButton(
                        row_frame, 
                        text="👁️ View", 
                        width=70,
                        height=25,
                        font=("Arial", 10),
                        fg_color=self.accent_color,
                        hover_color="#0056b3",
                        command=make_view_callback()
                    )
                    view_btn.grid(row=0, column=len(headers)-1, padx=10, pady=8)
            else:
                customtkinter.CTkLabel(
                    self.search_results_frame, 
                    text="❌ No patients found matching your search criteria", 
                    font=("Arial", 14), 
                    text_color=self.warning_color
                ).pack(expand=True)
                
        except Exception as e:
            customtkinter.CTkLabel(
                self.search_results_frame, 
                text=f"❌ Search error: {str(e)}", 
                font=("Arial", 14), 
                text_color=self.danger_color
            ).pack(expand=True)

    def clear_search(self):
        self.search_name_entry.delete(0, 'end')
        self.search_id_entry.delete(0, 'end')
        
        # Clear results
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
        
        customtkinter.CTkLabel(
            self.search_results_frame, 
            text="Enter search criteria above and click 'Search'", 
            font=("Arial", 14), 
            text_color="#666"
        ).pack(expand=True)

    def show_daily_reports(self):
        self.clear_content()
        self.current_view = "reports"
        self.update_nav_buttons("📊 Daily Reports")
        
        self.create_header("Daily Reports", "View registration statistics and summaries")
        
        # Reports container
        reports_container = customtkinter.CTkFrame(self.content, fg_color="white", corner_radius=12)
        reports_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        try:
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            
            # Today's stats
            self.cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(date_registered) = %s", (today,))
            today_count = self.cursor.fetchone()[0]
            
            # This week's stats
            self.cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(date_registered) >= %s", (week_ago,))
            week_count = self.cursor.fetchone()[0]
            
            # Total patients
            self.cursor.execute("SELECT COUNT(*) FROM patients")
            total_count = self.cursor.fetchone()[0]
            
            # Gender breakdown
            self.cursor.execute("SELECT gender, COUNT(*) FROM patients GROUP BY gender")
            gender_stats = self.cursor.fetchall()
            
            # Stats grid
            stats_frame = customtkinter.CTkFrame(reports_container, fg_color="transparent")
            stats_frame.pack(fill="x", padx=20, pady=20)
            
            stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
            
            # Today's registrations
            today_card = customtkinter.CTkFrame(stats_frame, fg_color=self.success_color, corner_radius=10)
            today_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            
            customtkinter.CTkLabel(today_card, text="📅", font=("Arial", 24)).pack(pady=(15, 5))
            customtkinter.CTkLabel(today_card, text="Today's Registrations", font=("Arial", 12, "bold"), text_color="white").pack()
            customtkinter.CTkLabel(today_card, text=str(today_count), font=("Arial", 32, "bold"), text_color="white").pack(pady=(5, 15))
            
            # Week's registrations
            week_card = customtkinter.CTkFrame(stats_frame, fg_color=self.accent_color, corner_radius=10)
            week_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            
            customtkinter.CTkLabel(week_card, text="📊", font=("Arial", 24)).pack(pady=(15, 5))
            customtkinter.CTkLabel(week_card, text="This Week", font=("Arial", 12, "bold"), text_color="white").pack()
            customtkinter.CTkLabel(week_card, text=str(week_count), font=("Arial", 32, "bold"), text_color="white").pack(pady=(5, 15))
            
            # Total patients
            total_card = customtkinter.CTkFrame(stats_frame, fg_color=self.primary_color, corner_radius=10)
            total_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
            
            customtkinter.CTkLabel(total_card, text="👥", font=("Arial", 24)).pack(pady=(15, 5))
            customtkinter.CTkLabel(total_card, text="Total Patients", font=("Arial", 12, "bold"), text_color="white").pack()
            customtkinter.CTkLabel(total_card, text=str(total_count), font=("Arial", 32, "bold"), text_color="white").pack(pady=(5, 15))
            
            # Gender breakdown
            gender_frame = customtkinter.CTkFrame(reports_container, fg_color=self.light_bg, corner_radius=10)
            gender_frame.pack(fill="x", padx=20, pady=10)
            
            customtkinter.CTkLabel(
                gender_frame, 
                text="👫 Gender Distribution", 
                font=("Arial", 16, "bold"), 
                text_color=self.primary_color
            ).pack(pady=15)
            
            gender_stats_frame = customtkinter.CTkFrame(gender_frame, fg_color="transparent")
            gender_stats_frame.pack(fill="x", padx=20, pady=(0, 15))
            
            for gender, count in gender_stats:
                gender_row = customtkinter.CTkFrame(gender_stats_frame, fg_color="white", corner_radius=5)
                gender_row.pack(fill="x", pady=5)
                
                customtkinter.CTkLabel(
                    gender_row, 
                    text=f"{gender.title()}: {count} patients", 
                    font=("Arial", 12), 
                    text_color="#333"
                ).pack(pady=8)
                
        except Exception as e:
            error_label = customtkinter.CTkLabel(
                reports_container, 
                text=f"❌ Error loading reports: {str(e)}", 
                font=("Arial", 14), 
                text_color=self.danger_color
            )
            error_label.pack(expand=True)

    def show_quick_actions(self):
        self.clear_content()
        self.current_view = "quick_actions"
        self.update_nav_buttons("⚙️ Quick Actions")
        
        self.create_header("Quick Actions", "Commonly used receptionist tools and shortcuts")
        
        # Quick actions container
        actions_container = customtkinter.CTkFrame(self.content, fg_color="white", corner_radius=12)
        actions_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Actions grid
        actions_grid = customtkinter.CTkFrame(actions_container, fg_color="transparent")
        actions_grid.pack(fill="both", expand=True, padx=40, pady=40)
        
        actions_grid.grid_columnconfigure((0, 1), weight=1)
        actions_grid.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Quick action buttons
        actions = [
            ("🏥 Hospital Info", "View hospital contact information", self.show_hospital_info),
            ("📞 Emergency Contacts", "Important phone numbers", self.show_emergency_contacts),
            ("📋 Print Patient List", "Generate patient list report", self.print_patient_list),
            ("🔄 Refresh Database", "Reload all patient data", self.refresh_database),
            ("📊 Export Reports", "Export data to file", self.export_reports),
            ("❓ Help & Support", "Get help using the system", self.show_help)
        ]
        
        for i, (title, description, command) in enumerate(actions):
            row = i // 2
            col = i % 2
            
            action_card = customtkinter.CTkFrame(actions_grid, fg_color=self.light_bg, corner_radius=12, border_width=2, border_color="#e1e8ed")
            action_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            customtkinter.CTkLabel(action_card, text=title.split()[0], font=("Arial", 32)).pack(pady=(20, 10))
            customtkinter.CTkLabel(action_card, text=title.split(' ', 1)[1], font=("Arial", 16, "bold"), text_color=self.primary_color).pack()
            customtkinter.CTkLabel(action_card, text=description, font=("Arial", 12), text_color="#666").pack(pady=(5, 15))
            
            customtkinter.CTkButton(
                action_card, 
                text="Execute", 
                command=command,
                height=35,
                fg_color=self.accent_color,
                hover_color="#0056b3"
            ).pack(pady=(0, 20))

    def show_hospital_info(self):
        info_text = """🏥 QUEEN ELIZABETH CENTRAL HOSPITAL
        
📍 Location: Blantyre, Malawi
📞 Main Line: +265 1 871 911
🚑 Emergency: +265 1 871 800
📧 Email: info@qech.gov.mw
🌐 Website: www.qech.gov.mw

⏰ Reception Hours:
Monday - Friday: 7:00 AM - 5:00 PM
Saturday: 8:00 AM - 12:00 PM
Sunday: Emergency Only

🏥 Departments:
- Emergency Department
- Outpatient Clinic
- Inpatient Wards
- Maternity Ward
- Pediatrics
- Surgery
- Radiology
- Laboratory"""
        
        messagebox.showinfo("Hospital Information", info_text)

    def show_emergency_contacts(self):
        emergency_text = """🚨 EMERGENCY CONTACTS
        
🏥 Hospital Emergency: +265 1 871 800
👨‍⚕️ Chief Medical Officer: +265 1 871 850
👩‍💼 Hospital Administrator: +265 1 871 820
🔧 IT Support: +265 1 871 900
🚨 Security: +265 1 871 999
🚑 Ambulance: +265 1 871 800

🌙 Night Shift Supervisor: +265 1 871 830
📞 Operator: +265 1 871 911

⚠️ For life-threatening emergencies, 
call 911 or go directly to Emergency Department"""
        
        messagebox.showinfo("Emergency Contacts", emergency_text)

    def print_patient_list(self):
        messagebox.showinfo("Print Function", "📄 Print function would generate a patient list report.\n\nThis feature requires printer setup and configuration.")

    def refresh_database(self):
        try:
            # Reconnect to database
            if self.conn:
                self.conn.close()
            self.conn = get_connection()
            self.cursor = self.conn.cursor()
            messagebox.showinfo("Success", "✅ Database connection refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to refresh database: {str(e)}")

    def export_reports(self):
        messagebox.showinfo("Export Function", "📊 Export function would save patient data to CSV/Excel file.\n\nThis feature requires file system permissions.")

    def show_help(self):
        help_text = """❓ HELP & SUPPORT
        
📘 User Manual:
- Register Patient: Fill all required fields (*)
- View Patients: Browse all registered patients
- Search: Find patients by name or ID
- Reports: View daily statistics

🔧 Technical Support:
- Phone: +265 1 871 900
- Email: it.support@qech.gov.mw

💡 Tips:
- Use YYYY-MM-DD format for dates
- Required fields are marked with (*)
- Double-click to view patient details
- Use Search for quick patient lookup

🚨 For urgent technical issues,
contact IT Support immediately."""
        
        messagebox.showinfo("Help & Support", help_text)

    def logout(self):
        try:
            if self.conn:
                self.conn.close()
            log_action(self.username, "Receptionist", "Logged out")
        except:
            pass
        self.master.destroy()
        if self.on_logout:
            self.on_logout()