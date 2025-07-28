import customtkinter
from tkinter import messagebox
from db_connection import get_connection, log_action
import datetime

class NurseFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # Simple layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.content = customtkinter.CTkFrame(self, fg_color="#f0f0f0")
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Show welcome screen
        self.show_welcome()

    def create_sidebar(self):
        """Create simple sidebar"""
        self.sidebar = customtkinter.CTkFrame(self, width=200, fg_color="#2e3f4f")
        self.sidebar.grid(row=0, column=0, sticky="ns", padx=(10, 5), pady=10)
        self.sidebar.grid_propagate(False)

        # Title
        customtkinter.CTkLabel(
            self.sidebar, 
            text="Queen Elizabeth Hospital", 
            font=("Arial", 14, "bold"), 
            text_color="white"
        ).pack(pady=(20, 10))
        
        customtkinter.CTkLabel(
            self.sidebar, 
            text=f"Nurse: {self.username}", 
            font=("Arial", 12), 
            text_color="lightgray"
        ).pack(pady=(0, 20))

        # Navigation buttons
        buttons = [
            ("Dashboard", self.show_welcome),
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
                font=("Arial", 12)
            )
            btn.pack(fill="x", padx=15, pady=5)

        # Logout button
        customtkinter.CTkButton(
            self.sidebar,
            text="Logout",
            command=self.logout,
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="bottom", fill="x", padx=15, pady=20)

    def clear_content(self):
        """Clear main content area"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        """Simple welcome screen"""
        self.clear_content()
        
        # Title
        customtkinter.CTkLabel(
            self.content,
            text=f"Welcome, Nurse {self.username}!",
            font=("Arial", 24, "bold")
        ).pack(pady=40)
        
        customtkinter.CTkLabel(
            self.content,
            text="Queen Elizabeth Hospital - Nursing Station",
            font=("Arial", 16)
        ).pack(pady=10)
        
        # Quick stats
        stats_frame = customtkinter.CTkFrame(self.content)
        stats_frame.pack(pady=30)
        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM treatments WHERE DATE(date) = CURDATE()")
            today_vitals = self.cursor.fetchone()[0]
        except:
            total_patients = 0
            today_vitals = 0
        
        customtkinter.CTkLabel(
            stats_frame,
            text=f"Total Patients: {total_patients}",
            font=("Arial", 14)
        ).pack(pady=10, padx=20)
        
        customtkinter.CTkLabel(
            stats_frame,
            text=f"Vitals Recorded Today: {today_vitals}",
            font=("Arial", 14)
        ).pack(pady=10, padx=20)

    def show_record_vitals(self):
        """Record patient vitals with notes and save button (beginner friendly)"""
        self.clear_content()
        
        # Title
        customtkinter.CTkLabel(
            self.content,
            text="Record Patient Vitals",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Main form frame
        form_frame = customtkinter.CTkFrame(self.content)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Get patients from database
        try:
            self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
            patients = self.cursor.fetchall()
        except:
            patients = []

        if not patients:
            customtkinter.CTkLabel(
                form_frame,
                text="No patients found in database",
                font=("Arial", 16)
            ).pack(pady=50)
            return

        # Patient selection
        customtkinter.CTkLabel(
            form_frame,
            text="Select Patient:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        patient_combo = customtkinter.CTkComboBox(
            form_frame,
            values=[f"{p[0]} - {p[1]}" for p in patients],
            width=400
        )
        patient_combo.pack(anchor="w", padx=20, pady=(0, 20))
        patient_combo.set(f"{patients[0][0]} - {patients[0][1]}")

        # --- SCROLLABLE VITALS FORM ---
        vitals_scroll = customtkinter.CTkScrollableFrame(form_frame, height=400)
        vitals_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # Blood Pressure
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Blood Pressure (e.g., 120/80):",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=(10, 0))
        bp_entry = customtkinter.CTkEntry(
            vitals_scroll,
            placeholder_text="Enter blood pressure",
            width=300
        )
        bp_entry.pack(anchor="w", padx=10, pady=(5, 10))

        # Temperature
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Temperature (°C):",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=(0, 0))
        temp_entry = customtkinter.CTkEntry(
            vitals_scroll,
            placeholder_text="Enter temperature",
            width=300
        )
        temp_entry.pack(anchor="w", padx=10, pady=(5, 10))

        # Weight
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Weight (kg):",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=(0, 0))
        weight_entry = customtkinter.CTkEntry(
            vitals_scroll,
            placeholder_text="Enter weight",
            width=300
        )
        weight_entry.pack(anchor="w", padx=10, pady=(5, 10))

        # Heart Rate
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Heart Rate (bpm):",
            font=("Arial", 12)
        ).pack(anchor="w", padx=10, pady=(0, 0))
        hr_entry = customtkinter.CTkEntry(
            vitals_scroll,
            placeholder_text="Enter heart rate",
            width=300
        )
        hr_entry.pack(anchor="w", padx=10, pady=(5, 10))

        # Additional Notes
        customtkinter.CTkLabel(
            vitals_scroll,
            text="Additional Notes:",
            font=("Arial", 12)
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

        # Save button
        def save_vitals():
            selection = patient_combo.get()
            if not selection:
                messagebox.showerror("Error", "Please select a patient")
                return
            patient_id = selection.split(" - ")[0].strip()
            bp = bp_entry.get().strip()
            temp = temp_entry.get().strip()
            weight = weight_entry.get().strip()
            hr = hr_entry.get().strip()
            notes = notes_text.get("1.0", "end-1c").strip()
            if not any([bp, temp, weight, hr]):
                messagebox.showerror("Error", "Please enter at least one vital sign")
                return
            try:
                temp_val = float(temp) if temp else None
                weight_val = float(weight) if weight else None
                hr_val = int(hr) if hr else None
                if mode_var.get() == "add":
                    self.cursor.execute("""
                        INSERT INTO treatments (patient_id, blood_pressure, temperature, weight)
                        VALUES (%s, %s, %s, %s)
                    """, (patient_id, bp or None, temp_val, weight_val))
                    message = "Vitals recorded successfully!"
                    log_message = f"Added vitals for patient ID: {patient_id}"
                else:
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
                        SET blood_pressure = %s, temperature = %s, weight = %s, 
                            heart_rate = %s, notes = %s
                        WHERE treatment_id = %s
                    """, (bp or None, temp_val, weight_val, hr_val, notes or None, result[0]))
                    message = "Latest vitals updated successfully!"
                    log_message = f"Updated vitals for patient ID: {patient_id}"
                self.conn.commit()
                messagebox.showinfo("Success", message)
                try:
                    log_action(self.username, "Nurse", log_message)
                except:
                    pass
                bp_entry.delete(0, 'end')
                temp_entry.delete(0, 'end')
                weight_entry.delete(0, 'end')
                hr_entry.delete(0, 'end')
                notes_text.delete("1.0", "end")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for temperature, weight, and heart rate")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error saving vitals: {str(e)}")

        save_button = customtkinter.CTkButton(
            vitals_scroll,
            text="Save Vitals",
            command=save_vitals,
            height=40,
            width=200,
            font=("Arial", 14, "bold"),
            fg_color="#27ae60",
            hover_color="#219a52"
        )
        save_button.pack(pady=30)

    def show_view_vitals(self):
        """FIXED - View patient vitals with proper data display"""
        self.clear_content()
        
        customtkinter.CTkLabel(
            self.content,
            text="View Patient Vitals & History",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Get patients
        try:
            self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
            patients = self.cursor.fetchall()
        except:
            patients = []

        if not patients:
            customtkinter.CTkLabel(
                self.content,
                text="No patients found",
                font=("Arial", 16)
            ).pack(pady=50)
            return

        # Patient selection
        selection_frame = customtkinter.CTkFrame(self.content)
        selection_frame.pack(fill="x", padx=20, pady=20)

        customtkinter.CTkLabel(
            selection_frame,
            text="Select Patient:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        patient_combo = customtkinter.CTkComboBox(
            selection_frame,
            values=[f"{p[0]} - {p[1]}" for p in patients],
            width=400,
            command=lambda _: show_patient_vitals()
        )
        patient_combo.pack(anchor="w", padx=20, pady=(0, 20))

        # Display area for vitals
        display_frame = customtkinter.CTkFrame(self.content)
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
            customtkinter.CTkLabel(
                display_frame,
                text=f"Patient: {patient_name} (ID: {patient_id})",
                font=("Arial", 16, "bold")
            ).pack(pady=20)

            try:
                # Get all vitals for this patient
                self.cursor.execute("""
                    SELECT blood_pressure, temperature, weight, date
                    FROM treatments 
                    WHERE patient_id = %s 
                    ORDER BY date DESC
                """, (patient_id,))
                
                vitals = self.cursor.fetchall()

                if not vitals:
                    customtkinter.CTkLabel(
                        display_frame,
                        text="No vitals recorded for this patient",
                        font=("Arial", 14)
                    ).pack(pady=20)
                    return

                # Show latest vitals first
                latest = vitals[0]
                latest_frame = customtkinter.CTkFrame(display_frame)
                latest_frame.pack(fill="x", padx=20, pady=10)

                customtkinter.CTkLabel(
                    latest_frame,
                    text="Latest Vitals:",
                    font=("Arial", 14, "bold")
                ).pack(anchor="w", padx=20, pady=(15, 10))

                # Display each vital sign
                vital_info = []
                if latest[0]:  # Blood pressure
                    vital_info.append(f"Blood Pressure: {latest[0]}")
                if latest[1]:  # Temperature
                    vital_info.append(f"Temperature: {latest[1]}°C")
                if latest[2]:  # Weight
                    vital_info.append(f"Weight: {latest[2]} kg")
                if latest[3]:  # Heart rate
                    vital_info.append(f"Heart Rate: {latest[3]} bpm")

                for info in vital_info:
                    customtkinter.CTkLabel(
                        latest_frame,
                        text=info,
                        font=("Arial", 12)
                    ).pack(anchor="w", padx=20, pady=2)

                if latest[4]:  # Notes
                    customtkinter.CTkLabel(
                        latest_frame,
                        text=f"Notes: {latest[4]}",
                        font=("Arial", 12),
                        wraplength=400
                    ).pack(anchor="w", padx=20, pady=(5, 10))

                customtkinter.CTkLabel(
                    latest_frame,
                    text=f"Date: {latest[5]}",
                    font=("Arial", 11, "italic")
                ).pack(anchor="w", padx=20, pady=(0, 15))

                # Show history if more than one record
                if len(vitals) > 1:
                    history_frame = customtkinter.CTkFrame(display_frame)
                    history_frame.pack(fill="both", expand=True, padx=20, pady=10)

                    customtkinter.CTkLabel(
                        history_frame,
                        text="Vitals History:",
                        font=("Arial", 14, "bold")
                    ).pack(anchor="w", padx=20, pady=(15, 10))

                    # Create scrollable area for history
                    history_scroll = customtkinter.CTkScrollableFrame(history_frame, height=200)
                    history_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

                    for vital in vitals[1:]:  # Skip the first one (already shown as latest)
                        record_frame = customtkinter.CTkFrame(history_scroll)
                        record_frame.pack(fill="x", pady=5)

                        # Build record text
                        record_text = f"Date: {vital[5]}\n"
                        if vital[0]: record_text += f"BP: {vital[0]} | "
                        if vital[1]: record_text += f"Temp: {vital[1]}°C | "
                        if vital[2]: record_text += f"Weight: {vital[2]}kg | "
                        if vital[3]: record_text += f"HR: {vital[3]}bpm"
                        
                        record_text = record_text.rstrip(" | ")
                        
                        if vital[4]:  # Notes
                            record_text += f"\nNotes: {vital[4]}"

                        customtkinter.CTkLabel(
                            record_frame,
                            text=record_text,
                            font=("Arial", 11),
                            justify="left"
                        ).pack(anchor="w", padx=15, pady=10)

            except Exception as e:
                customtkinter.CTkLabel(
                    display_frame,
                    text=f"Error loading vitals: {str(e)}",
                    font=("Arial", 12)
                ).pack(pady=20)

        # Bind selection event
        # patient_combo.bind("<<ComboboxSelected>>", lambda e: show_patient_vitals())

        # Show first patient by default
        if patients:
            patient_combo.set(f"{patients[0][0]} - {patients[0][1]}")
            show_patient_vitals()

    def show_patient_notes(self):
        """Patient notes interface"""
        self.clear_content()
        
        customtkinter.CTkLabel(
            self.content,
            text="Patient Notes",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Get patients
        try:
            self.cursor.execute("SELECT patient_id, name FROM patients ORDER BY name")
            patients = self.cursor.fetchall()
        except:
            patients = []

        if not patients:
            customtkinter.CTkLabel(
                self.content,
                text="No patients found",
                font=("Arial", 16)
            ).pack(pady=50)
            return

        # Form frame
        form_frame = customtkinter.CTkFrame(self.content)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Patient selection
        customtkinter.CTkLabel(
            form_frame,
            text="Select Patient:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 5))

        patient_combo = customtkinter.CTkComboBox(
            form_frame,
            values=[f"{p[0]} - {p[1]}" for p in patients],
            width=400
        )
        patient_combo.pack(anchor="w", padx=20, pady=(0, 20))

        # Note input
        customtkinter.CTkLabel(
            form_frame,
            text="Write Note:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        notes_text = customtkinter.CTkTextbox(
            form_frame,
            height=80,
            font=("Arial", 11)
        )
        notes_text.pack(anchor="w", padx=20, pady=(0, 20))

        # Emergency checkbox
        emergency_var = customtkinter.BooleanVar()
        emergency_check = customtkinter.CTkCheckBox(
            form_frame,
            text="Mark as Emergency",
            variable=emergency_var,
            font=("Arial", 12)
        )
        emergency_check.pack(anchor="w", padx=20, pady=10)

        # Save button
        def save_note():
            selection = patient_combo.get()
            note = notes_text.get("1.0", "end-1c").strip()
            
            if not selection or not note:
                messagebox.showerror("Error", "Please select a patient and write a note")
                return
            
            patient_id = selection.split(" - ")[0]
            
            try:
                self.cursor.execute("""
                    INSERT INTO patient_notes (patient_id, note, author, date, emergency)
                    VALUES (%s, %s, %s, %s, %s)
                """, (patient_id, note, self.username, datetime.datetime.now(), emergency_var.get()))
                
                self.conn.commit()
                messagebox.showinfo("Success", "Note saved successfully!")
                
                # Clear form
                notes_text.delete("1.0", "end")
                emergency_var.set(False)
                
                try:
                    log_action(self.username, "Nurse", f"Added note for patient ID: {patient_id}")
                except:
                    pass
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error saving note: {str(e)}")

        customtkinter.CTkButton(
            form_frame,
            text="Save Note",
            command=save_note,
            height=40,
            width=150,
            fg_color="#27ae60"
        ).pack(pady=20)

    def show_emergency_cases(self):
        """Show emergency cases"""
        self.clear_content()
        
        customtkinter.CTkLabel(
            self.content,
            text="Emergency Cases",
            font=("Arial", 20, "bold"),
            text_color="#e74c3c"
        ).pack(pady=20)

        # Emergency cases frame
        emergency_frame = customtkinter.CTkFrame(self.content)
        emergency_frame.pack(fill="both", expand=True, padx=20, pady=20)

        try:
            self.cursor.execute("""
                SELECT pn.note, pn.date, p.name, p.patient_id
                FROM patient_notes pn
                JOIN patients p ON pn.patient_id = p.patient_id
                WHERE pn.emergency = TRUE
                ORDER BY pn.date DESC
                LIMIT 10
            """)
            
            emergencies = self.cursor.fetchall()

            if emergencies:
                customtkinter.CTkLabel(
                    emergency_frame,
                    text="Recent Emergency Cases:",
                    font=("Arial", 16, "bold")
                ).pack(anchor="w", padx=20, pady=(20, 10))

                # Scrollable frame for emergencies
                scroll_frame = customtkinter.CTkScrollableFrame(emergency_frame)
                scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

                for note, date, patient_name, patient_id in emergencies:
                    case_frame = customtkinter.CTkFrame(scroll_frame, fg_color="#e74c3c")
                    case_frame.pack(fill="x", pady=10)

                    customtkinter.CTkLabel(
                        case_frame,
                        text=f"EMERGENCY - {patient_name} (ID: {patient_id})",
                        font=("Arial", 14, "bold"),
                        text_color="white"
                    ).pack(anchor="w", padx=20, pady=(15, 5))

                    customtkinter.CTkLabel(
                        case_frame,
                        text=f"Date: {date}",
                        font=("Arial", 11),
                        text_color="white"
                    ).pack(anchor="w", padx=20)

                    customtkinter.CTkLabel(
                        case_frame,
                        text=note,
                        font=("Arial", 12),
                        text_color="white",
                        wraplength=500,
                        justify="left"
                    ).pack(anchor="w", padx=20, pady=(5, 15))
            else:
                customtkinter.CTkLabel(
                    emergency_frame,
                    text="No emergency cases found",
                    font=("Arial", 16)
                ).pack(pady=50)

        except Exception as e:
            customtkinter.CTkLabel(
                emergency_frame,
                text=f"Error loading emergency cases: {str(e)}",
                font=("Arial", 14)
            ).pack(pady=50)

    def logout(self):
        """Logout with confirmation"""
        result = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
        if result:
            try:
                log_action(self.username, "Nurse", "Logged out")
                self.conn.close()
            except:
                pass
            self.master.destroy()

        # Debugging: Show treatment table structure
        self.cursor.execute("SHOW COLUMNS FROM treatments")
        print(self.cursor.fetchall())