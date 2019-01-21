from setuptools import setup, find_namespace_packages

setup(name='ml-utils',
      version='0.1',
      author='Saad Abderrazzaq',
      author_email='sabderr@example.com',
      description='Collection of machine learning utilities.',
      url='https://github.com/sabderra/ml_utils',
      install_requires=['jsonschema>=2.6.0', 'cloudant>=2.10.2', 'numpy>=1.15.1', 'Keras>=2.2.2', 'tensorflow>=1.9.0'],
      license='MIT',
      package_dir={'': 'src'},
      packages=find_namespace_packages(where='src')
      )
