import customtkinter
from tkinter import messagebox
from db_connection import get_connection

class AdminFrame(customtkinter.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # Layout: Sidebar and Main Content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = customtkinter.CTkFrame(self, width=180, fg_color="#2e3f4f")
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        customtkinter.CTkLabel(self.sidebar, text="Admin", font=("Arial", 18, "bold"),
                               fg_color="#2e3f4f", text_color="white").pack(pady=(30, 20))
        customtkinter.CTkButton(self.sidebar, text="Dashboard Home", command=self.show_welcome).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="View System Logs", command=self.show_logs).pack(fill="x", padx=20, pady=5)
        customtkinter.CTkButton(self.sidebar, text="Logout", command=self.logout).pack(side="bottom", fill="x", padx=20, pady=20)

        # Main content area
        self.content = customtkinter.CTkFrame(self, fg_color="white")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.show_welcome()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text=f"Welcome, Admin {self.username}!", font=("Arial", 22, "bold")).pack(pady=40)
        customtkinter.CTkLabel(self.content, text="Use the sidebar to view logs or manage the system.", font=("Arial", 14)).pack(pady=10)

    def show_logs(self):
        self.clear_content()
        customtkinter.CTkLabel(self.content, text="System Logs", font=("Arial", 18, "bold")).pack(pady=10)

        # Filter section
        filter_frame = customtkinter.CTkFrame(self.content)
        filter_frame.pack(fill="x", padx=10, pady=5)
        dept_combo = customtkinter.CTkComboBox(filter_frame, values=["All", "Receptionist", "Nurse", "Doctor"])
        dept_combo.set("All")
        dept_combo.pack(side="left", padx=5)
        date_entry = customtkinter.CTkEntry(filter_frame, placeholder_text="YYYY-MM-DD (optional)")
        date_entry.pack(side="left", padx=5)
        filter_btn = customtkinter.CTkButton(filter_frame, text="Filter", command=lambda: self.show_logs_filtered(dept_combo.get(), date_entry.get()))
        filter_btn.pack(side="left", padx=5)

        self.show_logs_filtered("All", "")

    def show_logs_filtered(self, department, date_str):
        for widget in self.content.winfo_children():
            if isinstance(widget, customtkinter.CTkFrame) and widget != self.sidebar:
                widget.destroy()
        try:
            query = "SELECT log_id, user, department, action, log_date, timestamp FROM logs"
            params = []
            filters = []
            if department != "All":
                filters.append("department=%s")
                params.append(department)
            if date_str:
                filters.append("log_date=%s")
                params.append(date_str)
            if filters:
                query += " WHERE " + " AND ".join(filters)
            query += " ORDER BY timestamp DESC"
            self.cursor.execute(query, tuple(params))
            logs = self.cursor.fetchall()
            if not logs:
                customtkinter.CTkLabel(self.content, text="No logs found.").pack()
                return

            # Table header
            header = customtkinter.CTkFrame(self.content, fg_color="#e0e0e0")
            header.pack(fill="x", padx=10, pady=(10,2))
            for col, w in zip(["ID", "User", "Department", "Action", "Date", "Time", "Delete"], [5, 15, 15, 40, 10, 15, 10]):
                customtkinter.CTkLabel(header, text=col, width=w*10, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=2)

            for log in logs:
                frame = customtkinter.CTkFrame(self.content, fg_color="white")
                frame.pack(fill="x", padx=10, pady=1)
                for val, w in zip(log[:-1], [5, 15, 15, 40, 10]):
                    customtkinter.CTkLabel(frame, text=str(val), width=w*10, anchor="w").pack(side="left", padx=2)
                customtkinter.CTkLabel(frame, text=str(log[-1]).split()[1][:8], width=15*10, anchor="w").pack(side="left", padx=2)
                del_btn = customtkinter.CTkButton(frame, text="Delete", width=60,
                                                  command=lambda log_id=log[0]: self.delete_log(log_id))
                del_btn.pack(side="left", padx=2)
        except Exception as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def delete_log(self, log_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this log?"):
            try:
                self.cursor.execute("DELETE FROM logs WHERE log_id=%s", (log_id,))
                self.conn.commit()
                messagebox.showinfo("Deleted", "Log entry deleted.")
                self.show_logs()
            except Exception as err:
                messagebox.showerror("Database Error", f"Error: {err}")

    def logout(self):
        self.conn.close()
        self.master.destroy()