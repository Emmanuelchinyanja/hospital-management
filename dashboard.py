import customtkinter
from doctor import DoctorFrame
from nurse import NurseFrame
from receptionist import ReceptionistFrame
from admin import AdminFrame

class Dashboard(customtkinter.CTk):
    def __init__(self, username, role):
        super().__init__()
        self.title("Hospital Management Dashboard")
        self.geometry("900x600")
        self.username = username
        self.role = role

        # Clear window and load the correct module
        if role == "Doctor":
            self.module_frame = DoctorFrame(self, username)
        elif role == "Nurse":
            self.module_frame = NurseFrame(self, username)
        elif role == "Receptionist":
            self.module_frame = ReceptionistFrame(self, username)
        elif role == "Admin":
            self.module_frame = AdminFrame(self, username)
        else:
            self.module_frame = customtkinter.CTkLabel(self, text="Unknown role")
        self.module_frame.pack(fill="both", expand=True)

    def logout(self):
        self.destroy()
        if hasattr(self, 'on_logout') and callable(self.on_logout):
            self.on_logout()

if __name__ == "__main__":
    app = Dashboard("doctor1", "Doctor")
    app.mainloop()