from setuptools import setup
import py2exe

setup(name='shyft_runner',
      version='0.1',
      description='Script for running ETL on Hive server',
      url='https://github.com/agromovfls/shyft_utilities',
      author='Andrey Gromov',
      author_email='gromovergec@gmail.com',
      license='MIT',
      packages=['shyft_runner'],
      install_requires=[
          'colorama',
      ],
      zip_safe=False,
      console=['main.py'],
      options={
        "py2exe": {
            "dll_excludes": ["MSVFW32.dll",
                             "AVIFIL32.dll",
                             "AVICAP32.dll",
                             "ADVAPI32.dll",
                             "CRYPT32.dll",
                             "WLDAP32.dll",
                             "api-ms-win-core-processthreads-l1-1-2.dll",
                             "api-ms-win-core-sysinfo-l1-2-1.dll",
                             "api-ms-win-core-heap-l2-1-0.dll",
                             "api-ms-win-core-delayload-l1-1-1.dll",
                             "api-ms-win-core-errorhandling-l1-1-1.dll",
                             'api-ms-win-core-libraryloader-l1-2-0.dll'
                             'api-ms-win-core-string-obsolete-l1-1-0.dll',
                             'api-ms-win-core-libraryloader-l1-2-0.dll'
                            ]


        }
    }
)
