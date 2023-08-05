from setuptools import setup, find_packages


setup(
    name='Firestack',
    license='MIT',
    author="Thandden",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Thandden/Firestack',
    keywords='Authenticate Python apps with Firebase.',
    install_requires=[
          'pydantic',
          'requests'
      ],

)