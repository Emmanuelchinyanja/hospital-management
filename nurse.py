import customtkinter

class NurseFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username

        label = customtkinter.CTkLabel(self, text=f"Nurse Dashboard - {self.username}", font=("Arial", 20))
        label.pack(pady=20)

        # Example widget
        info = customtkinter.CTkLabel(self, text="Here you can record and view patient vitals.", font=("Arial", 14))
        info.pack(pady=10)