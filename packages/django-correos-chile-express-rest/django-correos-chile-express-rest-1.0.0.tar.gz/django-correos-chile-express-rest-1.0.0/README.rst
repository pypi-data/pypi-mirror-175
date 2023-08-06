# Linets Correos Chile


## Starting 🚀
_These instructions will allow you to install the library in your django project._

### Current features 📋

-   Generate order in Correos Chile.
-   Generate default data for create order in Correos Chile.

### Pre-requisitos 📋

-   Python >= 3.7
***
## Installation 🔧

1. To get the latest stable release from PyPi:
```
pip install django-correos-chile-rest
```
or

2. From a build
```
git clone https://gitlab.com/linets/ecommerce/oms/integrations/django-correos
```

```
cd {{project}} && git checkout develop
```

```
python setup.py sdist
```
and, install in your project django
```
pip install {{path}}/django-correos/dist/{{tar.gz file}}
```

3. Settings in django project

```
DJANGO_CORREOS_CHILE_EXPRESS = {
    'CORREOS_CHILE': {
        'BASE_URL': '<CORREOS_CHILE_BASE_URL>',
        'USER': '<CORREOS_CHILE_USER>',
        'PASSWORD': '<CORREOS_CHILE_PASSWORD>',
        'TOKEN': '<CORREOS_CHILE_TOKEN>',
        'COD_SERVICIO': '<CORREOS_CHILE_COD_SERVICIO>',
        'COD_REF': '<CORREOS_CHILE_COD_REF>',
        'TYPE_POR': '<CORREOS_CHILE_TYPE_POR>',
        'DEV_CON': '<CORREOS_CHILE_DEV_CON>',
    },
    'SENDER': {
        'ADMISSION': '<CORREOS_CHILE_ADMISSION>',
        'CLIENT': '<CORREOS_CHILE_CLIENT>',
        'CENTRO': '<CORREOS_CHILE_CENTRO>',
        'NAME': '<CORREOS_CHILE_NAME>',
        'ADDRESS': '<CORREOS_CHILE_ADDRESS>',
        'COUNTRY': '<CORREOS_CHILE_COUNTRY>',
        'POSTALCODE': '<CORREOS_CHILE_POSTALCODE>',
        'CITY': '<CORREOS_CHILE_CITY>',
        'RUT': '<CORREOS_CHILE_RUT>',
        'CONTACT_NAME': '<CORREOS_CHILE_CONTACT_NAME>',
        'CONTACT_PHONE': '<CORREOS_CHILE_CONTACT_PHONE>',
    }
}
```

## Usage 🔧

1. Create instance to be sent
    ```
    import json
    from types import SimpleNamespace

    dict_ = {
        'reference': '99999',
        'created_at': '12/12/21',
        'shipping_date': '12/12/21',
        'expiration_date': '26/12/21'
        'tracking_code': '6075620-1',
        'transport_guide_number': '1121632479536-01-1',
        'purchase_number': 'CLV0048146676851-1',
        'customer': {
            'first_name': 'Marcos',
            'last_name': 'Sac',
            'full_name': 'Marcos Sac',
            'phone': '932932932',
            'email': 'test@gmail.com',
            'rut': '16936195-9'
        },
        'address': {
            'street': 'ALEJANDRO VENEGAS CADIZ',
            'number': '513',
            'unit': 'DEPTO 6A',
            'full_address': 'ALEJANDRO VENEGAS CADIZ 513 DEPTO 6A'
        },
        'commune': {
            'name': 'Aisen',
            'code': '',
            'zone_code': '11201',
            'zone_post': 'WPA',
        },
        'location': {
            'code': 'MONTANDON',
            'name': 'MNN',
        },
        'region': {
            'name': 'Aysén del General Carlos Ibáñez del Campo',
            'code': '11',
            'iso_code': 'CL-XI',
        }
    }

    instance = json.loads(json.dumps(dict_), object_hook=lambda attr: SimpleNamespace(**attr))
    ```


2. Generate default data for create a order in Correos Chile:
```
from correos_chile.handler import CorreosHandler

handler = CorreosHandler()
default_data = handler.get_default_payload(instance)

Output:
{
    "nroDTE": 0,
    "codCliente": "888888",
    "posicionInicial": 0,
    "formatoEtiqueta": "PDF",
    "modo": "json",
    "data": [
        {
            "codAdmision": "PRUEBA01",
            "codCentro": "",
            "codServicio": "24",
            "remitente": {
                "nombre": "PRUEBA CORREOSCHILE",
                "codPais": "056",
                "comuna": "ESTACION CENTRAL",
                "direccion": "EXPOSICION 221. Sexto 6",
                "codPostal": "9160002",
                "rut": "55.555.555-5",
                "contacto": "Soporte ecommerce",
                "telefono": "6009502020",
                "email": "soporte.ecommerce@correos.cl"
            },
            "destinatario": {
                "nombre": "CLIENTE DE PRUEBA",
                "codPais": "056",
                "comuna": "ESTACION CENTRAL",
                "direccion": "EXPOSICION 221. Sexto 6",
                "codPostal": "",
                "rut": "55.555.555-5",
                "contacto": "cliente de prueba",
                "telefono": "555555555",
                "email": "cliente@deprueba.cl"
            },
            "pagoSeguro": 0,
            "bultos": 1,
            "kilos": 1,
            "volumen": 0.001,
            "codReferencia": "prbcch0001",
            "observaciones": "Observaciones",
            "observacionesInternas": "Observaciones de uso interno",
            "tipoMercancia": "",
            "tipoPortes": "P",
            "valorDeclarado": 10000,
            "devolucionConforme": 0,
            "importeReembolso": 0,
            "numDocumentos": 0
        }
    ]
}
```

3. Create a order in Correos Chile:
```
from correos_chile.handler import CorreosHandler

handler = CorreosHandler()
response = handler.create_shipping(default_data)

Output:
{
    "info": [
        {
            "estado": "WARNING",
            "mensaje_1": "El parámetro rut de remitente se ajustó como 55555555-5",
            "mensaje_2": "El parámetro rut de destinatario se ajustó como 55555555-5",
            "admision": {
                "codAdmision": "PRUEBA01",
                "abreviaturaCentro": "888888",
                "codSucursal": "",
                "nombreSucursal": "",
                "codDelegacionDestino": "864",
                "nombreDelegacionDestino": "PLANTA CEP RM",
                "direccionDestino": "EXPOSICION 221  SEXTO 6",
                "cuartel": "4",
                "codEncaminamiento": "12491600027",
                "sector": "2",
                "numeroEnvio": "880000001459",
                "comunaDestino": "ESTACION CENTRAL",
                "abreviaturaServicio": "PED",
                "SDP": "1",
                "codigoBarras": [
                    "12491600027880000001459001"
                ]
            }
        }
    ],
    "errores": [],
    "archivos": [
        {
            "nombre": "etiquetas_20211229_174300",
            "extension": "pdf",
            "str64Data": ""
        }
    ]
}
```
