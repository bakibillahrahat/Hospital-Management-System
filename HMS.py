from datetime import date
import json

userPath = "./Data/user.json"
appoinmentPath = "./Data/appoinment.json"
patientPath = "./Data//patient.json"

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
        print(f'{id}\t{name}\t{qualification}\t\t{visit_hour}')

# Make appoinment function 
def make_appointment():
    doctor = input("Please enter your Doctor name: ")
    found = False
    for i in range(len(userData['doctor'])):
        if userData['doctor'][i]['name'] == doctor:
            aId = autoIdGenerator(appoinmentData, 'a-')
            pId = autoIdGenerator(read(patientPath), 'p-')
            patient = input("Enter you name: ")
            email = input("Enter you email: ")
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
            # appoinmentData.append(appoinment)
            # json_object = json.dumps(appoinmentData, indent=5)
            # write(appoinmentPath, json_object)
            pData = read(patientPath)
            for i in range(len(pData)):
                if pData[i]['name'] == patient:
                    pData[i]['appoinment'].append(aId)
                else:                    
                    apnArr = []
                    apnArr.append(appoinment['id'])
                    
                    patient = {
                        "id": pId,
                        "name": patient,
                        "email": email,
                        "appoinment": apnArr,
                        "prescription": []
                    }
            print("Appoinment Create Successfully!")
            print(patient)
            found = True
            break
    if not found:
        print("Doctor not found!")
  
make_appointment()

# See Patient History
    
# print("Hospital Management System")
# print("\n1. Admin Login \n2. Doctor Login\n3. Make Appoinment for patient\n4. Exit from the System")

# for i in range(3):
#   a = int(input("Enter your choice: "))
#   if a == 1:
#     for i in range(2):
#       print(f'you can make {i} attempt')
#       email = input("Enter you email: ")
#       password = input("Enter your password: ")
#       login(email, password)
#       break
#   elif a == 2:
#       print("Doctor login")
#   elif a == 3:
#     print("Appoinment function")
#   elif a == 4:
#     print("Exit From the system....")
#     break
#   else:
#     print("Please enter correct number: ")