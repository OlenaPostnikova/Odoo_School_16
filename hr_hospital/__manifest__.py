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
        'views/hr_hospital_patient.xml'
    ],
    'demo': [
        'demo/hospital_demo.xml',
    ]
}