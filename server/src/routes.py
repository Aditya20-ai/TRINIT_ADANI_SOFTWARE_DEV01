from .app import app, jsonify, request
from .utils import MysqlConnection, list_parser

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
        if connection := MysqlConnection():
            query = "INSERT INTO user_data (ID, name, email, donation_preferences) VALUES (%s, %s, %s, %s)"
            values = (user_id, name, email, donation_preferences)
            connection.insert_records(query, values)
            connection.close_connection()
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
        if connection := MysqlConnection():
            query = f"SELECT * FROM user_data WHERE ID = '{user_id}'"
            result = connection.select_records(query, return_list=True)
            connection.close_connection()
            if result:
                result[-1] = list_parser(result[-1])
            return jsonify({'QUERY': 'OK', 'data': result})
        else:
            return jsonify({'QUERY': 'FAILED', 'data': 'Failed to connect to database'})
    except Exception as e:
        return jsonify({'QUERY': 'FAILED', 'data' : {'error':  str(e)}})

