{
    'name': 'Hospital',
    'version': '1.0',
    'depends': ['base'],
    'author': 'Olena',
    'category': 'category',
    'description': """ DB for hospital""",
    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_menus.xml',
        'views/hr_hospital_doctor.xml',
        'views/hr_hospital_patient.xml',
        'views/hr_hospital_disease.xml'
    ],
    'demo': [
        'data/hospital_demo_doctor.xml',
        'data/hospital_demo_patient.xml',
        'data/hospital_demo_disease.xml',
    ],
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}