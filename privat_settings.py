

# SMTP(mail)
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dmitriy.evseev.99@gmail.com'
EMAIL_HOST_PASSWORD = 'pniraopitkyprsbe'
EMAIL_PORT = 587


MAIL = {
    'title': 'MicroMason',
    'phone': '+380508840819',
    'links': {
        'backend': {
            'main': 'http://192.168.1.228:8000',
        },
        'frontend': {
            'main': 'http://192.168.1.228:8081',
            'cabinet': 'http://192.168.1.228:8081/account/',
        },
    }
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1072563183925-8t7ri7d7ikbjcrfna2bu123pt93t90su.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'IWH3HU3Lpvcp25_PHXeuhL6q'


#   LiqPay

LIQPAY_PUBLIC_KEY = 'sandbox_i80911148214'
LIQPAY_PRIVATE_KEY = 'sandbox_WOrksBUssSUPN88B36ppPsDcRn4i5cL2AxPaLFyV'
LIQPAY_VERSION = '3'
LIQPAY_CURRENCY = 'UAH'


# Новая почта

NOVA_POSHTA_API_KEY = '9f114041505c633de9523ec691981d44'
NOVA_POSHTA_PHONE_NUMBER = '+380508840819'