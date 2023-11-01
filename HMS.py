import json
from datetime import date

userPath = "./Data/user.json"
appointmentPath = "./Data/appointment.json"
patientPath = "./Data//patient.json"
prescriptionPath = "./Data/prescription.json"

with open(userPath, 'r') as user:
    userData = json.load(user)
with open(appointmentPath, 'r') as appointment:
    appointmentData = json.load(appointment)
    
def read(path):
    with open(path, 'r') as file:
        data =  json.loads(file.read())
        return data

def write(path, obj):
    with open(path, 'w') as allData:
        allData.write(obj)

# def login(email, password):
#     userData = read(userPath)
#     for key,value in userData.items():
#         for i in value:
#             if email == i['email'] and password == i['password'] and key:
#                 if role == 'admin':
#                     admin_menu()
#                 elif role == 'doctor':
#                     doctor_menu()
#                 else:
#                     print("Wrong input!")
#                 break
#             else:
#                 print("Invalid Credential!")
                # break


def autoIdGenerator(data, basePattern):
    lastId = data[-1]['id']
    count = int(lastId[-1])
    id = ''
    count += 1
    if count < 10:
        id = basePattern + '0' + str(count)
    elif count > 9:
        id = basePattern + str(count)
    return id
# -----------Admin Part ------------------
def admin_menu():
    print("\n1. Doctor Management\n2. Appointment Management 3. Patient Info")
def doctor_menu():
    print("\n1. Appointment Info\n2. Patient Info\n3. Patient Medical Record")
    
def add_doctor(data):
    name = input("Enter Doctor Name : ")
    email = input("Enter Doctor Email: ")
    password = input("Enter Doctor temporary password: ")
    visit_hour = input("Enter Visit-Hour: ")
    specialist = input("Enter the Doctor Specialization: ")
    qualification = input("Enter Doctor Qualification: ")
        
    doctor_obj = {
        "id": autoIdGenerator(data['doctor'],'d-'),
        "name": name,
        "email": email,
        "password": password,
        "visit-hour": visit_hour,
        "Specialist": specialist,
        "qualification": qualification
    }
    data['doctor'].append(doctor_obj)
    userData_json_obj = json.dumps(data)
    write(userPath, userData_json_obj)
# add_doctor(userData)

def read_doctor(data):
    print("\nDoctor Info")
    print("\nID\tName\t\t\tEmail\t\t\tVisit-Hour\tSpecialist\tQualification")
    for i in data['doctor']:
        print(f"{i['id'].upper()}\t{i['name'].upper()}\t\t{i['email']}\t{i['visit-hour']}\t{i['Specialist']}\t\t{i['qualification']}")
    print("\n")
    
read_doctor(userData)
    
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
        print(f'{id.upper()}\t{name.upper()}\t{qualification}\t\t{visit_hour}')
    print("\n")

# Make appointment function 
def make_appointment():
    pData = read(patientPath)
    doctor = input("Please enter your Doctor name: ").lower()
    found = False
    for i in range(len(userData['doctor'])):
        if userData['doctor'][i]['name'] == doctor:
            aId = autoIdGenerator(appointmentData, 'a-')
            pId = autoIdGenerator(pData, 'p-')
            patient = input("Enter you name: ").lower()
       
            for i in range(len(pData)):
                if pData[i]['name'] == patient.lower(): 
                    pData[i]['appointment'].append(aId)
                    break
                else:
                    email = input("Enter you email: ")
                    apnArr = []
                    apnArr.append(aId)
                    patientObj = {
                        "id": pId,
                        "name": patient,
                        "email": email,
                        "appointment": apnArr,
                        "prescription": []
                    } 
                    pData.append(patientObj)
                    break
            doctor = userData['doctor'][i]['name']
            time = userData['doctor'][i]['visit-hour']
            today = date.today()       
            appointment = {
                "id": aId,
                "doctorName": doctor,
                "patientName": patient,
                "time": time,
                "date": str(today)
            }

            appointmentData.append(appointment)
                    
            pData_json_obj = json.dumps(pData, indent=5)
            write(patientPath, pData_json_obj)
            
            apnData_json_object = json.dumps(appointmentData, indent=5)
            write(appointmentPath, apnData_json_object)
            print("Appointment Create Successfully!")
            
            found = True
            break
    if not found:
        print("Doctor not found!")
  
# make_appointment()

# read appointment history
def read_appointment():
    patientData = read(patientPath)
    name = input("Please enter your name: ").lower()
    for i in range(len(patientData)):
        if name == patientData[i]['name']:
            print(patientData[i]['appointment'])
            des = input("Do you want to cancel appointment: ")
            if des == "yes":
                apnId = input("Enter your appointment ID: ")
                patientData[i]['appointment'].remove(apnId)
                for apn in range(len(appointmentData)):
                    if apnId == appointmentData[apn]["id"]:
                        del appointmentData[apn]
                        break
                    else:
                        pass
            else:
                pass    
            patientData_json_obj = json.dumps(patientData, indent=5)
            appointmentData_json_obj = json.dumps(appointmentData, indent=5)
            write(patientPath, patientData_json_obj)
            write(appointmentPath, appointmentData_json_obj)
            print("Appointment successfully deleted")
            break


# See Patient History
def see_history():
    patientData = read(patientPath)
    historyData = read(prescriptionPath)
    name = input("Please enter your name: ").lower()
    for i in range(len(patientData)):
        if name == patientData[i]['name']:
            print(patientData[i]['prescription'])
            prisId = input("Enter your prescription ID: ")
            for sp in range(len(historyData)):
                if historyData[sp]['prescriptionId'] == prisId:
                    for key, value in historyData[sp].items():
                        print(f"\t{key}:\t{value}")
                    break
            break
        else:
            print("You entered wrong name!")
            break

# see_history()
print("Hospital Management System")
print("\n1. Login for (Admin & Doctor)\n2. Make Appointment for patient\n3. Exit from the System")

for i in range(3):
  a = int(input("\nEnter your choice: "))
  if a == 1:
    for i in range(2):
      print(f'you can make {i} attempt')
      email = input("Enter you email: ")
      password = input("Enter your password: ")
      role = input("Enter your role: ")
      login(email, password, role)
      break
  elif a == 2:
      for i in range(3):
        print("\n1. Make Appointment\n2. See Appointment\n3. Previous Medical Record")
        pChoice = int(input("\nEnter your choice (For Patient): "))
        if pChoice == 1:
            show_doctor()
            make_appointment()
            break
        elif pChoice == 2:
            read_appointment()
            break
        elif pChoice == 3:
            see_history()
            break
        else:
            print("Please enter correct number.")
  elif a == 3:
    print("Exit From the system....")
    break
  else:
    print("Please enter correct number: ")