"""
Seller Constants
"""

from django.utils.translation import gettext_lazy as _


# State constants
STATE_AC = 'AC'
STATE_AL = 'AL'
STATE_AP = 'AP'
STATE_AM = 'AM'
STATE_BA = 'BA'
STATE_CE = 'CE'
STATE_DF = 'DF'
STATE_ES = 'ES'
STATE_GO = 'GO'
STATE_MA = 'MA'
STATE_MT = 'MT'
STATE_MS = 'MS'
STATE_MG = 'MG'
STATE_PA = 'PA'
STATE_PB = 'PB'
STATE_PR = 'PR'
STATE_PE = 'PE'
STATE_PI = 'PI'
STATE_RJ = 'RJ'
STATE_RN = 'RN'
STATE_RS = 'RS'
STATE_RO = 'RO'
STATE_RR = 'RR'
STATE_SC = 'SC'
STATE_SP = 'SP'
STATE_SE = 'SE'
STATE_TO = 'TO'


# State choices
STATE_CHOICES = [
    (STATE_AC, _('Acre')),
    (STATE_AL, _('Alagoas')),
    (STATE_AP, _('Amapá')),
    (STATE_AM, _('Amazonas')),
    (STATE_BA, _('Bahia')),
    (STATE_CE, _('Ceará')),
    (STATE_DF, _('Distrito Federal')),
    (STATE_ES, _('Espírito Santo')),
    (STATE_GO, _('Goiás')),
    (STATE_MA, _('Maranhão')),
    (STATE_MT, _('Mato Grosso')),
    (STATE_MS, _('Mato Grosso do Sul')),
    (STATE_MG, _('Minas Gerais')),
    (STATE_PA, _('Pará')),
    (STATE_PB, _('Paraíba')),
    (STATE_PR, _('Paraná')),
    (STATE_PE, _('Pernambuco')),
    (STATE_PI, _('Piauí')),
    (STATE_RJ, _('Rio de Janeiro')),
    (STATE_RN, _('Rio Grande do Norte')),
    (STATE_RS, _('Rio Grande do Sul')),
    (STATE_RO, _('Rondônia')),
    (STATE_RR, _('Roraima')),
    (STATE_SC, _('Santa Catarina')),
    (STATE_SP, _('São Paulo')),
    (STATE_SE, _('Sergipe')),
    (STATE_TO, _('Tocantins')),
]


# Referrals constants
FRIENDS = 'friends'
INSTAGRAM = 'instagram'
FACEBOOK = 'facebook'
TWITTER = 'twitter'
OTHERS = 'others'


# Telephone Regex
TELEPHONE_NUMBER_REGEX = r'^[0-9()+-].+$'


# Order means and fields pairs
MEANS_FIELDS_PAIRS = {
    'telephone': 'telephone_number',
    'whatsapp': 'whatsapp_number',
    'ifood': 'ifood_url',
    'uber_eats': 'uber_eats_url',
    'rappi': 'rappi_url',
    'website': 'site_url',
}
