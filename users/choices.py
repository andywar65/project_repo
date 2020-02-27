from django.utils.html import format_html

GENDER = [('F', 'Femmina'), ('M', 'Maschio'), ]

NOTICE = [('SPAM', 'Da inviare'), ('DONE', 'Già inviata'), ]

SECTOR = [('0-NO', 'No'), ('3-FI', 'No, solo i figli'),
    ('1-YC', 'Sì, con il corso'), ('2-NC', 'Sì, senza corso'), ]

SECTOR_DICT = {'0-NO': 'No', '3-FI': 'No, solo i figli',
    '1-YC': 'Sì, con il corso', '2-NC': 'Sì, senza corso', }

COURSE = [
    ('INTU', 'Integrazione per materiale socio UISP'),
    ('INTF', 'Integrazione per materiale socio FIDAL'),
    ]

NO_COURSE = [('UNA', 'UISP non agonistico'),
    ('UA', 'UISP agonistico'),
    ('FID', 'FIDAL agonistico'),
    ]

MC_STATE = [
    ('0-NF', 'Manca il file'),
    ('1-VF', 'Verifica file'),
    ('2-RE', 'Regolare'),
    ('6-IS', 'In scadenza'),
    ('3-SV', 'Scaduto, da verificare'),
    ('4-SI', 'Scaduto, inviare notifica'),
    ('5-NI', 'Scaduto, notifica inviata'),
    ]

SETTLED = [
    ('VI', 'Verifica importo totale'),
    ('YES', 'A posto'),
    ('NO', 'No!'),
    ]

MC_STATE_DICT = {
    '0-NF': format_html('<span style="color: red;">{}</span>',
        'manca il file'),
    '1-VF': format_html('<span style="color: red;">{}</span>',
        'verificare file'),
    '2-RE': 'regolare',
    '3-SV': format_html('<span style="color: red;">{}</span>',
        'scaduto, da verificare'),
    '4-SI': format_html('<span style="color: red;">{}</span>',
        'scaduto, inviare notifica'),
    '5-NI': format_html('<span style="color: red;">{}</span>',
        'scaduto, notifica inviata'),
    '6-IS': format_html('<span style="color: red;">{}</span>',
        'in scadenza'),
    }

SETTLED_DICT = {
    'VI': 'Verifica importo totale',
    'YES': 'In regola con i pagamenti, grazie!',
    'NO': format_html('<span style="color: red;">{}</span>',
        'Non in regola con i pagamenti!'),
    None: 'Nessun dato sui pagamenti',
    }
