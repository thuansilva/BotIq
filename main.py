from iqoptionapi.stable_api import IQ_Option
import time,json
from datetime import datetime
from dateutil import tz
from  dotenv  import  load_dotenv ,  find_dotenv 
import  os 

load_dotenv ( find_dotenv ())

API = IQ_Option(os.getenv("LOGIN"), os.getenv("SENHA"))
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

def banca():
    print(API.get_balance())

def candle_real_time():
    par = 'EURUSD'

    API.start_candles_stream(par,60,1)
    time.sleep(1)

    vela=API.get_realtime_candles(par,60)

    while True:
        for velas in vela:
            print(vela[velas]['close'])
        time.sleep(1)

    API.stop_candles_stream(par,60)


def payout(par, tipo_operacao, timeframe =1 ):
    if tipo_operacao == 'turbo':
        op= API.get_all_profit()
        return int (100* op[par]['turbo'])

    elif tipo_operacao =='digital':
        API.subscribe_strike_list(par, timeframe)
        while True:
            d= API.get_digital_current_profit(par, timeframe)
            if d != False:
                d=int(d)
                break
            time.sleep(1)
        API.unsubscribe_strike_list(par, timeframe)
        return d

def paridade():
    par = API.get_all_open_time()

    for paridade in par['turbo']:
        if par['turbo'][paridade]['open'] == True:
            print('[TURBO]:'+paridade+'| Payout:'+ str(payout(paridade,'turbo')))

    print('\n')

    for paridade in par['digital']:
        if par['digital'][paridade]['open'] == True:
            print('[DIGITAL]:'+paridade+'| Payout:'+ str(payout(paridade,'digital')))

    
paridade()