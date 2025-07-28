import customtkinter
from tkinter import messagebox
from db_connection import get_connection
from dashboard import Dashboard
import os
from PIL import Image

class LoginPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Queen Elizabeth Hospital Management System - Login")
        self.geometry("1000x700")
        self.resizable(False, False)
        
        # Set hospital color theme
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        
        # Configure main window background
        self.configure(fg_color="#f0f8ff")  # Light blue background
        
        # Create main container
        main_container = customtkinter.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header section with hospital branding
        header_frame = customtkinter.CTkFrame(main_container, fg_color="#1e3a5f", height=120, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 30))
        header_frame.pack_propagate(False)
        
        # Hospital logo and title
        title_frame = customtkinter.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(expand=True, fill="both")
        
        # Hospital emblem/logo
        logo_frame = customtkinter.CTkFrame(title_frame, fg_color="transparent")
        logo_frame.pack(pady=15)
        
        # Try to load logo, fallback to text
        img_path = os.path.join(os.path.dirname(__file__), "hospital_logo.png")
        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                hospital_logo = customtkinter.CTkImage(light_image=pil_img, size=(60, 60))
                logo_label = customtkinter.CTkLabel(logo_frame, image=hospital_logo, text="")
                logo_label.pack(side="left", padx=(0, 15))
            except:
                pass
        
        # Hospital name and subtitle
        text_frame = customtkinter.CTkFrame(logo_frame, fg_color="transparent")
        text_frame.pack(side="left")
        
        hospital_name = customtkinter.CTkLabel(
            text_frame, 
            text="QUEEN ELIZABETH HOSPITAL", 
            font=("Arial", 28, "bold"), 
            text_color="white"
        )
        hospital_name.pack(anchor="w")
        
        subtitle = customtkinter.CTkLabel(
            text_frame, 
            text="Central Hospital • Blantyre, Malawi", 
            font=("Arial", 14), 
            text_color="#a8c8ec"
        )
        subtitle.pack(anchor="w")
        
        # Main content area
        content_frame = customtkinter.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Left side - Login form
        login_frame = customtkinter.CTkFrame(
            content_frame, 
            corner_radius=20, 
            width=450, 
            height=480,
            fg_color="white",
            border_width=2,
            border_color="#e1e8ed"
        )
        login_frame.pack(side="left", padx=(0, 20), pady=20)
        login_frame.pack_propagate(False)
        
        # Login form header
        form_header = customtkinter.CTkLabel(
            login_frame, 
            text="🏥 Staff Login Portal", 
            font=("Arial", 24, "bold"), 
            text_color="#1e3a5f"
        )
        form_header.pack(pady=(30, 10))
        
        form_subtitle = customtkinter.CTkLabel(
            login_frame, 
            text="Access Hospital Management System", 
            font=("Arial", 14), 
            text_color="#666"
        )
        form_subtitle.pack(pady=(0, 30))
        
        # Username field with icon
        username_frame = customtkinter.CTkFrame(login_frame, fg_color="transparent")
        username_frame.pack(pady=15, padx=40, fill="x")
        
        username_label = customtkinter.CTkLabel(
            username_frame, 
            text="👤 Username", 
            font=("Arial", 12, "bold"), 
            text_color="#1e3a5f"
        )
        username_label.pack(anchor="w", pady=(0, 5))
        
        self.username_entry = customtkinter.CTkEntry(
            username_frame, 
            placeholder_text="Enter your staff username",
            height=40,
            font=("Arial", 12),
            corner_radius=8,
            border_color="#1e3a5f"
        )
        self.username_entry.pack(fill="x")
        
        # Password field with icon
        password_frame = customtkinter.CTkFrame(login_frame, fg_color="transparent")
        password_frame.pack(pady=15, padx=40, fill="x")
        
        password_label = customtkinter.CTkLabel(
            password_frame, 
            text="🔒 Password", 
            font=("Arial", 12, "bold"), 
            text_color="#1e3a5f"
        )
        password_label.pack(anchor="w", pady=(0, 5))
        
        self.password_entry = customtkinter.CTkEntry(
            password_frame, 
            placeholder_text="Enter your password",
            show="*",
            height=40,
            font=("Arial", 12),
            corner_radius=8,
            border_color="#1e3a5f"
        )
        self.password_entry.pack(fill="x")
        
        # Password toggle
        self.show_password = False
        toggle_frame = customtkinter.CTkFrame(password_frame, fg_color="transparent")
        toggle_frame.pack(fill="x", pady=(5, 0))
        
        self.toggle_btn = customtkinter.CTkButton(
            toggle_frame, 
            text="👁️ Show Password", 
            width=130,
            height=25,
            font=("Arial", 10),
            fg_color="transparent",
            text_color="#1e3a5f",
            hover_color="#f0f8ff",
            command=self.toggle_password
        )
        self.toggle_btn.pack(anchor="w")
        
        # Login button
        login_btn = customtkinter.CTkButton(
            login_frame, 
            text="🔐 LOGIN TO SYSTEM", 
            command=self.check_login,
            height=45,
            width=200,
            font=("Arial", 14, "bold"),
            fg_color="#1e3a5f",
            hover_color="#2d4a6b",
            corner_radius=10
        )
        login_btn.pack(pady=25)
        
        # Status message
        self.status_label = customtkinter.CTkLabel(
            login_frame, 
            text="", 
            font=("Arial", 12), 
            text_color="#dc3545"
        )
        self.status_label.pack(pady=(0, 20))
        
        # Right side - Information panel
        info_frame = customtkinter.CTkFrame(
            content_frame, 
            corner_radius=20, 
            fg_color="#1e3a5f",
            width=450,
            height=480
        )
        info_frame.pack(side="right", padx=(20, 0), pady=20)
        info_frame.pack_propagate(False)
        
        # Info panel content
        info_title = customtkinter.CTkLabel(
            info_frame, 
            text="🏥 Hospital Information", 
            font=("Arial", 20, "bold"), 
            text_color="white"
        )
        info_title.pack(pady=(30, 20))
        
        # Hospital stats/info
        stats_frame = customtkinter.CTkFrame(info_frame, fg_color="transparent")
        stats_frame.pack(pady=20, padx=30, fill="x")
        
        info_items = [
            ("📋", "Comprehensive Patient Management"),
            ("👨‍⚕️", "Staff & Doctor Scheduling"),
            ("💊", "Pharmacy & Inventory Control"),
            ("📊", "Medical Records & Reports"),
            ("🚑", "Emergency Department Integration"),
            ("🏥", "Ward & Bed Management")
        ]
        
        for icon, text in info_items:
            item_frame = customtkinter.CTkFrame(stats_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=8)
            
            customtkinter.CTkLabel(
                item_frame, 
                text=f"{icon} {text}", 
                font=("Arial", 12), 
                text_color="#a8c8ec"
            ).pack(anchor="w")
        
        # Emergency contact
        emergency_frame = customtkinter.CTkFrame(info_frame, fg_color="#2d4a6b", corner_radius=10)
        emergency_frame.pack(pady=20, padx=30, fill="x")
        
        customtkinter.CTkLabel(
            emergency_frame, 
            text="🚨 IT Support", 
            font=("Arial", 14, "bold"), 
            text_color="white"
        ).pack(pady=(10, 5))
        
        customtkinter.CTkLabel(
            emergency_frame, 
            text="Phone: +265 1 871 911\nEmail: it.support@qech.gov.mw", 
            font=("Arial", 11), 
            text_color="#a8c8ec"
        ).pack(pady=(0, 10))
        
        # Footer
        footer_frame = customtkinter.CTkFrame(main_container, fg_color="transparent", height=60)
        footer_frame.pack(fill="x", pady=(20, 0))
        footer_frame.pack_propagate(False)
        
        footer_content = customtkinter.CTkFrame(footer_frame, fg_color="#1e3a5f", corner_radius=10)
        footer_content.pack(fill="both", expand=True)
        
        footer_text = customtkinter.CTkLabel(
            footer_content, 
            text="© 2025 Queen Elizabeth Central Hospital • Ministry of Health, Malawi • Secure Medical Information System", 
            font=("Arial", 11), 
            text_color="#a8c8ec"
        )
        footer_text.pack(expand=True)
        
        # Bind Enter key to login
        self.bind('<Return>', lambda event: self.check_login())
        self.username_entry.bind('<Return>', lambda event: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda event: self.check_login())

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="🙈 Hide Password")
        else:
            self.password_entry.configure(show="*")
            self.toggle_btn.configure(text="👁️ Show Password")

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Clear previous status
        self.status_label.configure(text="")
        
        if not username or not password:
            self.status_label.configure(text="⚠️ Please enter both username and password.", text_color="#dc3545")
            return
            
        # Show loading state
        self.status_label.configure(text="🔄 Authenticating...", text_color="#0066cc")
        self.update()
        
        try:
            self.conn = get_connection()
            self.cursor = self.conn.cursor()
            
            # More secure query (consider using hashed passwords in production)
            self.cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
            result = self.cursor.fetchone()
            self.conn.close()
            
            if result:
                role = result[0]
                self.status_label.configure(text="✅ Login successful! Loading dashboard...", text_color="#28a745")
                self.update()
                
                # Hide login window and show dashboard
                self.withdraw()
                app = Dashboard(username, role)
                app.on_logout = self.restart_login
                app.mainloop()
            else:
                self.status_label.configure(text="❌ Invalid username or password. Please try again.", text_color="#dc3545")
                
        except Exception as err:
            self.status_label.configure(text=f"🚫 Database connection error. Contact IT support.", text_color="#dc3545")
            print(f"Database Error: {err}")  # Log for debugging

    def restart_login(self):
        """Called when user logs out"""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.status_label.configure(text="")
        self.show_password = False
        self.password_entry.configure(show="*")
        self.toggle_btn.configure(text="👁️ Show Password")
        self.deiconify()  # Show login window again
        self.username_entry.focus()  # Focus on username field

    def logout(self):
        self.conn.close()
        self.cursor.close()
        # Do NOT use self.conn or self.cursor after this!

if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    login = LoginPage()
    login.mainloop()