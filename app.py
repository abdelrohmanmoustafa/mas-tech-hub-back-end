from flask import Flask, flash, request, redirect, url_for, jsonify, send_file, make_response,session
from flask_cors import CORS
import mysql.connector
import uuid

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
host_name = "localhost"
user_name_database = "backend-mas-tech-hub"
pass_database = "backend-mas-tech-hub"
database_name = "backend-mas-tech-hub"

@app.route('/', methods=['GET'])
def start_page():
  return "Hello World!"

@app.route('/signup_account', methods=['POST'])
def signup_account():
  email = request.form.get('email') if request.form.get('email') else request.get_json()['email']
  password = request.form.get('password') if request.form.get('password') else request.get_json()['password']
  name = request.form.get('name') if request.form.get('name') else request.get_json()['name']
  account_type = request.form.get('account_type') if request.form.get('account_type') else request.get_json()['account_type']
  account_id = uuid.uuid4().hex
  
  mydb = mysql.connector.connect(
    host=host_name,
    user=user_name_database,
    password=pass_database,
    database=database_name
    )
  mycursor = mydb.cursor()
  
  while True: 
    try:
        mycursor.execute(f"""INSERT INTO `Users` (`ID`, `Name`, `Email`, `Password`, `Role`, `AccountStatus`) VALUES 
                            ('{account_id}', '{name}', '{email}', '{password}', '{account_type}', 'pending');
                            """)
        mydb.commit()
        mydb.close()
        return "true", 200
      
    except Exception as e:
        mydb.commit()
        mydb.close()
        error = str(e)
        
        if 'Users.Email' in error:
            error = 'Email already exists'
          
        elif 'users.PRIMARY' in error:
            account_id = uuid.uuid4().hex
            continue
        
        return error, 400
        
@app.route('/account_signin', methods=['POST'])
def account_signin():
  email = request.form.get('email') if request.form.get('email') else request.get_json()['email']
  password = request.form.get('password') if request.form.get('password') else request.get_json()['password']
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor(dictionary=True)
    
    mycursor.execute(f"""Select * from Users WHERE Email='{email}' and Password='{password}'
                              """)
    
    result = mycursor.fetchone()
    
    if result:
      if result['AccountStatus'] == 'active':
        return jsonify(result), 200
      else:
        return "Account is not active, Kindly contact admin", 400
    
    else: 
      return "Wrong Credentials", 400
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/get_accounts_info', methods=['GET'])
def get_accounts_info():
  account_type = request.args.get('account_type')
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor(dictionary=True)
    if account_type == 'master':
      mycursor.execute(f"""Select * from Users WHERE Role != 'master'
                              """)
    else:
      mycursor.execute(f"""Select * from Users WHERE Role = 'volunteer'
                              """)
    
    result = mycursor.fetchall()
    
    return result, 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/update_user_status', methods=['PUT'])
def update_user_status():
  account_id = request.form.get('id') if request.form.get('id') else request.get_json()['id']
  status = request.form.get('status') if request.form.get('status') else request.get_json()['status']
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor()
    mycursor.execute(f"""UPDATE Users SET AccountStatus = '{status}' WHERE ID='{account_id}'
                              """)
    mydb.commit()
    mydb.close()
    
    return "true", 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
  account_id = request.args.get('id')
  account_status = request.args.get('status')
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor()
    mycursor.execute(f"""DELETE FROM Users WHERE ID = '{account_id}'
                              """)

    mydb.commit()
    mydb.close()
    return "true", 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/delete_users', methods=['DELETE'])
def delete_users():
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor()
    mycursor.execute(f"""DELETE FROM Users WHERE AccountStatus='deleted' AND Role='volunteer'
                              """)

    mydb.commit()
    mydb.close()
    return "true", 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/get_truck_drivers', methods=['GET'])
def get_truck_drivers():
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"""Select * from Drivers
                              """)
    
    result = mycursor.fetchall()
    
    return result, 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/add_driver', methods=['POST'])
def add_driver():
  driver_name = request.form.get('driverName') if request.form.get('driverName') else request.get_json()['driverName']
  account_creator_id = request.form.get('accountID') if request.form.get('accountID') else request.get_json()['accountID']
  account_id = uuid.uuid4().hex
  status = "active"
  
  mydb = mysql.connector.connect(
    host=host_name,
    user=user_name_database,
    password=pass_database,
    database=database_name
    )
  mycursor = mydb.cursor()
  
  while True: 
    try:
        mycursor.execute(f"""INSERT INTO `Drivers` (`DriverID`, `DriverName`, `UserIdCreated`, `DriverStatus`) VALUES 
                            ('{account_id}', '{driver_name}', '{account_creator_id}', '{status}');
                            """)
        mydb.commit()
        mydb.close()
        return jsonify({"DriverName": driver_name, "DriverStatus": status, "DriverID": account_id}), 200
      
    except Exception as e:
        mydb.commit()
        mydb.close()
        error = str(e)
        if 'Drivers.PRIMARY' in error:
            account_id = uuid.uuid4().hex
            continue
        
        return error, 400

@app.route('/delete_driver', methods=['DELETE'])
def delete_driver():
  driver_id = request.args.get('id')
  account_status = request.args.get('status')
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor()
    if account_status == "deleted":
      mycursor.execute(f"""DELETE FROM Drivers WHERE DriverID='{driver_id}'
                              """)
    else:
      mycursor.execute(f"""UPDATE Drivers SET DriverStatus = 'deleted' WHERE DriverID='{driver_id}'
                              """)

    mydb.commit()
    mydb.close()
    return "true", 200
  
  except Exception as e:
    print(e)
    return str(e), 400

@app.route('/add_truck_operation', methods=['POST'])
def add_truck_operation():
  truck_location = request.form.get('truckLocation') if request.form.get('truckLocation') else request.get_json()['truckLocation']
  booth_location = request.form.get('boothLocation') if request.form.get('boothLocation') else request.get_json()['boothLocation']
  operation_request = request.form.get('request') if request.form.get('request') else request.get_json()['request']
  notes = request.form.get('notes') if request.form.get('notes') else request.get_json()['notes']
  priority = request.form.get('priority') if request.form.get('priority') else request.get_json()['priority']
  driver_id = request.form.get('assignedDriver') if request.form.get('assignedDriver') else request.get_json()['assignedDriver']
  operation_id = uuid.uuid4().hex
  status = "active"
  
  mydb = mysql.connector.connect(
    host=host_name,
    user=user_name_database,
    password=pass_database,
    database=database_name
    )
  mycursor = mydb.cursor()
  
  while True: 
    try:
        mycursor.execute(f"""INSERT INTO `TruckOperations` (`ID`, `TruckLocation`, `BoothLocation`, `Request`, `Notes`, `Priority`, `AssignedDriver`, `OperationStatus`) VALUES 
                            ('{operation_id}', '{truck_location}', '{booth_location}', '{operation_request}', '{notes}', '{priority}', '{driver_id}', '{status}');
                            """)
        mydb.commit()
        mydb.close()
        return "true", 200
      
    except Exception as e:
        mydb.commit()
        mydb.close()
        error = str(e)
        if 'TruckOperations.PRIMARY' in error:
            operation_id = uuid.uuid4().hex
            continue
        
        return error, 400  
      
@app.route('/get_truck_operation', methods=['GET'])
def get_truck_operation():
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"""
    SELECT * From TruckOperations, Drivers WHERE TruckOperations.AssignedDriver=Drivers.DriverID AND TruckOperations.OperationStatus!='resolved';
                              """)
    truck_operations_result = mycursor.fetchall()

    mycursor.execute(f"""
    Select * from Drivers
                              """)
    driver_result = mycursor.fetchall()

    result = {"drivers": driver_result, "truck_operations": truck_operations_result}

    return jsonify(result), 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/delete_truck_operation', methods=['DELETE'])
def delete_truck_operation():
  operation_id = request.args.get('id')
  operation_status = request.args.get('status')
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor()
    if operation_status == "deleted":
      mycursor.execute(f"""DELETE FROM TruckOperations WHERE ID='{operation_id}'
                              """)
    else:
      mycursor.execute(f"""UPDATE TruckOperations SET OperationStatus = 'deleted' WHERE ID='{operation_id}'
                              """)

    mydb.commit()
    mydb.close()
    return "true", 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/update_truck_operation', methods=['PUT'])
def update_truck_operation():
  operation_id = request.form.get('id') if request.form.get('id') else request.get_json()['id']
  operation_status = request.form.get('status') if request.form.get('status') else request.get_json()['status']
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor()
    
    mycursor.execute(f"""UPDATE TruckOperations SET OperationStatus = '{operation_status}' WHERE ID='{operation_id}'
                              """)

    mydb.commit()
    mydb.close()
    return "true", 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  
@app.route('/get_resolved_truck_oeprations', methods=['GET'])
def get_resolved_truck_oeprations():
  try:
    mydb = mysql.connector.connect(
      host=host_name,
      user=user_name_database,
      password=pass_database,
      database=database_name
      )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(f"""
    SELECT * From TruckOperations, Drivers WHERE TruckOperations.AssignedDriver=Drivers.DriverID and TruckOperations.OperationStatus='resolved';
                              """)
    
    result = mycursor.fetchall()
    result = {"truck_operations": result}

    return jsonify(result), 200
  
  except Exception as e:
    print(e)
    return str(e), 400
  

# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host='0.0.0.0', port=8090)