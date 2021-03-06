# -*- coding: utf-8 -*-
from setuptools import setup

setup(
        name='myslicelib',
        version='0.1',
        description='MySlice Python Library',
        url='',
        author=u'Ciro Scognamiglio',
        author_email='ciro.scognamiglio@lip6.fr',
        license='MIT',
        packages=['myslicelib'],
        classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            # Pick your license as you wish (should match "license" above)
             'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3',
        ],
        keywords='myslice testbed api',
        #install_requires=[''],
        #zip_safe=False,
        #include_package_data=True
)