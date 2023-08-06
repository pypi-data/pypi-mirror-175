from setuptools import setup, find_packages

setup(
    name='Mensajes-OniNicole',
    version='6.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='OniNicole',
    author_email='nico_meli_99@gmail.com',
    url='https://test.pypi.org/user/OniNicole/',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License','Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities']
)

