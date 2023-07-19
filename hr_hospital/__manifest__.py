{
    'name': 'Hospital',
    'version': '1.0',

    'author': 'Olena',
    'category': 'category',
    'description': """ DB for hospital""",

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_menus.xml',
        'views/hr_hospital_doctor.xml',
        'views/hr_hospital_patient.xml',
        'views/hr_hospital_disease.xml',
        'views/hr_hospital_specialty.xml',
        'views/hr_hospital_diagnosis.xml',
        'views/hr_hospital_visit.xml',
        'views/hr_hospital_doctor_history.xml',
        'views/hr_hospital_doctor_schedule.xml',
        'views/hr_hospital_sample.xml',
        'views/hr_hospital_sample_type.xml',
        'wizard/new_doctor_wizard_view.xml',
        'wizard/new_schedule_wizard_view.xml',
    ],
    'demo': [
        'data/hospital_demo_doctor.xml',
        'data/hospital_demo_patient.xml',
        'data/hospital_demo_disease_group.xml',
        'data/hospital_demo_disease.xml',
        'data/hospital_demo_specialty.xml',

    ],
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}