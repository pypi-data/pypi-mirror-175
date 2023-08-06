from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='brain-pred-toolbox',
      version='2.3.1',
      long_description=long_description,
      long_description_content_type='text/markdown',
      description='The Brain Predictability toolbox (BPt) is a ' +
      'Python based machine learning library designed to work with ' +
      'a range of neuroimaging data.',
      url='http://github.com/sahahn/BPt',
      author='Sage Hahn',
      author_email='sahahn@euvm.edu',
      license='MIT',
      packages=find_packages(),
      python_requires=">=3.8",
      install_requires=[
          'scikit-learn>=1.1.0',
          'numpy>=1.21',
          'scipy>=1.2',
          'pandas>=1.1.5',
          'matplotlib>=3.2.2',
          'seaborn>=0.9',
          'scikit-image>=0.16',
          'tqdm>=4.51',
          'nevergrad>=0.5.0',
          'Ipython',
          'joblib>=1',
          'loky',
          'threadpoolctl>=3'
      ],
      extras_require={
          'extra': ['lightgbm>=3.3.0',
                    'nilearn>=0.9',
                    'python-docx',
                    'mvlearn',
                    'imblearn',
                    'xgboost>=1.4',
                    'bp-neurotools'],
       },
      test_suite='pytest',
      tests_require=['pytest', 'coverage'],
      zip_safe=False)
