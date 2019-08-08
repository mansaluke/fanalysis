from setuptools import setup, find_packages

setup(name='fanalyasis',
      version='0.9',
      description='Machine learning for FOREX data',
      author='Luke Mcleary',
      author_email='lukemcleary95@gmail.com',
      license='Apache 2.0',
      keywords = ['pandas', 'sklearn', 'data', 'forex'],
      url = 'https://github.com/mansaluke/fanalysis',
      packages = find_packages(),
      include_package_data = True,
      install_requires = ['matplotlib>=3.0.2'
                          'numpy>=1.16.0'
                          'pandas>= 0.24.0'
                          'pydot>=1.4.1'
                          'graphviz>=0.10.1'
                          'numba>= 0.16.0'
                          'quandl'
                          'requests'
                          'bs4'
                          'scikit-learn'
                          'ipykernel'
                          'pydotplus'
                          'tables>=3.5.2'
                          'feather-format'
                          'pyarrow'
                          'tqdm==4.32.1'],
	  zip_safe=False)