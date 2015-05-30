__author__ = 'gaspardzul'


from setuptools import setup
APP = ['damfara.py']


OPTIONS = {
 'iconfile':'icon.ico',
}

setup(
    app = APP,
    setup_requires = ['py2app'],
    options = {'py2app': OPTIONS},
    name="damfara",
    description= "Compresor de imagenes"
    )