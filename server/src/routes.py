import os

from .app import app, jsonify, request
from .utils import MysqlConnection, UploadHandler, list_parser
from secrets import randbits

connection = MysqlConnection()
uploader = UploadHandler()


@app.route('/api/create-profile', methods=['POST'])
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
        if not connection:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
        values = (user_id, name, email, donation_preferences)
        query = "INSERT INTO user_data (ID, name, email, donation_preferences) VALUES (%s, %s, %s, %s)"
        connection.insert_records(query, values)
        return jsonify({'message': 'Profile created successfully', 'QUERY': 'OK'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})


@app.route('/api/create-crowdfunding', methods=['POST'])
def create_crowdfunding():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method'})
    """
    USER_ID varchar(32) NOT NULL,
    NGO_ID varchar(32) PRIMARY KEY,
    name varchar(32) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mission varchar(255) NOT NULL,
    history varchar(255),
    impact varchar(255),
    plans varchar(255),
    banner_url varchar(64),
    funding_needs varchar(255) NOT NULL,
    location varchar(255) NOT NULL,
    type JSON NOT NULL
    
    
    """
    if not (data := request.form):
        return jsonify({'message': 'Invalid data'})
    user_id = data['user_id']
    ngo_id = data['ngo_id']
    name = data['name']
    mission = data['mission']
    history = data['history']
    impact = data['impact']
    plans = data['plans']
    banner_url = data['banner_url']
    funding_needs = data['funding_needs']
    location = data['location']
    type = data['type']
    title = data['title']
    description = data['description']
    target_amount = data['target_amount']
    image = request.files['image']
    try:
        if not connection:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
        image_url = uploader.upload_image(image)
        values = (user_id, title, description, target_amount, image_url)
        query = "INSERT INTO crowdfunding (user_id, title, description, target_amount, image_url) VALUES (%s, %s, %s, %s, %s)"
        connection.insert_records(query, values)
        return jsonify({'message': 'Crowdfunding created successfully', 'QUERY': 'OK'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})



@app.route('/api/get-profile')
def get_profile():
    if request.method != 'GET':
        return jsonify({'message': 'Invalid request method'})
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'QUERY': 'FAILED', 'data': 'Invalid user_id'})
    try:
        if not connection :
            return jsonify({'QUERY': 'FAILED', 'data': 'Failed to connect to database'})
        query = "SELECT * FROM user_data WHERE ID = %s"
        value = (user_id,)
        result = connection.select_records(query, value)
        if result:
            result = list(result)
            result[-1] = eval(result[-1])
            return jsonify({'QUERY': 'OK', 'data': result})
        else:
            return jsonify({'QUERY': 'FAILED', 'data': 'No data found'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})


@app.route('/api/update-profile', methods=['POST'])
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
        if not connection:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
        values = (name, email, donation_preferences, user_id)
        query = "UPDATE user_data SET name = %s, email = %s, donation_preferences = %s WHERE ID = %s"
        connection.insert_records(query, values)
        return jsonify({'message': 'Profile updated successfully', 'QUERY': 'OK'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})


@app.route('/api/delete-profile', methods=['POST'])
def delete_profile():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method'})

    if not (data := request.form):
        return jsonify({'message': 'Invalid data'})
    user_id = data['user_id']
    try:
        if not connection:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
        values = (user_id,)
        query = "DELETE FROM user_data WHERE ID = %s"
        connection.insert_records(query, values)
        return jsonify({'message': 'Profile deleted successfully', 'QUERY': 'OK'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})


@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method'})

    if not (data := request.files):
        return jsonify({'message': 'Invalid data'})
    image = data['file']
    try:
        if connection:
            image_filename = f"{randbits(64)}.png"
            if not os.path.exists('temp/images'):
                os.makedirs('temp/images')
            image_path = f"temp/images/{image_filename}"
            image.save(image_path)
            image_link = uploader.upload_image(image_path)
            os.remove(image_path)
            return jsonify({'message': 'Image uploaded successfully', 'QUERY': 'OK', 'data': image_link})
        else:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})


@app.route('/api/shutdown')
def shutdown():
    connection.close_connection()
    return jsonify({'message': 'Server shutdown'})
