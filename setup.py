from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='''ckanext-moeiemailer''',
    entry_points='''
        [ckan.plugins]
        moeiemailer=ckanext.moeiemailer.plugin:MailerMoei
    ''',
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    },
)
