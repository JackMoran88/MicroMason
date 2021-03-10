import requests
from django.conf import settings


def toApi(modelName, calledMethod, methodProperties={}):
    """
    :param modelName:
    :param calledMethod:
    :param methodProperties:
    :return: Response from api
    """
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "apiKey": "9f114041505c633de9523ec691981d44",
        "modelName": modelName,
        "calledMethod": calledMethod,
        "methodProperties": methodProperties,
    }

    result = requests.post(
        'https://api.novaposhta.ua/v2.0/json/',
        headers=headers,
        json=data
    )

    if not (result.json()['success']):
        print(result.json()['errors'])
    return result


def getCities():
    data = {
        'modelName': 'Address',
        'calledMethod': 'getCities',

    }
    return toApi(**data)


def getWarehouses():
    data = {
        'modelName': 'Address',
        'calledMethod': 'getWarehouses',
    }
    return toApi(**data)


def getDocumentList():
    data = {
        'modelName': 'InternetDocument',
        'calledMethod': 'getDocumentList',
    }
    return toApi(**data)


def deleteDocument(barcodes):
    data = {
        "modelName": "InternetDocument",
        "calledMethod": "delete",
        "methodProperties": {
            "DocumentBarcodes": barcodes
        }
    }
    return toApi(**data)


def getStatusDocuments(documents):
    """
    :param documents: [{DocumentNumber,Phone}]
    :return: Response from api
    """""
    data = {
        'modelName': 'TrackingDocument',
        'calledMethod': 'getStatusDocuments',
        'methodProperties': {
            'Documents': documents
        }
    }
    return toApi(**data)


def saveCounterparty(properties):
    data = {
        'modelName': 'Counterparty',
        'calledMethod': 'save',
        'methodProperties': properties
    }
    return toApi(**data)


def saveDocument(properties):
    data = {
        'modelName': 'InternetDocument',
        'calledMethod': 'save',
        "methodProperties": properties,
    }
    return toApi(**data)
