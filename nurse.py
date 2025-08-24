import customtkinter
from tkinter import messagebox
from db_connection import get_connection, log_action
import datetime

class NurseFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor(buffered=True)  # Fixed: Added buffered=True
        self.on_logout = None

        # Enhanced color scheme
        self.colors = {
            'primary': '#2c5f41',      # Forest green
            'secondary': '#1e3a5f',     # Deep blue
            'accent': '#27ae60',        # Success green
            'light_green': '#d5f4e6',   # Light green
            'white': '#ffffff',
            'light_gray': '#f5f5f5',
            'text_dark': '#2c3e50',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#3498db'
        }

        # Simple layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.content = customtkinter.CTkFrame(self, fg_color=self.colors['light_gray'])
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Show welcome screen
        self.show_welcome()

    def create_sidebar(self):
        """Create enhanced sidebar with reordered navigation"""
        self.sidebar = customtkinter.CTkFrame(self, width=220, fg_color=self.colors['primary'])
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)
        self.sidebar.grid_propagate(False)

        # Hospital Title
        customtkinter.CTkLabel(
            self.sidebar, 
            text="Queen Elizabeth\nCentral Hospital", 
            font=("Arial", 16, "bold"), 
            text_color="white",
            justify="center"
        ).pack(pady=(20, 5))
        
        customtkinter.CTkLabel(
            self.sidebar, 
            text="Nursing Station", 
            font=("Arial", 14, "bold"), 
            text_color="#cccccc"
        ).pack(pady=(0, 10))
        
        customtkinter.CTkLabel(
            self.sidebar, 
            text=f"Nurse: {self.username}", 
            font=("Arial", 12), 
            text_color="lightgray"
        ).pack(pady=(0, 20))

        # Navigation buttons - REORDERED FOR BETTER WORKFLOW
        buttons = [
            ("Dashboard", self.show_welcome),
            ("Pending Patients", self.show_pending_patients),  # NEW - Added as priority
            ("Record Vitals", self.show_record_vitals),
            ("View Patient Data", self.show_view_vitals),
            ("Patient Notes", self.show_patient_notes),
            ("Emergency Cases", self.show_emergency_cases)
        ]
        
        for text, command in buttons:
            btn = customtkinter.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=40,
                font=("Arial", 12, "bold"),
                fg_color="transparent",
                hover_color=self.colors['secondary'],
                text_color="white"
            )
            btn.pack(fill="x", padx=15, pady=3)

        # Emergency alert button
        emergency_btn = customtkinter.CTkButton(
            self.sidebar,
            text="Check Emergencies",
            command=self.check_emergencies,
            height=45,
            font=("Arial", 12, "bold"),
            fg_color=self.colors['danger'],
            hover_color="#c0392b",
            text_color="white"
        )
        emergency_btn.pack(fill="x", padx=15, pady=10)

        # Logout button
        customtkinter.CTkButton(
            self.sidebar,
            text="Logout",
            command=self.logout,
            height=40,
            fg_color=self.colors['text_dark'],
            hover_color="#1a252f"
        ).pack(side="bottom", fill="x", padx=15, pady=20)

    def clear_content(self):
        """Clear main content area"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        """Enhanced welcome screen with statistics"""
        self.clear_content()
        
        # Welcome header
        welcome_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            welcome_frame,
            text=f"Welcome, Nurse {self.username}!",
            font=("Arial", 24, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        customtkinter.CTkLabel(
            welcome_frame,
            text="Queen Elizabeth Hospital - Nursing Station",
            font=("Arial", 16),
            text_color="#7f8c8d"
        ).pack(anchor="w", pady=(5, 0))
        
        # Enhanced statistics cards
        stats_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        try:
            # Fixed SQL queries
            self.cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = self.cursor.fetchone()[0]
            
            # Get pending patients (those without vitals today) - FIXED QUERY
            self.cursor.execute("""
                SELECT COUNT(DISTINCT p.patient_id) 
                FROM patients p 
                WHERE p.patient_id NOT IN (
                    SELECT DISTINCT patient_id FROM treatments 
                    WHERE DATE(date) = CURDATE() 
                    AND (blood_pressure IS NOT NULL OR temperature IS NOT NULL OR weight IS NOT NULL)
                )
            """)
            pending_patients = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM treatments WHERE DATE(date) = CURDATE()")
            today_vitals = self.cursor.fetchone()[0]
            
            # Fixed emergency query - check if table exists
            try:
                self.cursor.execute("SELECT COUNT(*) FROM patient_notes WHERE emergency = TRUE AND DATE(date) = CURDATE()")
                today_emergencies = self.cursor.fetchone()[0]
            except:
                today_emergencies = 0
                
        except Exception as e:
            print(f"Database error in dashboard: {e}")
            total_patients = pending_patients = today_vitals = today_emergencies = 0
        
        # Statistics cards
        stats_data = [
            ("Total Patients", total_patients, self.colors['info']),
            ("Pending Patients", pending_patients, self.colors['warning']),
            ("Vitals Recorded Today", today_vitals, self.colors['accent']),
            ("Emergency Cases", today_emergencies, self.colors['danger'])
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            card = customtkinter.CTkFrame(stats_frame, fg_color=color, width=150, height=100)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            customtkinter.CTkLabel(
                card,
                text=str(value),
                font=("Arial", 24, "bold"),
                text_color="white"
            ).pack(pady=(20, 5))
            
            customtkinter.CTkLabel(
                card,
                text=title,
                font=("Arial", 11),
                text_color="white"
            ).pack()

        # Quick actions
        actions_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        actions_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        customtkinter.CTkLabel(
            actions_frame,
            text="Quick Nursing Actions",
            font=("Arial", 18, "bold"),
            text_color=self.colors['text_dark']
        ).pack(pady=20)
        
        quick_frame = customtkinter.CTkFrame(actions_frame, fg_color="transparent")
        quick_frame.pack(expand=True, fill="both", padx=40, pady=20)
        
        actions = [
            ("View Pending Patients", self.show_pending_patients, self.colors['warning']),
            ("Record Patient Vitals", self.show_record_vitals, self.colors['accent']),
            ("Check Emergency Cases", self.show_emergency_cases, self.colors['danger']),
            ("Add Patient Notes", self.show_patient_notes, self.colors['info'])
        ]
        
        for i, (text, command, color) in enumerate(actions):
            btn = customtkinter.CTkButton(
                quick_frame,
                text=text,
                command=command,
                width=180,
                height=50,
                font=("Arial", 13, "bold"),
                fg_color=color
            )
            btn.grid(row=i//2, column=i%2, padx=15, pady=10, sticky="ew")

    # FIXED: Show Pending Patients for Nurse
    def show_pending_patients(self):
        """Show patients who need nursing attention (vitals recording)"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="Pending Patients - Need Vitals Recording",
            font=("Arial", 22, "bold"),
            text_color=self.colors['warning']
        ).pack(anchor="w")
        
        try:
            # FIXED: Simplified query that should work
            self.cursor.execute("""
                SELECT p.patient_id, p.name, p.gender, p.blood_type, p.date_registered
                FROM patients p
                WHERE p.patient_id NOT IN (
                    SELECT DISTINCT patient_id FROM treatments 
                    WHERE DATE(date) = CURDATE() 
                    AND (blood_pressure IS NOT NULL OR temperature IS NOT NULL OR weight IS NOT NULL)
                )
                ORDER BY p.date_registered ASC
            """)
            pending = self.cursor.fetchall()

            if not pending:
                customtkinter.CTkLabel(
                    self.content,
                    text="Excellent! All patients have current vitals recorded today.",
                    font=("Arial", 16),
                    text_color=self.colors['accent']
                ).pack(pady=50)
                return

            # Statistics
            stats_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['warning'])
            stats_frame.pack(fill="x", padx=20, pady=10)
            
            customtkinter.CTkLabel(
                stats_frame,
                text=f"NURSING PRIORITY: {len(pending)} patients need vitals recording",
                font=("Arial", 16, "bold"),
                text_color="white"
            ).pack(pady=10)

            # Scrollable patient list
            list_frame = customtkinter.CTkFrame(self.content)
            list_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            scroll_frame = customtkinter.CTkScrollableFrame(list_frame, height=400)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Header
            header_frame = customtkinter.CTkFrame(scroll_frame, fg_color=self.colors['text_dark'])
            header_frame.pack(fill="x", pady=(0, 5))
            
            headers = ["Patient ID", "Name", "Gender", "Blood Type", "Registered", "Action"]
            widths = [80, 150, 80, 100, 120, 120]
            
            for i, (header, width) in enumerate(zip(headers, widths)):
                customtkinter.CTkLabel(
                    header_frame, 
                    text=header, 
                    font=("Arial", 12, "bold"), 
                    text_color="white",
                    width=width
                ).grid(row=0, column=i, padx=5, pady=10)

            # Patient rows
            for patient in pending:
                patient_frame = customtkinter.CTkFrame(scroll_frame, fg_color="#ecf0f1")
                patient_frame.pack(fill="x", pady=2)
                
                data = [
                    patient[0], 
                    patient[1][:15] + "..." if len(patient[1]) > 15 else patient[1], 
                    patient[2], 
                    patient[3], 
                    str(patient[4]).split()[0] if patient[4] else 'N/A'
                ]
                
                for i, (value, width) in enumerate(zip(data, widths[:-1])):
                    label = customtkinter.CTkLabel(
                        patient_frame, 
                        text=str(value), 
                        width=width,
                        font=("Arial", 11)
                    )
                    label.grid(row=0, column=i, padx=5, pady=8)
                
                # Action button
                record_btn = customtkinter.CTkButton(
                    patient_frame,
                    text="Record Vitals",
                    width=100,
                    height=30,
                    font=("Arial", 10, "bold"),
                    fg_color=self.colors['accent'],
                    command=lambda pid=patient[0], pname=patient[1]: self.quick_record_vitals(pid, pname)
                )
                record_btn.grid(row=0, column=5, padx=5, pady=5)

        except Exception as e:
            print(f"Database error in show_pending_patients: {e}")
            messagebox.showerror("Database Error", f"Error loading pending patients: {e}")

    def quick_record_vitals(self, patient_id, patient_name):
        """FIXED: Quick vitals recording interface for pending patients"""
        try:
            # Create vitals window
            vitals_window = customtkinter.CTkToplevel(self)
            vitals_window.title(f"Record Vitals - {patient_name}")
            vitals_window.geometry("500x600")
            vitals_window.grab_set()  # Make window modal
            
            # Patient info
            customtkinter.CTkLabel(
                vitals_window,
                text=f"Recording Vitals for: {patient_name} (ID: {patient_id})",
                font=("Arial", 16, "bold")
            ).pack(pady=20)
            
            # Vital signs form
            form_frame = customtkinter.CTkFrame(vitals_window, fg_color=self.colors['light_green'])
            form_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Blood Pressure
            customtkinter.CTkLabel(
                form_frame,
                text="Blood Pressure (e.g., 120/80):",
                font=("Arial", 12, "bold"),
                text_color=self.colors['text_dark']
            ).pack(anchor="w", padx=20, pady=(20, 5))
            
            bp_entry = customtkinter.CTkEntry(
                form_frame,
                placeholder_text="Enter blood pressure",
                width=300,
                height=35
            )
            bp_entry.pack(anchor="w", padx=20, pady=(0, 15))
            
            # Temperature
            customtkinter.CTkLabel(
                form_frame,
                text="Temperature (°C):",
                font=("Arial", 12, "bold"),
                text_color=self.colors['text_dark']
            ).pack(anchor="w", padx=20, pady=(0, 5))
            
            temp_entry = customtkinter.CTkEntry(
                form_frame,
                placeholder_text="Enter temperature",
                width=300,
                height=35
            )
            temp_entry.pack(anchor="w", padx=20, pady=(0, 15))
            
            # Weight
            customtkinter.CTkLabel(
                form_frame,
                text="Weight (kg):",
                font=("Arial", 12, "bold"),
                text_color=self.colors['text_dark']
            ).pack(anchor="w", padx=20, pady=(0, 5))
            
            weight_entry = customtkinter.CTkEntry(
                form_frame,
                placeholder_text="Enter weight",
                width=300,
                height=35
            )
            weight_entry.pack(anchor="w", padx=20, pady=(0, 15))
            
            # Additional Notes
            customtkinter.CTkLabel(
                form_frame,
                text="Additional Notes:",
                font=("Arial", 12, "bold"),
                text_color=self.colors['text_dark']
            ).pack(anchor="w", padx=20, pady=(10, 5))
            
            notes_text = customtkinter.CTkTextbox(
                form_frame,
                height=80,
                width=300
            )
            notes_text.pack(anchor="w", padx=20, pady=(0, 20))
            
            def save_vitals():
                """FIXED: Save the vitals with proper error handling"""
                bp = bp_entry.get().strip()
                temp = temp_entry.get().strip()
                weight = weight_entry.get().strip()
                notes = notes_text.get("1.0", "end-1c").strip()
                
                if not any([bp, temp, weight]):
                    messagebox.showerror("Error", "Please enter at least one vital sign.")
                    return
                
                try:
                    # Convert numeric values with validation
                    temp_val = None
                    weight_val = None
                    
                    if temp:
                        temp_val = float(temp)
                        if temp_val < 30 or temp_val > 50:
                            messagebox.showerror("Error", "Temperature must be between 30-50°C")
                            return
                    
                    if weight:
                        weight_val = float(weight)
                        if weight_val < 1 or weight_val > 500:
                            messagebox.showerror("Error", "Weight must be between 1-500 kg")
                            return
                    
                    # FIXED: Insert new treatment record with vitals
                    self.cursor.execute("""
                        INSERT INTO treatments (patient_id, blood_pressure, temperature, weight, notes, date)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                    """, (patient_id, bp if bp else None, temp_val, weight_val, notes if notes else None))
                    
                    self.conn.commit()
                    
                    messagebox.showinfo("Success", f"Vitals recorded successfully for {patient_name}!")
                    
                    # Log the action
                    try:
                        log_action(self.username, "Nurse", f"Recorded vitals for patient ID: {patient_id}")
                    except Exception as log_err:
                        print(f"Logging error: {log_err}")
                    
                    vitals_window.destroy()
                    self.show_pending_patients()  # Refresh the list
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers for temperature and weight.")
                except Exception as err:
                    print(f"Database error saving vitals: {err}")
                    messagebox.showerror("Database Error", f"Error saving vitals: {str(err)}")
            
            # Save button
            save_btn = customtkinter.CTkButton(
                form_frame,
                text="Save Vitals",
                command=save_vitals,
                height=45,
                width=200,
                font=("Arial", 14, "bold"),
                fg_color=self.colors['accent']
            )
            save_btn.pack(pady=20)
            
        except Exception as e:
            print(f"Error opening vitals window: {e}")
            messagebox.showerror("Error", f"Error opening vitals recording window: {str(e)}")

    def check_emergencies(self):
        """FIXED: Check for emergency cases"""
        try:
            # Check if patient_notes table exists
            self.cursor.execute("SHOW TABLES LIKE 'patient_notes'")
            table_exists = self.cursor.fetchone()
            
            if not table_exists:
                messagebox.showinfo("No Emergency System", "Emergency notes system is not set up yet.")
                return
                
            self.cursor.execute("""
                SELECT n.patient_id, p.name, n.notes, n.date, n.author
                FROM patient_notes n
                JOIN patients p ON n.patient_id = p.patient_id
                WHERE n.emergency=1 AND DATE(n.date) = CURDATE()
                ORDER BY n.date DESC
            """)
            today_emergencies = self.cursor.fetchall()
            
            if today_emergencies:
                msg = "EMERGENCY ALERT - TODAY'S CASES!\n\n"
                for patient_id, name, notes, date, author in today_emergencies:
                    msg += f"Patient: {name} (ID: {patient_id})\n"
                    msg += f"Notes: {notes}\n"
                    msg += f"Time: {date.strftime('%H:%M')}\n"
                    msg += f"Reported by: {author}\n"
                    msg += "-" * 40 + "\n\n"
                
                messagebox.showwarning("Emergency Alert", msg)
                self.show_emergency_cases()
            else:
                messagebox.showinfo("No Emergencies", "No emergency cases reported today.")
                
        except Exception as e:
            print(f"Error checking emergencies: {e}")
            messagebox.showerror("Error", f"Error checking emergencies: {str(e)}")

    # FIXED: Record vitals with better error handling
    def show_record_vitals(self):
        """FIXED: Record patient vitals with enhanced interface"""
        self.clear_content()
        
        # Title
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="Record Patient Vitals",
            font=("Arial", 20, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")
        
        customtkinter.CTkLabel(
            title_frame,
            text="Complete vital signs recording for patient care",
            font=("Arial", 14),
            text_color="#7f8c8d"
        ).pack(anchor="w", pady=(5, 0))

        # Main form frame
        form_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Get patients from database
        try:
            self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
            patients = self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting patients: {e}")
            patients = []

        if not patients:
            customtkinter.CTkLabel(
                form_frame,
                text="No patients found in database",
                font=("Arial", 16),
                text_color=self.colors['danger']
            ).pack(pady=50)
            return

        # Patient selection
        customtkinter.CTkLabel(
            form_frame,
            text="Select Patient:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=20, pady=(20, 5))

        patient_combo = customtkinter.CTkComboBox(
            form_frame,
            values=[f"{p[0]} - {p[1]}" for p in patients],
            width=400,
            height=35,
            font=("Arial", 12)
        )
        patient_combo.pack(anchor="w", padx=20, pady=(0, 20))
        if patients:
            patient_combo.set(f"{patients[0][0]} - {patients[0][1]}")

        # SCROLLABLE VITALS FORM
        vitals_scroll = customtkinter.CTkScrollableFrame(form_frame, height=400)
        vitals_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Blood Pressure
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Blood Pressure (e.g., 120/80):",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=10, pady=(10, 0))
        bp_entry = customtkinter.CTkEntry(
            vitals_scroll,
            placeholder_text="Enter blood pressure",
            width=300,
            height=35
        )
        bp_entry.pack(anchor="w", padx=10, pady=(5, 10))

        # Temperature
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Temperature (°C):",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=10, pady=(0, 0))
        temp_entry = customtkinter.CTkEntry(
            vitals_scroll,
            placeholder_text="Enter temperature",
            width=300,
            height=35
        )
        temp_entry.pack(anchor="w", padx=10, pady=(5, 10))

        # Weight
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Weight (kg):",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=10, pady=(0, 0))
        weight_entry = customtkinter.CTkEntry(
            vitals_scroll,
            placeholder_text="Enter weight",
            width=300,
            height=35
        )
        weight_entry.pack(anchor="w", padx=10, pady=(5, 10))

        # Additional Notes
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Additional Notes:",
            font=("Arial", 12, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=10, pady=(10, 0))
        notes_text = customtkinter.CTkTextbox(
            vitals_scroll,
            height=80,
            font=("Arial", 11)
        )
        notes_text.pack(anchor="w", padx=10, pady=(5, 20))

        # Mode selection
        mode_var = customtkinter.StringVar(value="add")
        mode_frame = customtkinter.CTkFrame(vitals_scroll, fg_color="transparent")
        mode_frame.pack(anchor="w", padx=10, pady=10)
        add_radio = customtkinter.CTkRadioButton(
            mode_frame,
            text="Add New Record",
            variable=mode_var,
            value="add"
        )
        add_radio.pack(side="left", padx=(0, 20))
        update_radio = customtkinter.CTkRadioButton(
            mode_frame,
            text="Update Latest Record",
            variable=mode_var,
            value="update"
        )
        update_radio.pack(side="left")

        # FIXED: Save button with proper error handling
        def save_vitals():
            selection = patient_combo.get()
            if not selection:
                messagebox.showerror("Error", "Please select a patient")
                return
            
            try:
                patient_id = selection.split(" - ")[0].strip()
                bp = bp_entry.get().strip()
                temp = temp_entry.get().strip()
                weight = weight_entry.get().strip()
                notes = notes_text.get("1.0", "end-1c").strip()
                
                if not any([bp, temp, weight]):
                    messagebox.showerror("Error", "Please enter at least one vital sign")
                    return
                
                # Validate numeric inputs
                temp_val = None
                weight_val = None
                
                if temp:
                    try:
                        temp_val = float(temp)
                        if temp_val < 30 or temp_val > 50:
                            messagebox.showerror("Error", "Temperature must be between 30-50°C")
                            return
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid temperature")
                        return
                
                if weight:
                    try:
                        weight_val = float(weight)
                        if weight_val < 1 or weight_val > 500:
                            messagebox.showerror("Error", "Weight must be between 1-500 kg")
                            return
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid weight")
                        return
                
                if mode_var.get() == "add":
                    self.cursor.execute("""
                        INSERT INTO treatments (patient_id, blood_pressure, temperature, weight, notes, date)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                    """, (patient_id, bp if bp else None, temp_val, weight_val, notes if notes else None))
                    message = "Vitals recorded successfully!"
                    log_message = f"Added vitals for patient ID: {patient_id}"
                else:
                    # Update mode
                    self.cursor.execute("""
                        SELECT treatment_id FROM treatments 
                        WHERE patient_id = %s 
                        ORDER BY date DESC LIMIT 1
                    """, (patient_id,))
                    result = self.cursor.fetchone()
                    if not result:
                        messagebox.showerror("Error", "No previous record found to update")
                        return
                    self.cursor.execute("""
                        UPDATE treatments 
                        SET blood_pressure = %s, temperature = %s, weight = %s, notes = %s, date = NOW()
                        WHERE treatment_id = %s
                    """, (bp if bp else None, temp_val, weight_val, notes if notes else None, result[0]))
                    message = "Latest vitals updated successfully!"
                    log_message = f"Updated vitals for patient ID: {patient_id}"
                
                self.conn.commit()
                messagebox.showinfo("Success", message)
                
                # Log the action
                try:
                    log_action(self.username, "Nurse", log_message)
                except Exception as log_err:
                    print(f"Logging error: {log_err}")
                
                # Clear form
                bp_entry.delete(0, 'end')
                temp_entry.delete(0, 'end')
                weight_entry.delete(0, 'end')
                notes_text.delete("1.0", "end")
                
            except Exception as e:
                print(f"Database error saving vitals: {e}")
                messagebox.showerror("Database Error", f"Error saving vitals: {str(e)}")

        save_button = customtkinter.CTkButton(
            vitals_scroll,
            text="Save Vitals",
            command=save_vitals,
            height=50,
            width=250,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['accent'],
            hover_color="#219a52"
        )
        save_button.pack(pady=30)

    def show_view_vitals(self):
        """View patient vitals with enhanced interface"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="View Patient Vitals & History",
            font=("Arial", 20, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")

        # Get patients
        try:
            self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
            patients = self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting patients for view: {e}")
            patients = []

        if not patients:
            customtkinter.CTkLabel(
                self.content,
                text="No patients found",
                font=("Arial", 16),
                text_color=self.colors['danger']
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
            width=400,
            height=35,
            command=lambda _: show_patient_vitals()
        )
        patient_combo.pack(anchor="w", padx=20, pady=(0, 20))

        # Display area for vitals
        display_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['light_gray'])
        display_frame.pack(fill="both", expand=True, padx=20, pady=20)

        def show_patient_vitals():
            """Display selected patient's vitals"""
            # Clear display area
            for widget in display_frame.winfo_children():
                widget.destroy()

            selection = patient_combo.get()
            if not selection:
                return

            patient_id = selection.split(" - ")[0]
            patient_name = selection.split(" - ")[1]

            # Patient header
            header_frame = customtkinter.CTkFrame(display_frame, fg_color=self.colors['primary'])
            header_frame.pack(fill="x", padx=20, pady=20)
            
            customtkinter.CTkLabel(
                header_frame,
                text=f"Patient: {patient_name} (ID: {patient_id})",
                font=("Arial", 16, "bold"),
                text_color="white"
            ).pack(pady=15)

            try:
                # Get all vitals for this patient
                self.cursor.execute("""
                    SELECT blood_pressure, temperature, weight, notes, date
                    FROM treatments 
                    WHERE patient_id = %s AND (blood_pressure IS NOT NULL OR temperature IS NOT NULL OR weight IS NOT NULL)
                    ORDER BY date DESC
                """, (patient_id,))
                
                vitals = self.cursor.fetchall()

                if not vitals:
                    customtkinter.CTkLabel(
                        display_frame,
                        text="No vitals recorded for this patient",
                        font=("Arial", 14),
                        text_color=self.colors['text_dark']
                    ).pack(pady=20)
                    return

                # Show latest vitals first
                latest = vitals[0]
                latest_frame = customtkinter.CTkFrame(display_frame, fg_color=self.colors['white'])
                latest_frame.pack(fill="x", padx=20, pady=10)

                customtkinter.CTkLabel(
                    latest_frame,
                    text="Latest Vitals:",
                    font=("Arial", 14, "bold"),
                    text_color=self.colors['text_dark']
                ).pack(anchor="w", padx=20, pady=(15, 10))

                # Display each vital sign
                vital_info = []
                if latest[0]:  # Blood pressure
                    vital_info.append(f"Blood Pressure: {latest[0]}")
                if latest[1]:  # Temperature
                    vital_info.append(f"Temperature: {latest[1]}°C")
                if latest[2]:  # Weight
                    vital_info.append(f"Weight: {latest[2]} kg")

                for info in vital_info:
                    customtkinter.CTkLabel(
                        latest_frame,
                        text=info,
                        font=("Arial", 12),
                        text_color=self.colors['text_dark']
                    ).pack(anchor="w", padx=20, pady=2)

                if latest[3]:  # Notes
                    customtkinter.CTkLabel(
                        latest_frame,
                        text=f"Notes: {latest[3]}",
                        font=("Arial", 12),
                        text_color=self.colors['text_dark'],
                        wraplength=400
                    ).pack(anchor="w", padx=20, pady=(5, 10))

                customtkinter.CTkLabel(
                    latest_frame,
                    text=f"Date: {latest[4]}",
                    font=("Arial", 11, "italic"),
                    text_color="#7f8c8d"
                ).pack(anchor="w", padx=20, pady=(0, 15))

                # Show history if more than one record
                if len(vitals) > 1:
                    history_frame = customtkinter.CTkFrame(display_frame, fg_color=self.colors['white'])
                    history_frame.pack(fill="both", expand=True, padx=20, pady=10)

                    customtkinter.CTkLabel(
                        history_frame,
                        text="Vitals History:",
                        font=("Arial", 14, "bold"),
                        text_color=self.colors['text_dark']
                    ).pack(anchor="w", padx=20, pady=(15, 10))

                    # Create scrollable area for history
                    history_scroll = customtkinter.CTkScrollableFrame(history_frame, height=200)
                    history_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

                    for vital in vitals[1:]:  # Skip the first one (already shown as latest)
                        record_frame = customtkinter.CTkFrame(history_scroll, fg_color=self.colors['light_green'])
                        record_frame.pack(fill="x", pady=5)

                        # Build record text
                        record_text = f"Date: {vital[4]}\n"
                        if vital[0]: record_text += f"BP: {vital[0]} | "
                        if vital[1]: record_text += f"Temp: {vital[1]}°C | "
                        if vital[2]: record_text += f"Weight: {vital[2]}kg"
                        
                        record_text = record_text.rstrip(" | ")
                        
                        if vital[3]:  # Notes
                            record_text += f"\nNotes: {vital[3]}"

                        customtkinter.CTkLabel(
                            record_frame,
                            text=record_text,
                            font=("Arial", 11),
                            justify="left",
                            text_color=self.colors['text_dark']
                        ).pack(anchor="w", padx=15, pady=10)

            except Exception as e:
                print(f"Error loading patient vitals: {e}")
                customtkinter.CTkLabel(
                    display_frame,
                    text=f"Error loading vitals: {str(e)}",
                    font=("Arial", 12),
                    text_color=self.colors['danger']
                ).pack(pady=20)

        # Show first patient by default
        if patients:
            patient_combo.set(f"{patients[0][0]} - {patients[0][1]}")
            show_patient_vitals()

    def show_patient_notes(self):
        """Enhanced patient notes interface"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="Patient Notes Management",
            font=("Arial", 20, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w")

        # Get patients
        try:
            self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
            patients = self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting patients for notes: {e}")
            patients = []

        if not patients:
            customtkinter.CTkLabel(
                self.content,
                text="No patients found",
                font=("Arial", 16),
                text_color=self.colors['danger']
            ).pack(pady=50)
            return

        # Check if patient_notes table exists, if not create it
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS patient_notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT,
                    notes TEXT,
                    author VARCHAR(100),
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    emergency BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            self.conn.commit()
        except Exception as e:
            print(f"Error creating patient_notes table: {e}")

        # Form frame
        form_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Patient selection
        customtkinter.CTkLabel(
            form_frame,
            text="Select Patient:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=20, pady=(20, 5))

        patient_combo = customtkinter.CTkComboBox(
            form_frame,
            values=[f"{p[0]} - {p[1]}" for p in patients],
            width=400,
            height=35
        )
        patient_combo.pack(anchor="w", padx=20, pady=(0, 20))

        # Notes input
        customtkinter.CTkLabel(
            form_frame,
            text="Write Notes:",
            font=("Arial", 14, "bold"),
            text_color=self.colors['text_dark']
        ).pack(anchor="w", padx=20, pady=(10, 5))

        notes_text = customtkinter.CTkTextbox(
            form_frame,
            height=120,
            width=500,
            font=("Arial", 11)
        )
        notes_text.pack(anchor="w", padx=20, pady=(0, 20))

        # Emergency checkbox
        emergency_var = customtkinter.BooleanVar()
        emergency_check = customtkinter.CTkCheckBox(
            form_frame,
            text="Mark as Emergency",
            variable=emergency_var,
            font=("Arial", 12, "bold"),
            text_color=self.colors['danger']
        )
        emergency_check.pack(anchor="w", padx=20, pady=10)

        # Save button
        def save_notes():
            selection = patient_combo.get()
            notes = notes_text.get("1.0", "end-1c").strip()
            
            if not selection or not notes:
                messagebox.showerror("Error", "Please select a patient and write a note")
                return
            
            patient_id = selection.split(" - ")[0]
            
            try:
                self.cursor.execute("""
                    INSERT INTO patient_notes (patient_id, notes, author, date, emergency)
                    VALUES (%s, %s, %s, NOW(), %s)
                """, (patient_id, notes, self.username, emergency_var.get()))
                
                self.conn.commit()
                
                if emergency_var.get():
                    messagebox.showwarning("Emergency Notes Saved", 
                        "EMERGENCY notes saved successfully!\nAll medical staff will be notified.")
                else:
                    messagebox.showinfo("Success", "Notes saved successfully!")
                
                # Clear form
                notes_text.delete("1.0", "end")
                emergency_var.set(False)
                
                try:
                    log_action(self.username, "Nurse", f"Added {'EMERGENCY' if emergency_var.get() else ''} notes for patient ID: {patient_id}")
                except Exception as log_err:
                    print(f"Logging error: {log_err}")
                    
            except Exception as e:
                print(f"Error saving notes: {e}")
                messagebox.showerror("Error", f"Error saving notes: {str(e)}")

        save_btn = customtkinter.CTkButton(
            form_frame,
            text="Save Notes",
            command=save_notes,
            height=45,
            width=200,
            font=("Arial", 14, "bold"),
            fg_color=self.colors['accent']
        )
        save_btn.pack(pady=20)

    def show_emergency_cases(self):
        """Enhanced emergency cases display"""
        self.clear_content()
        
        title_frame = customtkinter.CTkFrame(self.content, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=20)
        
        customtkinter.CTkLabel(
            title_frame,
            text="Emergency Cases Management",
            font=("Arial", 20, "bold"),
            text_color=self.colors['danger']
        ).pack(anchor="w")

        # Emergency cases frame
        emergency_frame = customtkinter.CTkFrame(self.content, fg_color=self.colors['white'])
        emergency_frame.pack(fill="both", expand=True, padx=20, pady=20)

        try:
            # Check if table exists first
            self.cursor.execute("SHOW TABLES LIKE 'patient_notes'")
            table_exists = self.cursor.fetchone()
            
            if not table_exists:
                customtkinter.CTkLabel(
                    emergency_frame,
                    text="Emergency notes system is not set up yet.\nUse 'Patient Notes' to create emergency notes first.",
                    font=("Arial", 16),
                    text_color=self.colors['info']
                ).pack(pady=50)
                return
            
            self.cursor.execute("""
                SELECT pn.notes, pn.date, p.name, p.patient_id, pn.author
                FROM patient_notes pn
                JOIN patients p ON pn.patient_id = p.patient_id
                WHERE pn.emergency = TRUE
                ORDER BY pn.date DESC
                LIMIT 20
            """)
            
            emergencies = self.cursor.fetchall()

            if emergencies:
                # Statistics
                import datetime
                today_count = sum(1 for e in emergencies if e[1].date() == datetime.date.today())
                
                stats_frame = customtkinter.CTkFrame(emergency_frame, fg_color=self.colors['danger'])
                stats_frame.pack(fill="x", padx=20, pady=20)
                
                customtkinter.CTkLabel(
                    stats_frame,
                    text=f"Emergency Cases: {today_count} today | {len(emergencies)} total recent",
                    font=("Arial", 16, "bold"),
                    text_color="white"
                ).pack(pady=15)

                customtkinter.CTkLabel(
                    emergency_frame,
                    text="Recent Emergency Cases:",
                    font=("Arial", 16, "bold"),
                    text_color=self.colors['text_dark']
                ).pack(anchor="w", padx=20, pady=(10, 10))

                # Scrollable frame for emergencies
                scroll_frame = customtkinter.CTkScrollableFrame(emergency_frame, height=300)
                scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

                for notes, date, patient_name, patient_id, author in emergencies:
                    import datetime
                    is_today = date.date() == datetime.date.today()
                    case_color = self.colors['danger'] if is_today else "#e67e22"
                    
                    case_frame = customtkinter.CTkFrame(scroll_frame, fg_color=case_color)
                    case_frame.pack(fill="x", pady=8)

                    priority_text = "TODAY - " if is_today else ""
                    
                    customtkinter.CTkLabel(
                        case_frame,
                        text=f"{priority_text}EMERGENCY - {patient_name} (ID: {patient_id})",
                        font=("Arial", 14, "bold"),
                        text_color="white"
                    ).pack(anchor="w", padx=20, pady=(15, 5))

                    customtkinter.CTkLabel(
                        case_frame,
                        text=f"Date: {date.strftime('%Y-%m-%d %H:%M')} | Reported by: {author}",
                        font=("Arial", 11),
                        text_color="white"
                    ).pack(anchor="w", padx=20, pady=2)

                    customtkinter.CTkLabel(
                        case_frame,
                        text=notes,
                        font=("Arial", 12),
                        text_color="white",
                        wraplength=500,
                        justify="left"
                    ).pack(anchor="w", padx=20, pady=(5, 15))
            else:
                customtkinter.CTkLabel(
                    emergency_frame,
                    text="No emergency cases found",
                    font=("Arial", 16),
                    text_color=self.colors['accent']
                ).pack(pady=50)

        except Exception as e:
            print(f"Error loading emergency cases: {e}")
            customtkinter.CTkLabel(
                emergency_frame,
                text=f"Error loading emergency cases: {str(e)}",
                font=("Arial", 14),
                text_color=self.colors['danger']
            ).pack(pady=50)

    def logout(self):
        """Enhanced logout with confirmation"""
        result = messagebox.askyesno(
            "Logout Confirmation", 
            f"Are you sure you want to logout, Nurse {self.username}?\n\nAll unsaved work will be lost."
        )
        if result:
            try:
                log_action(self.username, "Nurse", "Logged out from nursing system")
                self.conn.close()
            except Exception as e:
                print(f"Logout error: {e}")
            messagebox.showinfo("Goodbye", f"Thank you for your dedication, Nurse {self.username}!")
            self.master.destroy()
            if self.on_logout:
                self.on_logout()