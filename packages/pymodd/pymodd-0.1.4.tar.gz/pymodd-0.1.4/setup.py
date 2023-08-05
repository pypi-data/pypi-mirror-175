from distutils.core import setup

if __name__ == '__main__':
    setup(
        name='pymodd',
        url='https://github.com/jeff5343/Pymodd',
        version='0.1.4',
        author='Jeff',
        packages=['pymodd', 'pymodd.utils', 'pymodd.console_scripts'],
        entry_points={
            'console_scripts': [
                'generate-game = pymodd.console_scripts.generate:main',
            ]
        },
        license='MIT',
        description='A package for creating modd.io games using python!',
        long_description=open('README.rst').read(),
        install_requires=[
            'case-converter==1.1.0'
        ],
    )
