import customtkinter
from tkinter import messagebox
from db_connection import get_connection  # <-- Use the shared connection
from dashboard import App

class LoginPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management Login")
        self.geometry("400x350")
        self.resizable(False, False)

        # Main frame
        frame = customtkinter.CTkFrame(self)
        frame.pack(padx=40, pady=40, fill="both", expand=True)

        title = customtkinter.CTkLabel(frame, text="Login", font=("Arial", 24))
        title.pack(pady=(10, 20))

        self.username_entry = customtkinter.CTkEntry(frame, placeholder_text="Username")
        self.username_entry.pack(pady=10, fill="x")
        self.password_entry = customtkinter.CTkEntry(frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10, fill="x")

        login_btn = customtkinter.CTkButton(frame, text="Login", command=self.check_login)
        login_btn.pack(pady=20)

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        try:
            conn = get_connection()  # <-- Use the shared connection
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                role = result[0]
                messagebox.showinfo("Success", f"Welcome, {role}!")
                self.destroy()
                app = App(username=username, role=role)
                app.mainloop()
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")  # or "dark"
    customtkinter.set_default_color_theme("blue")
    login = LoginPage()
    login.mainloop()