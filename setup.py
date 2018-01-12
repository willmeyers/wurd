from setuptools import setup


setup(
    name = 'wurd',
    version = '1.0',
    description = 'A password manager',
    author = 'Will Meyers',
    author_email = 'will@willmeyers.net',
    packages = ['wurd'],
    entry_points = {
        'console_scripts': [
            'wurd = wurd.__main__:main'
        ]
    }
)
