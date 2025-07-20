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
        self.geometry("900x600")
        self.resizable(False, False)

        # --- Main frame ---
        frame = customtkinter.CTkFrame(self, corner_radius=20, width=420, height=500)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # --- Logo/Image section ---
        img_path = os.path.join(os.path.dirname(__file__), "login_illustration.png")
        if os.path.exists(img_path):
            pil_img = Image.open(img_path)
            login_img = customtkinter.CTkImage(light_image=pil_img, size=(110, 110))
            img_label = customtkinter.CTkLabel(frame, image=login_img, text="")
            img_label.pack(pady=(24, 10))
        else:
            customtkinter.CTkLabel(frame, text="Queen Elizabeth Hospital", font=("Arial", 22, "bold")).pack(pady=(24, 10))

        customtkinter.CTkLabel(frame, text="Login to your account", font=("Arial", 16)).pack(pady=(0, 18))

        # --- Username field ---
        self.username_entry = customtkinter.CTkEntry(frame, placeholder_text="Username")
        self.username_entry.pack(pady=10, fill="x", padx=40)

        # --- Password field ---
        self.password_entry = customtkinter.CTkEntry(frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10, fill="x", padx=40)

        # --- Login button ---
        login_btn = customtkinter.CTkButton(frame, text="Login", command=self.check_login)
        login_btn.pack(pady=18)

        # --- Show/hide password toggle ---
        self.show_password = False
        toggle_btn = customtkinter.CTkButton(frame, text="Show Password", width=120, command=self.toggle_password)
        toggle_btn.pack(pady=(0, 8))
        self.toggle_btn = toggle_btn

        # --- Status/Error message ---
        self.status_label = customtkinter.CTkLabel(frame, text="", text_color="red", font=("Arial", 12))
        self.status_label.pack(pady=(0, 5))

        # --- Contact Info & Footer ---
        contact_frame = customtkinter.CTkFrame(self, fg_color="transparent", width=420)
        contact_frame.place(relx=0.5, rely=1.0, anchor="s", y=-10)
        customtkinter.CTkLabel(
            contact_frame,
            text="Contact: +265 1 234 567 | Email: info@qehospital.mw",
            font=("Arial", 12),
            text_color="#555"
        ).pack()
        customtkinter.CTkLabel(
            contact_frame,
            text="Queen Elizabeth Hospital, Blantyre, Malawi",
            font=("Arial", 12, "italic"),
            text_color="#888"
        ).pack()
        customtkinter.CTkLabel(
            contact_frame,
            text="© 2025 Queen Elizabeth Hospital Management System",
            font=("Arial", 11),
            text_color="#aaa"
        ).pack(pady=(5, 0))

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="Hide Password")
        else:
            self.password_entry.configure(show="*")
            self.toggle_btn.configure(text="Show Password")

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            self.status_label.configure(text="Please enter both username and password.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            conn.close()
            if result:
                role = result[0]
                self.status_label.configure(text="")
                self.withdraw()  # Hide login window
                app = Dashboard(username, role)
                app.on_logout = self.restart_login
                app.mainloop()
            else:
                self.status_label.configure(text="Invalid username or password.")
        except Exception as err:
            self.status_label.configure(text=f"Database Error: {err}")

    def restart_login(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.status_label.configure(text="")
        self.deiconify()  # Show login window again

if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    login = LoginPage()
    login.mainloop()