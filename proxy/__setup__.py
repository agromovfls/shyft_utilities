from setuptools import setup

setup(name='shyft_proxy',
      version='0.1',
      description='Proxy-script for running requent on Hive server',
      url='https://github.com/agromovfls/shyft_utilities',
      author='Andrey Gromov',
      author_email='gromovergec@gmail.com',
      license='MIT',
      packages=['shyft_proxy'],
      install_requires=[
          'pyhive',
          'thrift',
          'sasl',
          'thrift-sasl',
          'Werkzeug'
      ],
      zip_safe=False)