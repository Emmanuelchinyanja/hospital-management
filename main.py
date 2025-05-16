import datetime

class AuditLog:
    def __init__(self):
        self.logs = []

    def log(self, username, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{timestamp}] {username} - {action}")

    def view_logs(self):
        if not self.logs:
            print("No audit logs found.")
        else:
            print("\n--- Audit Log ---")
            for log in self.logs:
                print(log)


class Patient:
    def __init__(self, patient_id, name, age, gender):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.treatments = []

    def add_treatment(self, treatment):
        self.treatments.append(treatment)

    def __str__(self):
        return f"ID: {self.patient_id}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}"


class HospitalSystem:
    def __init__(self):
        self.patients = []
        self.audit = AuditLog()

    def add_patient(self, username):
        patient_id = input("Enter Patient ID: ")
        name = input("Enter Name: ")
        if name.isalpha():
            print("welcome, ", name)
        age = input("Enter Age: ")
        gender = input("Enter Gender (M/F): ")

        patient = Patient(patient_id, name, int(age), gender)
        self.patients.append(patient)
        self.audit.log(username, f"Added new patient {patient_id}")


    def view_patients(self):
        if not self.patients:
            print("No patient records found.")
        else:
            print("\n--- Patients ---")
            for p in self.patients:
                print(p)

    def update_patient(self, username):
        pid = input("Enter Patient ID to update: ")
        patient = self.get_patient_by_id(pid)
        if patient:
            name = input("Enter new name (leave blank to keep current): ")
            age = input("Enter new age (leave blank to keep current): ")
            gender = input("Enter new gender (leave blank to keep current): ")

            if name:
                patient.name = name
            if age:
                patient.age = int(age)
            if gender:
                patient.gender = gender

            self.audit.log(username, f"Updated patient {pid}")
            print("Patient updated.")
        else:
            print("Patient not found.")

    def add_treatment(self, username):
        pid = input("Enter Patient ID: ")
        patient = self.get_patient_by_id(pid)
        if patient:
            treatment = input("Enter treatment details: ")
            patient.add_treatment(treatment)
            self.audit.log(username, f"Added treatment for patient {pid}")
            print("Treatment added.")
        else:
            print("Patient not found.")

    def view_treatments(self):
        pid = input("Enter Patient ID to view treatments: ")
        patient = self.get_patient_by_id(pid)
        if patient:
            print(f"\n--- Treatments for {patient.name} ---")
            if not patient.treatments:
                print("No treatments found.")
            else:
                for t in patient.treatments:
                    print(f"- {t}")
        else:
            print("Patient not found.")

    def get_patient_by_id(self, pid):
        for patient in self.patients:
            if patient.patient_id == pid:
                return patient
        return None

    def run(self):
        print("=== Welcome to Hospital Management System ===")
        username = input("Enter your username: ")

        while True:
            print("\n--- Menu ---")
            print("1. Add Patient")
            print("2. View Patients")
            print("3. Update Patient Info")
            print("4. Add Treatment Record")
            print("5. View Patient Treatments")
            print("6. View Audit Logs")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_patient(username)
            elif choice == '2':
                self.view_patients()
            elif choice == '3':
                self.update_patient(username)
            elif choice == '4':
                self.add_treatment(username)
            elif choice == '5':
                self.view_treatments()
            elif choice == '6':
                self.audit.view_logs()
            elif choice == '7':
                print("Exiting system. Goodbye.")
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    system = HospitalSystem()
    system.run()
