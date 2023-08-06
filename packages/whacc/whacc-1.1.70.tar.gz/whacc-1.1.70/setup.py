from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


import os
from whacc import utils

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename[0] != '.':
                paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('/Users/phil/Dropbox/HIRES_LAB/GitHub/whacc/whacc/whacc_data')


# packages = find_packages('/Users/phil/Dropbox/HIRES_LAB/GitHub/whacc/')

# package_data={'thing': ['data/*.bin']}
# exclude_package_data={'whacc': ['whacc_data/final_model/final_resnet50V2_full_model/']}
# include_package_data=True
#
#
packages=find_packages()  # include all packages under src
# package_dir={"": "src"},   # tell distutils packages are under src
#
# include_package_data=True,    # include everything in source control

# ...but exclude README.txt from all packages
exclude_package_data={"": ["*final_resnet50V2_full_model*", "*training_data*"]}


setup(name='whacc',
      version='1.1.70',
      author="Phillip Maire",
      license='MIT',
      description='Automatic and customizable pipeline for creating a CNN + light GBM model to predict whiskers contacting objects',
      packages=find_packages(),
      author_email='phillip.maire@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/hireslab/whacc",
      zip_safe=False,
      classifiers=["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"],
      python_requires='>=3.6',
      install_requires=["natsort==7.1.1"],
      package_data={'': extra_files},
      exclude_package_data=exclude_package_data,
      # package_data={'whacc': ['whacc_data/*',
      #                         'whacc/whacc_data/feature_data/*',
      #                         'whacc/whacc_data/feature_data/*.pkl',
      #                         'whacc/whacc_data/*.png',
      #                         'whacc_data/final_model/final_resnet50V2_full_model/variables/*',
      #                         'whacc_data/final_model/final_resnet50V2_full_model/assets/*',
      #                         'whacc_data/final_model/final_resnet50V2_full_model/*',
      #                         'whacc_data/final_model/*',
      #                         'whacc/whacc_data/final_model/final_resnet50V2_full_model/*pb',
      #                         'whacc/whacc_data/final_model/final_resnet50V2_full_model/variables/*.index',
      #                         'whacc/whacc_data/final_model/final_resnet50V2_full_model/variables/*.data-00000-of-00001']},
      include_package_data=True
      )

