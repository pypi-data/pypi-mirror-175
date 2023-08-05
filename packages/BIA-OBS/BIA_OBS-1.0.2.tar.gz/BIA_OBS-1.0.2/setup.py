from setuptools import setup

setup(
    name='BIA_OBS',
    version='1.0.2',    
    description='Business Impact Assesment',
    long_description_content_type='text/markdown',
    long_description="""
    # BIA Toolkit

        ## Functionality
        This application helps with generating a YAML file for the BIA assesment.
        You fill in the fields and after pressing the 'Generate YAML' button at the end of the document the application outputs a YAML file based on date/time format to the "/Output" folder in the application folder.

        ## Supported Platforms
        The application works on both MacOS & Windows OS & Linux (GUI)

        ## Contact
        Owner: Ferry Stelte
        Programmer: Mick Hilhorst
    
     """,
    url='https://github.com/shuds13/pyexample',
    author='Mick Hilhorst(LooseDevGoose)',
    author_email='mick.hilhorst@gmail.com',
    license='MIT',
    packages=['BIA'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[  'click==8.1.3',
                        'colorama==0.4.5',
                        'Flask==2.2.2',
                        'importlib-metadata==5.0.0',
                        'itsdangerous==2.1.2',
                        'Jinja2==3.1.2',
                        'MarkupSafe==2.1.1',
                        'PyYAML==6.0',
                        'Werkzeug==2.2.2',
                        'zipp==3.9.0',
                      ],

    classifiers=[
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',        
        'Programming Language :: Python :: 3',

    ],
)
