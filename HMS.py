import json
from datetime import date

userPath = "./Data/user.json"
appoinmentPath = "./Data/appoinment.json"
patientPath = "./Data//patient.json"
prescriptionPath = "./Data/prescription.json"

with open(userPath, 'r') as user:
    userData = json.load(user)
with open(appoinmentPath, 'r') as appoinment:
    appoinmentData = json.load(appoinment)
    
def read(path):
    with open(path, 'r') as file:
        data =  json.loads(file.read())
        return data

def write(path, obj):
    with open(path, 'w') as allData:
        allData.write(obj)

def login(email, password):
  if email == 'bakibillahrahat@gmail.com' and password == '12345':
    print(f'Welcome MD. Bakibillah Rahat')
    print('\n1. Doctor Info\n2. Patient Info\n3. Appoinment Status')
  else:
    print('Invalid credential!')

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

# -----------Patient Part ------------------
# show doctor in table
def show_doctor():
    print("ID\tName\t\tQualification\tVisit-Hour\n")
    for i in range(len(userData['doctor'])):
        id = userData['doctor'][i]['id']
        name = userData['doctor'][i]['name']
        qualification = userData['doctor'][i]['qualification']
        visit_hour = userData['doctor'][i]['visit-hour']
        print(f'{id}\t{name.upper()}\t{qualification}\t\t{visit_hour}')

# Make appoinment function 
def make_appointment():
    pData = read(patientPath)
    doctor = input("Please enter your Doctor name: ").lower()
    found = False
    for i in range(len(userData['doctor'])):
        if userData['doctor'][i]['name'] == doctor:
            aId = autoIdGenerator(appoinmentData, 'a-')
            pId = autoIdGenerator(pData, 'p-')
            patient = input("Enter you name: ").lower()
       
            for i in range(len(pData)):
                if pData[i]['name'] == patient.lower(): 
                    pData[i]['appoinment'].append(aId)
                    break
                else:
                    email = input("Enter you email: ")
                    apnArr = []
                    apnArr.append(aId)
                    patientObj = {
                        "id": pId,
                        "name": patient,
                        "email": email,
                        "appoinment": apnArr,
                        "prescription": []
                    } 
                    pData.append(patientObj)
                    break
            doctor = userData['doctor'][i]['name']
            time = userData['doctor'][i]['visit-hour']
            today = date.today()       
            appoinment = {
                "id": aId,
                "doctorName": doctor,
                "patientName": patient,
                "time": time,
                "date": str(today)
            }

            appoinmentData.append(appoinment)
                    
            pData_json_obj = json.dumps(pData, indent=5)
            write(patientPath, pData_json_obj)
            
            apnData_json_object = json.dumps(appoinmentData, indent=5)
            write(appoinmentPath, apnData_json_object)
            print("Appoinment Create Successfully!")
            
            found = True
            break
    if not found:
        print("Doctor not found!")
  
# make_appointment()

# read appoinment history
def read_appoinment():
    patientData = read(patientPath)
    name = input("Please enter your name: ").lower()
    for i in range(len(patientData)):
        if name == patientData[i]['name']:
            print(patientData[i]['appoinment'])
            des = input("Do you want to cancel appoinment: ")
            if des == "yes":
                apnId = input("Enter your appoinment ID: ")
                patientData[i]['appoinment'].remove(apnId)
                for apn in range(len(appoinmentData)):
                    if apnId == appoinmentData[apn]["id"]:
                        del appoinmentData[apn]
                        break
                    else:
                        pass
            else:
                pass    
            patientData_json_obj = json.dumps(patientData, indent=5)
            appoinmentData_json_obj = json.dumps(appoinmentData, indent=5)
            write(patientPath, patientData_json_obj)
            write(appoinmentPath, appoinmentData_json_obj)
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
print("\n1. Admin Login \n2. Doctor Login\n3. Make Appoinment for patient\n4. Exit from the System")

for i in range(3):
  a = int(input("\nEnter your choice: "))
  if a == 1:
    for i in range(2):
      print(f'you can make {i} attempt')
      email = input("Enter you email: ")
      password = input("Enter your password: ")
      login(email, password)
      break
  elif a == 2:
      print("Doctor login")
  elif a == 3:
      for i in range(3):
        print("\n1. Make Appoinment\n2. See Appoinment\n3. Previous Medical Record")
        pChoice = int(input("\nEnter your choice (For Patient): "))
        if pChoice == 1:
            make_appointment()
            break
        elif pChoice == 2:
            read_appoinment()
            break
        elif pChoice == 3:
            see_history()
            break
        else:
            print("Please enter correct number.")
  elif a == 4:
    print("Exit From the system....")
    break
  else:
    print("Please enter correct number: ")