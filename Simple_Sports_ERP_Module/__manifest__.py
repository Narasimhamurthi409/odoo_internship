{
    'name': 'Simple Sports ERP Module',
    'version': '1.0',
    'summary': 'Basic module with two views',
    'category': 'Sports',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/athlete_view.xml',
        'views/event_view.xml',
        'data/data.xml',
    ],
    'installable': True,
    'auto_install': False,
}