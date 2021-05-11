from flask import Flask, json, jsonify, request
app = Flask(__name__)

languages = [{'name': 'JavaScript'}, {'name': 'Python'}, {'name': 'Ruby'}]

def is_json():
    # Do we need this? Just putting it in there for good luck.
    mimetype_lower = request.mimetype.lower()
    print(f"{is_json.__name__}: Checking if request MIME is JSON...")
    if mimetype_lower.find('json'):
        print(f'{is_json.__name__}: Request is a JSON')
        return True
    print(f'{is_json.__name__}: Request is not JSON')
    return False

@app.route('/', methods=['GET'])
def main():
    if is_json():
        return jsonify({'message': 'Welcome to Python RESTful API!'})
    else:
        return 'Welcome to Python RESTful API!'

@app.route('/lang', methods=['GET'])
def returnAll():
    if is_json():
        return jsonify({'languages': languages})
    else:
        return languages.__str__()

@app.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
    langs = [language for language in languages if language['name'] == name]
    if is_json():
        return jsonify({'language': langs[0]})
    else:
        return f'Name: {langs[0]}'

@app.route('/lang', methods=['POST'])
def addOne():
    if request.is_json:
        if 'name' not in request.json:
            if is_json():
                return jsonify({'error': 'Required key "name" is not found in request.'}),400
            else:
                return f'Required key "name" is not found in request.', 400
        language = {'name': request.json['name']}
        languages.append(language)
        return jsonify({'languages': languages}), 201
    if is_json():
        return jsonify({'error': 'Request payload data is not in JSON format.'}), 400
    else:
        return f'Error: Request payload data is not in JSON format.', 400

@app.route('/lang/<string:name>', methods=['PUT'])
def editOne(name):
    langs = [language for language in languages if language['name'] == name]
    langs[0]['name'] = request.json['name']
    if is_json():
        return jsonify({'language': langs[0]})
    else:
        return f'Languages: {languages}'

@app.route('/lang/<string:name>')
def removeOne(name):
    lang = [language for language in languages if language['name'] == name]
    languages.remove(lang[0])
    if is_json():
        return jsonify({'languages': languages})
    else:
        return f'Languages: {languages}'

if __name__ == '__main__':
    app.run()
