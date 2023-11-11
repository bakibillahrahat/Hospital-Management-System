import json
from datetime import date
import random
import os

# ---------------Data Path-----------------------
userPath = "./Data/user.json"
appointmentPath = "./Data/appointment.json"
patientPath = "./Data//patient.json"
prescriptionPath = "./Data/prescription.json"

if not os.path.exists('./Data'):
    os.mkdir('./Data')

def read(path):

    try:
        with open(path, 'r') as file:
            data = json.loads(file.read())
            return data
    except FileNotFoundError:
        basicObj = {
            "admin": [
                {"name": "admin",
                        "email": "admin@gmail.com",
                        "password": "12345"}
            ],
            "doctor": []
        }
        with open(path, 'w') as file:
            if path == userPath:
                file.write(json.dumps(basicObj, indent=5))
            else:
                file.write(json.dumps([], indent=5))


def write(path, obj):
    with open(path, 'w') as allData:
        allData.write(obj)


# -----------------------Data--------------------------

userData = read(userPath)
appointmentData = read(appointmentPath)
patientData = read(patientPath)
historyData = read(prescriptionPath)

    

# --------------Auto ID Generator Functions---------------------


def autoIdGenerator(basePattern):
    random_number = random.randint(0, 300)
    id = basePattern + str(random_number)
    return id
# -----------Admin Part ------------------
# ------------------Doctor Management-----------------------
# Read Doctor Info


def read_doctor(data):
    print("\nDoctor Info")
    print("\nID\tName\t\t\tEmail\t\t\tVisit-Hour\tSpecialist\tQualification")
    for i in data['doctor']:
        print(f"{i['id'].upper()}\t{i['name'].upper()}\t\t{i['email']}\t{i['visit-hour']}\t{i['Specialist'].capitalize()}\t\t{i['qualification'].upper()}")
    print("\n")

# Add New Doctor


def add_doctor(data):
    name = input("Enter Doctor Name : ").lower()
    email = input("Enter Doctor Email: ").lower()
    password = input("Enter Doctor temporary password: ")
    visit_hour = input("Enter Visit-Hour: ")
    specialist = input("Enter the Doctor Specialization: ").lower()
    qualification = input("Enter Doctor Qualification: ").lower()

    doctor_obj = {
        "id": autoIdGenerator('d-'),
        "name": name,
        "email": email,
        "password": password,
        "visit-hour": visit_hour,
        "Specialist": specialist,
        "qualification": qualification
    }
    data['doctor'].append(doctor_obj)
    userData_json_obj = json.dumps(data, indent=5)
    write(userPath, userData_json_obj)
# Update Doctor


def update_doctor(data):
    doctor_id = input(
        "Enter the ID of the doctor you want to update: ").lower()

    found = False
    for doctor in data['doctor']:
        if doctor['id'] == doctor_id:
            found = True
            print("\nID\tName\t\t\tEmail\t\t\tVisit-Hour\tSpecialist\tQualification\n")
            print(f"{doctor['id'].upper()}\t{doctor['name'].upper()}\t\t{doctor['email']}\t{doctor['visit-hour']}\t{doctor['Specialist'].capitalize()}\t\t{doctor['qualification'].upper()}\n")
            print("Doctor found. Please update their information: \n")
            name = doctor['name']
            email = input("Enter Doctor Email: ")
            password = doctor['password']
            visit_hour = input("Enter Visit-Hour: ")
            specialist = input("Enter the Doctor Specialization: ").lower()
            qualification = input("Enter Doctor Qualification: ").lower()

            doctor.update({
                "name": name,
                "email": email,
                "password": password,
                "visit-hour": visit_hour,
                "Specialist": specialist,
                "qualification": qualification
            })

            userData_json_obj = json.dumps(data, indent=5)
            write(userPath, userData_json_obj)
            print("Doctor information updated successfully.")
            break

    if not found:
        print(f"Doctor with ID {doctor_id} not found.")


def delete_doctor(data):
    id = input("Enter Doctor ID: ").lower()
    flag = False
    for i in data['doctor']:
        if id == i['id']:
            index = data['doctor'].index(i)
            del data['doctor'][index]
            userData_json_obj = json.dumps(data, indent=5)
            write(userPath, userData_json_obj)
            flag = True
            break
    if flag:
        print("Doctor Info deleted Successfully!")
    else:
        print("Doctor not Registered!")
# --------------------- Patient Management ---------------------
# Patient Info Read


def read_patient(data):
    print("\nPatient Info\n")
    print("\nID\tName\t\t\tEmail\t\t\tAppointment\tPrescription")
    for i in data:
        print(
            f"{i['id'].upper()}\t{i['name'].upper()}\t\t{i['email']}\t{i['appointment']}\t{i['prescription']}\n")


def delete_patient(data):
    id = input("Enter Patient ID: ").lower()
    flag = False
    for patient in data:
        if id == patient['id']:
            index = data.index(patient)
            del data[index]
            patientData_json_obj = json.dumps(data, indent=5)
            write(patientPath, patientData_json_obj)
            flag = True
            break
    if flag:
        print("Patient info deleted successfully!")
    else:
        print("Patient not Registered")

# read_patient(patientData)
# ----------------Appointment Management--------------
# Read Appointment Info


def read_appointment_info(data):
    print("\nAppointment Info\n")
    print("\nID\tDoctor Name\t\tPatient Name\t\tTime\tDate\n")
    for i in data:
        print(f"{i['id'].upper()}\t{i['doctorName'].upper()}\t\t{i['patientName'].upper()}\t{i['time']}\t{i['date']}")

# Cancel Appointment


def cancel_appointment(apnData, ptData, id):
    patient = ""

    for i in apnData:
        if id.lower() == i['id']:
            index = apnData.index(i)
            del apnData[index]
            patient = i['patientName']
            break
    else:
        print("Appointment Not Found")

    for p in ptData:
        if p['name'] == patient:
            p['appointment'].remove(id.lower())
            break
    else:
        print("not match")
    apnData_json_obj = json.dumps(apnData, indent=5)
    ptData_json_obj = json.dumps(ptData, indent=5)
    write(appointmentPath, apnData_json_obj)
    write(patientPath, ptData_json_obj)
    print("Appointment cancel Successfully")

# -----------Doctor Part --------------------
# read appointment using by doctor name


def read_doctor_appointment(aData, doc_name):
    print("\nID\t\tPatient Name\t\tTime\tDate\n")
    for appointment in aData:
        if appointment['doctorName'] == doc_name:
            print(
                f"{appointment['id'].upper()}\t\t{appointment['patientName'].upper()}\t{appointment['time']}\t{appointment['date']}")


def read_doctor_patient(data, aData, doc_name):
    print("\nPatient Info\n")
    print("\nID\tName\t\t\tEmail\t\t\tAppointment\tPrescription")
    apnId = ""
    for appointment in aData:
        if appointment['doctorName'] == doc_name:
            apnId = appointment["id"]

    for i in data:
        if (apnId in i["appointment"]):
            print(
                f"{i['id'].upper()}\t{i['name'].upper()}\t\t{i['email']}\t{i['appointment']}\t{i['prescription']}\n")
        else:
            print("Today you have no patient!")
            break


# create prescription for patient


def add_prescription(pData, hData, dName, pName):
    prsFlag = False
    for patient in pData:
        if patient['name'] == pName:
            prsID = autoIdGenerator('prs-')
            d_Name = dName
            p_Name = pName
            problem = input("Enter Patient Problem: ").lower()
            medicine = input("Enter the name of medicine: ")
            test = input("Enter the name of test: ")

            mdcn = medicine.split(", ")
            tst = test.split(", ")

            prescription_obj = {
                "id": prsID,
                "doctorName": d_Name,
                "patientName": p_Name,
                "medicine": mdcn,
                "test": tst
            }

            patient['prescription'].append(prsID)
            hData.append(prescription_obj)

            pData_json_obj = json.dumps(pData, indent=5)
            hData_json_obj = json.dumps(hData, indent=5)

            write(patientPath, pData_json_obj)
            write(prescriptionPath, hData_json_obj)

            prsFlag = True
            break
    if not prsFlag:
        print("Patient name not in appointment!")

# add_prescription(patientData, historyData, 'rahat khan', 'shilpa')
# -----------Patient Part ------------------
# show doctor in table


def show_doctor():
    print("\nDoctor Info\n")
    print("ID\tName\t\tQualification\tVisit-Hour\n")
    for i in range(len(userData['doctor'])):
        id = userData['doctor'][i]['id']
        name = userData['doctor'][i]['name']
        qualification = userData['doctor'][i]['qualification']
        visit_hour = userData['doctor'][i]['visit-hour']
        print(f'{id.upper()}\t{name.upper()}\t{qualification.upper()}\t\t{visit_hour}')
    print("\n")

# Make appointment function


def make_appointment(pData, uData, aData):
    doctor_name = input("Doctor Name: ").lower()
    doctor_found = False
    patient_found = False
    for doctor in userData['doctor']:
        if doctor_name == doctor['name']:
            aId = autoIdGenerator('a-')
            pId = autoIdGenerator('p-')
            patient_name = input("Patient Name: ").lower()
            for patient in pData:
                if patient['name'] == patient_name:
                    patient['appointment'].append(aId)
                    patient_found = True
            if not patient_found:
                patient_email = input("Patient Email: ").lower()
                apnArr = []
                apnArr.append(aId)
                patient_object = {
                    "id": pId,
                    "name": patient_name,
                    "email": patient_email,
                    "appointment": apnArr,
                    "prescription": []
                }
                pData.append(patient_object)

            time = doctor['visit-hour']
            today = date.today()
            appointment = {
                "id": aId,
                "doctorName": doctor['name'],
                "patientName": patient_name,
                "time": time,
                "date": str(today)
            }
            aData.append(appointment)

            aData_json_obj = json.dumps(aData, indent=5)
            pData_json_obj = json.dumps(pData, indent=5)

            write(patientPath, pData_json_obj)
            write(appointmentPath, aData_json_obj)
            print("Appointment Create Successfully!")
            doctor_found = True
    if not doctor_found:
        print("Doctor not found!")

# read appointment history


def read_appointment(pData, aData):
    name = input("Please enter your name: ").lower()
    for i in range(len(pData)):
        if name == pData[i]['name']:
            print(pData[i]['appointment'])
            des = input("Do you want to cancel appointment (y/n): ").lower()
            if des == "y":
                apnId = input("Enter your appointment ID: ")
                pData[i]['appointment'].remove(apnId)
                for apn in range(len(aData)):
                    if apnId == aData[apn]["id"]:
                        del aData[apn]
                        break
                    else:
                        pass
            else:
                pass
            patientData_json_obj = json.dumps(pData, indent=5)
            appointmentData_json_obj = json.dumps(aData, indent=5)
            write(patientPath, patientData_json_obj)
            write(appointmentPath, appointmentData_json_obj)
            print("Appointment successfully deleted")
            break

# See Patient History


def see_history(patientData, historyData):
    name = input("Patient Name: ").lower()
    hflag = False
    for patient in patientData:
        if patient['name'] == name:
            hflag = True
            if len(patient['prescription']) == 0:
                print(f"{patient['name'].upper()} has no medical records.")
                break
            else:
                print(patient['prescription'])
                prisId = input("Enter your prescription ID: ").lower()
                print("\n")
                for sp in historyData:
                    if sp['id'] == prisId:
                        for key, value in sp.items():
                            print(f"\t{key}: \t{value}")
                print("\n")
                break
    if not hflag:
        print("You entered wrong name.")
# ---------------Admin Menu--------------


def admin_menu():
    while True:
        try:
            print(
                "\n1. Doctor Management\n2. Appointment Management\n3. Patient Management\n4. Back Main Menu\n")
            choice = int(input("Enter you choice from (Admin Menu): "))

            if choice == 1:
                read_doctor(userData)
                while True:
                    print(
                        "\n1. ADD Doctor\n2. Doctor List\n3. Update Doctor\n4. Delete Doctor\n5. Back Previous Menu\n")
                    choice = int(
                        input("Enter your choice for (Doctor Management): "))
                    if choice == 1:
                        add_doctor(userData)
                        read_doctor(userData)
                    elif choice == 2:
                        read_doctor(userData)
                    elif choice == 3:
                        # update_doctor(userData)
                        upC = input(
                            "Do you want to update doctor info: (y/n): ").lower()
                        if upC == 'y':
                            update_doctor(userData)
                        else:
                            pass
                    elif choice == 4:
                        delete_doctor(userData)
                    elif choice == 5:
                        break
                    else:
                        print("Option not in the list")
                        break
            elif choice == 2:
                read_appointment_info(appointmentData)
                cancelApn = input(
                    "Do you want to cancel Appointment: (y/n) ").lower()
                if cancelApn == "y":
                    apnt_id = input("Enter Appointment ID: ")
                    cancel_appointment(appointmentData, patientData, apnt_id)
                else:
                    pass
            elif choice == 3:
                while True:
                    try:
                        print("\n1.Show Patient Info\n2. Delete Patient\n3. Back Previous Menu")
                        pch = int(input("Enter your choice: (Patient Management): "))
                        if (pch == 1):
                            read_patient(patientData)
                        elif (pch == 2):
                            dpc = input(
                                "Do you want to delete any patient info: (y/n)").lower()
                            if dpc == 'y':
                                delete_patient(patientData)
                            else:
                                break
                        elif (pch == 3):
                            break
                        else:
                            print("Option not in the list!")
                    except:
                        print("You entered invalid option!")
            elif choice == 4:
                break
            else:
                print("Invalid option")
                break
        except:
            print("You entered invalid option!")

# -----------------------------Doctor Menu--------------


def doctor_menu(dct):
    while True:
        try:
            print("\n1. Appointment Info\n2. Patient Info\n3. Patient Medical Record\n4. Make Prescription \n5. Back Main Menu")
            choice = int(input("Enter your choice (For Doctor) : "))
            if choice == 1:
                print("Appointment Information")
                read_doctor_appointment(appointmentData, dct['name'])
            elif choice == 2:
                # read_patient(patientData)
                read_doctor_patient(patientData, appointmentData, dct['name'])
            elif choice == 3:
                see_history(patientData, historyData)
            elif choice == 4:
                print("Make prescription\n")
                patient_name = input("Patient Name: ").lower()
                add_prescription(patientData, historyData,
                                 dct['name'], patient_name)
                p_apnt_id = ""
                for singleapt in appointmentData:
                    if singleapt['doctorName'] == dct['name']:
                        p_apnt_id = singleapt['id']

                cancel_appointment(appointmentData, patientData, p_apnt_id)
                print("Prescription Make successfully!")
            elif choice == 5:
                break
            else:
                print("Option NOt found!")
        except:
            print("You entered Invalid option!")

# -------------------Authentication function------------------------


def authenticate_admin(email, password, users):
    for admin in users.get("admin", []):
        if admin["email"] == email and admin["password"] == password:
            admin = admin_menu()
            return admin
    return None


def authenticate_doctor(email, password, users):
    for doctor in users.get("doctor", []):
        if doctor["email"] == email and doctor["password"] == password:
            doctor = doctor_menu(doctor)
            return doctor
    return None


def login(email, password, role):

    authenticated_user = None
    if role == "admin":
        authenticated_user = authenticate_admin(email, password, userData)
    elif role == "doctor":
        authenticated_user = authenticate_doctor(email, password, userData)

    if authenticated_user:
        print("Login successful")
        print("User details:", authenticated_user)
    else:
        print("Login failed. Check your credentials.")


# ---------------------------- show option list ------------------

print("Hospital Management System")
while True:
    try:
        print("\n1. Login for (Admin & Doctor)\n2. Make Appointment for patient\n3. Exit from the System")
        a = int(input("\nEnter your choice: "))
        if a == 1:
            for i in range(3):
                email = input("Enter you email: ")
                password = input("Enter your password: ")
                role = input("Enter your role: ").lower()
                login(email, password, role)
                break
        elif a == 2:
            while True:
                print(
                    "\n1. Make Appointment\n2. See Appointment\n3. Previous Medical Record\n4. Back Main Menu\n")
                pChoice = int(input("\nEnter your choice (For Patient): "))
                if pChoice == 1:
                    show_doctor()
                    make_appointment(patientData, userData, appointmentData)
                elif pChoice == 2:
                    read_appointment(patientData, appointmentData)

                elif pChoice == 3:
                    see_history(patientData, historyData)
                elif pChoice == 4:
                    break
                else:
                    print("Please enter correct number.")
        elif a == 3:
            print("Exit From the system....")
            break
        else:
            print("Please enter correct number: ")
    except:
        print("You entered invalid option!")
