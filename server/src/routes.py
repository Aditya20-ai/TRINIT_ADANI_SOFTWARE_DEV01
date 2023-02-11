import datetime
import os

from .app import app, jsonify, request
from .utils import MysqlConnection, UploadHandler, list_parser, ZoomMeeting
from secrets import randbits

connection = MysqlConnection()
uploader = UploadHandler()
meeting = ZoomMeeting()

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
    if not (data := request.form):
        return jsonify({'message': 'Invalid data'})
    user_id = data['user_id']
    ngo_id = data['ngo_id']
    name = data['name']
    mission = data['mission']
    history = data['history']
    impact = data['impact']
    plans = data['plans']
    funding_needs = data['funding_needs']
    location = data['location']
    _type = data['type']
    image = request.files['image']
    try:
        if not connection:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
        banner_url = uploader.upload_image(image)
        values = (user_id, ngo_id, name, mission, history, impact, plans, banner_url, funding_needs, location, _type)
        query = "INSERT INTO ngo_data (USER_ID, NGO_ID, name, created_at, mission, history, impact, plans, banner_url, funding_needs, location, type) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s)"
        connection.insert_records(query, values)
        return jsonify({'message': 'Crowdfunding created successfully', 'QUERY': 'OK'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})

@app.route('/api/get-crowdfundings')
def get_crowdfundings():
    if request.method != 'GET':
        return jsonify({'message': 'Invalid request method'})
    ngo_id = request.args.get('ngo_id')
    if not ngo_id:
        return jsonify({'QUERY': 'FAILED', 'data': 'Invalid ngo_id'})
    try:
        if not connection:
            return jsonify({'QUERY': 'FAILED', 'data': 'Failed to connect to database'})
        query = "SELECT * FROM ngo_data WHERE NGO_ID = %s"
        value = (ngo_id,)
        if result := connection.select_records(query, value):
            return jsonify({'QUERY': 'OK', 'data': list(result)})
        else:
            return jsonify({'QUERY': 'FAILED', 'data': 'No data found'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})
    
@app.route('/api/get-crowdfundings-by-user')
def get_crowdfundings_by_user():
    if request.method != 'GET':
        return jsonify({'message': 'Invalid request method'})
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'QUERY': 'FAILED', 'data': 'Invalid user_id'})
    try:
        if not connection:
            return jsonify({'QUERY': 'FAILED', 'data': 'Failed to connect to database'})
        query = "SELECT * FROM ngo_data WHERE USER_ID = %s"
        value = (user_id,)
        if result := connection.select_records(query, value):
            return jsonify({'QUERY': 'OK', 'data': list(result)})
        else:
            return jsonify({'QUERY': 'FAILED', 'data': 'No data found'})
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
        if not connection:
            return jsonify({'QUERY': 'FAILED', 'data': 'Failed to connect to database'})
        query = "SELECT * FROM user_data WHERE ID = %s"
        value = (user_id,)
        if result := connection.select_records(query, value):
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

@app.route('/api/update-crowdfunding', methods=['POST'])
def update_crowdfunding():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method'})

    if not (data := request.form):
        return jsonify({'message': 'Invalid data'})
    user_id = data['user_id']
    ngo_id = data['ngo_id']
    name = data['name']
    mission = data['mission']
    history = data['history']
    impact = data['impact']
    plans = data['plans']
    funding_needs = data['funding_needs']
    location = data['location']
    _type = data['type']
    image = request.files['image']
    try:
        if not connection:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
        banner_url = uploader.upload_image(image)
        values = (name, mission, history, impact, plans, banner_url, funding_needs, location, _type, user_id, ngo_id)
        query = "UPDATE ngo_data SET name = %s, mission = %s, history = %s, impact = %s, plans = %s, banner_url = %s, funding_needs = %s, location = %s, type = %s WHERE USER_ID = %s AND NGO_ID = %s"
        connection.insert_records(query, values)
        return jsonify({'message': 'Crowdfunding updated successfully', 'QUERY': 'OK'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})
    
@app.route('/api/delete-crowdfunding', methods=['POST'])
def delete_crowdfunding():
    if request.method != 'POST':
        return jsonify({'message': 'Invalid request method'})

    if not (data := request.form):
        return jsonify({'message': 'Invalid data'})
    user_id = data['user_id']
    ngo_id = data['ngo_id']
    try:
        if not connection:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
        values = (user_id, ngo_id)
        query = "DELETE FROM ngo_data WHERE USER_ID = %s AND NGO_ID = %s"
        connection.insert_records(query, values)
        return jsonify({'message': 'Crowdfunding deleted successfully', 'QUERY': 'OK'})
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
        if not connection:
            return jsonify({'message': 'Failed to connect to database', 'QUERY': 'FAILED'})
        image_filename = f"{randbits(64)}.png"
        if not os.path.exists('temp/images'):
            os.makedirs('temp/images')
        image_path = f"temp/images/{image_filename}"
        image.save(image_path)
        image_link = uploader.upload_image(image_path)
        os.remove(image_path)
        return jsonify({'message': 'Image uploaded successfully', 'QUERY': 'OK', 'data': image_link})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data': {'error': str(e)}})


@app.route("/api/create-meeting", methods=['GET'])
def create_meeting():
    result = meeting.create_meeting(topic="Test Meeting", duration=40, time=datetime.datetime.now())
    return jsonify(result)


@app.route('/api/shutdown')
def shutdown():
    connection.close_connection()
    return jsonify({'message': 'Server shutdown'})
