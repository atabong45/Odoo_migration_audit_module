{
    'name' : 'My first module',
    'version' : '1',
    'summary': 'My first custom module',
    'author': 'Atabong',
    'sequence': 100,
    'description': """
            rien a dire Tonton
   """,
    'category': 'Tools',
    'website': 'https:atabong-portfolio.vercel.app',
    'images' : [],
    'depends' : [
        'sale',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/patient.xml',
        'views/sale.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'views/appointment_view.xml',
    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,

    'license': 'LGPL-3',
}
