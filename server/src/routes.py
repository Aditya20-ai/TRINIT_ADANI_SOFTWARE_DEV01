from .app import app, jsonify, request
from .utils import MysqlConnection, UploadHandler, list_parser
from secrets import randbits
connection = MysqlConnection()
uploader = UploadHandler()

@app.route('/create-profile', methods=['POST'])
def create_profile():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method'})

    if not (data := request.form):
        return jsonify({'message': 'Invalid data'})
    user_id = data['user_id']
    name = data['name']
    email = data['email']
    donation_preferences = data['donation_preferences']
    try:            
        if connection :
            query = "INSERT INTO user_data (ID, name, email, donation_preferences) VALUES (%s, %s, %s, %s)"
            values = (user_id, name, email, donation_preferences)
            connection.insert_records(query, values)
            return jsonify({'message': 'Profile created successfully', 'QUERY': 'OK'})
        else:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data' : {'error':  str(e)}})

@app.route('/get-profile')
def get_profile():
    if request.method != 'GET':
        return jsonify({'message': 'Invalid request method'})
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'QUERY': 'FAILED', 'data': 'Invalid user_id'})
    try:
        if connection :
            query = f"SELECT * FROM user_data WHERE ID = '{user_id}'"
            result = connection.select_records(query)
            if result:
                result = list(result)
                result[-1] = list_parser(result[-1])
                return jsonify({'QUERY': 'OK', 'data': result})
            else:
                return jsonify({'QUERY': 'FAILED', 'data': 'No data found'})
        return jsonify({'QUERY': 'FAILED', 'data': 'Failed to connect to database'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data' : {'error':  str(e)}})

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method'})

    if not (data := request.form):
        return jsonify({'message': 'Invalid data'})
    user_id = data['user_id']
    name = data['name']
    email = data['email']
    donation_preferences = data['donation_preferences']
    try:
        if connection :
            #query = f"UPDATE user_data SET name = '{name}', email = '{email}', donation_preferences = '{donation_preferences}' WHERE ID = '{user_id}'"
            query = "UPDATE user_data SET name = %s, email = %s, donation_preferences = %s WHERE ID = %s"
            values = (name, email, donation_preferences, user_id)
            connection.insert_records(query, values)
            return jsonify({'message': 'Profile updated successfully', 'QUERY': 'OK'})
        else:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data' : {'error':  str(e)}})

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method'})

    if not (data := request.files):
        return jsonify({'message': 'Invalid data'})
    image = data['image']
    try:
        if connection :
            image_filename = f"{randbits(64)}.png"
            image_path = f"server/temp/images/{image_filename}"
            image.save(image_path)
            image_link = uploader.upload_image(image_path)
            return jsonify({'message': 'Image uploaded successfully', 'QUERY': 'OK', 'data': image_link})
        else:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data' : {'error':  str(e)}})

@app.route('/shutdown')
def shutdown():
    connection.close_connection()
    return jsonify({'message': 'Server shutdown'})
