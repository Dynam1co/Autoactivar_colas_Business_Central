import base64
import json
import requests
import time
from datetime import datetime


def getUserPassBase64(company) -> str:
    message = company['user'] + ':' + company['pass']
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    return base64_message


def postData(url, payload, company) -> str:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + getUserPassBase64(company),
        'Cookie': 'RuntimeTenantAffinity=msweua3554t49851626'
    }

    try:
        response = requests.request('POST', url, headers=headers, data=payload)
    except requests.exceptions.Timeout:
        print('Superado el tiempo de espera al levantar la cola.')
        return ''
    except requests.exceptions.RequestException as e:
        print(f'Error al levantar la cola. {e}')
        return ''

    return response.json()


def activaCola(idCola, company) -> bool:
    data = {}

    data['pIdCola'] = idCola

    json_data = json.dumps(data)

    result = postData(company['endpoint_activar'], json_data, company)

    return result['value']


def getColas(company) -> str:
    url = company['endpoint_colas']

    payload={}

    headers = {
        'Authorization': 'Basic ' + getUserPassBase64(company),
        'Cookie': 'RuntimeTenantAffinity=msweua3554t49851626'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.Timeout:
        print('Superado el tiempo de espera al leer las colas.')
        return ''
    except requests.exceptions.RequestException as e:
        print(f'Error al leer las colas. {e}')
        return ''


    return response.json()


def update_log(item, companyname):
    try:
        file_object = open('log.txt', 'a')

        file_object.write('\n{0};{1};{2};{3};{4};{5}'.format(
            companyname,
            str(datetime.now()),
            item['Object_Type_to_Run'],
            item['Object_ID_to_Run'],
            item['Description'],
            'Cola reactivada'
        ))
    except IOError:
        print('Error al escribir en el log')
    finally:
        file_object.close()


def procesa_empresa(company):
    json_respuesta = getColas(company)

    if 'value' not in json_respuesta:
        print('Error. No se encuentra atribugo value en la respuesta')
        print(f'Respuesta {str(json_respuesta)}')
        return

    for item in json_respuesta['value']:
        if (item['Object_ID_to_Run'] >= 50000) and (item['Object_ID_to_Run'] <= 99999):
            if item['Status'] not in ['Ready', 'In Process']:
                print('Cola tipo: {0} id: {1} nombre: {2} esta parada. Se va a arrancar.'.format(
                    item['Object_Type_to_Run'],
                    item['Object_ID_to_Run'],
                    item['Description'])
                )

                if activaCola(item['ID'], company):
                    update_log(item, company['name'])
                    print('')
                    print('Correcto')
                else:
                    print('')
                    print('No se ha podido reactivar')


if __name__ == '__main__':
    config_path = 'config.ini'

    with open(config_path) as f:
        conf = json.load(f)

        while 1:
            print('##############################')
            print(datetime.now())
            print('##############################')
            print('')

            for company in conf['companies']:
                print(f"Comprobando empresa: {company['name']}")

                procesa_empresa(company)

                print('')
                print('---------------------------------')
                print('')

            time.sleep(120)
