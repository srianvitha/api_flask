from flask import Flask, jsonify, request

app = Flask(__name__)

def is_sanitized(payload):
    # List of characters that could be used for SQL injection
    sql_injection_chars = ["'", '"', ";", "--", "/*", "*/"]

    for char in sql_injection_chars:
        if char in payload:
            return False
    return True

@app.route('/v1/sanitized/input/', methods=['POST'])
def check_sanitization():
    data = request.get_json()
    payload = data.get('payload')

    if payload is None:
        return jsonify({'error': 'No payload provided'}), 400

    if is_sanitized(payload):
        return jsonify({'result': 'sanitized'})
    else:
        return jsonify({'result': 'unsanitized'})

if __name__ == '__main__':
    app.run()
