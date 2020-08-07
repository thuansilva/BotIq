from iqoptionapi.stable_api import IQ_Option
import time,json
from datetime import datetime
from dateutil import tz

API = IQ_Option("pobibom865@in4mail.net", "botteste")
API.connect()

API.change_balance('PRACTICE') # PRACTICE / REAL

while True: 
    if API.check_connect() == False:
        print('erro ao se conectar')
        API.connect()
        
    else: 
        print('voce está conectado!')
        break

    time.sleep(1)

def perfil():
    perfil = json.loads(json.dumps(API.get_profile_ansyc()))
    return perfil


def timestamp_converter(x): # Função para converter timestamp
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora)[:-6]


print(API.get_balance())