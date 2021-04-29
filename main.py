import conf_management as cfg
import base64
import json
import requests


def getUserPassBase64(produccion) -> str:
    message = cfg.get_user(produccion) + ':' + cfg.get_pass(produccion)
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    return base64_message

def postData(url, payload, produccion) -> str:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + getUserPassBase64(produccion),
        'Cookie': 'RuntimeTenantAffinity=msweua3554t49851626'
    }

    print(url)

    response = requests.request('POST', url, headers=headers, data=payload)

    return response.json()

def activaCola(idCola, produccion):
    data = {}

    data['pIdCola'] = idCola

    json_data = json.dumps(data)

    result = postData(cfg.get_endpoint_activar_colas(produccion), json_data, produccion)

    print(result)

def getColas(produccion) -> str:
    url = cfg.get_endpoint_consulta_colas(produccion)

    payload={}

    headers = {
        'Authorization': 'Basic ' + getUserPassBase64(produccion),
        'Cookie': 'RuntimeTenantAffinity=msweua3554t49851626'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


if __name__ == '__main__':
    produccion = False

    json_respuesta = getColas(produccion)

    # for key, value in json_respuesta.items():
        # print(key, ':', value)

    for item in json_respuesta['value']:
        if (item['Object_ID_to_Run'] >= 50000) and (item['Object_ID_to_Run'] <= 70000):
            if item['Status'] not in ['Ready', 'In Process']:
                print('Cola tipo: {0} id: {1} nombre: {2} esta parada. Se va a arrancar.'.format(
                    item['Object_Type_to_Run'],
                    item['Object_ID_to_Run'],
                    item['Description']))

                activaCola(item['ID'], produccion)

