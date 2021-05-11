# Import Flask, jsonify and request module
from flask import Flask, jsonify, request
# Import MethodView from flask.views
from flask.views import MethodView

app = Flask(__name__)

# Populate an initial list of languages
languages = [
                'JavaScript', 'Python', 'Ruby'
            ]

# Function to look up and return the language name from languages list.
def get_language(name):
    # This is kind of a clusterfuck, but the equivalent way of this code is:
    # for language in languages:
    #     if language['name'].lower() == name.lower():
    #         return language
    # return None
    #
    #return [language for language in languages if language['name'].lower() == name.lower()][0]
    elementnumber = get_index(name)
    if elementnumber is not None:
        return {'name': languages[elementnumber]}
    return None

# Find the index number given the name to be searched.
# This search is not case-sensitive.
def get_index(name):
    # This is inefficicent in general, but may be the best way to use it for the time being.
    lowercaselist = [language.lower() for language in languages]
    count = lowercaselist.count(name.lower())
    if count > 0:
        return lowercaselist.index(name.lower)
    else:
        return None

# Language class that handles request for /language route
class Language(MethodView):
    
    # GET method
    def get(self, language_name):
        if language_name:
            if get_language(language_name) is not None:
                return jsonify({'language': get_language(language_name)})
            else:
                return jsonify({'error': f'Language {language_name} is not found'}), 404
        else:
            templist = []
            for language in languages:
                templist.append({'name': language})
            return jsonify({'languages': templist})

    # POST method
    def post(self):
        if request.is_json:
            new_language_name = request.json['name']
            languages.append(new_language_name)
            return jsonify({'language': get_language(new_language_name)}), 201
        else:
            return jsonify({'error': 'Request must be a JSON format'}), 400

    # PUT method
    def put(self,language_name):
        indexnumber = get_index(language_name)
        if indexnumber is None:
            return jsonify({'error': f'Language {language_name} is not found'}), 404
        if request.is_json:
            new_language_name = request.json['name']
            languages[indexnumber] = new_language_name
            return jsonify({'language': get_language(new_language_name)})
        else:
            return jsonify({'error': 'Request must be a JSON format'}), 400

    # DELETE method
    def delete(self, language_name):
        if get_language(language_name) is not None:
            language = get_language(language_name)
            languages.remove(language)
            return f'Language {language_name} is deleted.', 204
        return jsonify({'error': f'Language {language_name} is not found'}), 404

# Register Language view using Flask pluggable feature
language_view = Language.as_view('language_api')

# Define the URL rules for languages
app.add_url_rule('/language', methods=['POST'], view_func=language_view)
app.add_url_rule('/language', methods=['GET'], defaults={'language_name': None}, view_func=language_view)
app.add_url_rule('/language/<language_name>', methods=['GET', 'PUT', 'DELETE'], view_func=language_view)

# Start Flask app
app.run()
