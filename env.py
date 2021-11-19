import os
from dotenv import load_dotenv
import json

def init():
    load_dotenv()

    global go_daddy_api
    go_daddy_api = os.getenv('GO_DADDY_API')

    global go_daddy_key
    go_daddy_key = os.getenv('GO_DADDY_KEY')

    global go_daddy_secret
    go_daddy_secret = os.getenv('GO_DADDY_SECRET')

    global name_server
    name_server = json.loads(os.getenv('NAME_SERVER'))

    global contact_address1
    contact_address1 = os.getenv('CONTACT_ADDRESS1')

    global contact_city
    contact_city = os.getenv('CONTACT_CITY')

    global contact_country
    contact_country = os.getenv('CONTACT_COUNTRY')

    global contact_postalCode
    contact_postalCode = os.getenv('CONTACT_POSTAL_CODE')

    global contact_state
    contact_state = os.getenv('CONTACT_STATE')

    global contact_email
    contact_email = os.getenv('CONTACT_EMAIL')

    global contact_nameFirst
    contact_nameFirst = os.getenv('CONTACT_NAME_FIRST')

    global contact_nameLast
    contact_nameLast = os.getenv('CONTACT_NAME_LAST')

    global contact_phone
    contact_phone = os.getenv('CONTACT_PHONE')