import json 
import requests
from flask_babel import _
from app import app

def translate(text, source_language, dest_language):
    '''
    Take text to translate along with source language and destination language as arguments.
    Returns a string with the translated text.
    '''

    if 'MS_TRANSLATOR_KEY' not in app.config or \
            not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}
    # get is used to send a HTTP request to the URL with provided arguments
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    # if any other status code than 200 then an error has occured 
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))