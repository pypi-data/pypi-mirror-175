from setuptools import setup, find_packages
#python setup.py sdist bdist_wheel
#makes dist, build, name.egg-info
#twine upload dist/* --verbose
setup(
    name = "chipipexample",
    version = "0.1.9",
    packages = find_packages(),
    description='A simple example of a Python package',
    author='Nathan Park',
    author_email='<nathanschool2000@gmail.com>',
    keywords=['example', 'education'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Education',
    ],
    install_requires=['numpy', 'lmfit','uncertainties'],

)