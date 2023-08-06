from setuptools import find_packages, setup

requirements = ['scipy', 'pandas', 'pyranges', 'anndata', 'numpy', 'fisher', 'pykeen', 'torch', 'scvi-tools']

setup(
    name='alethiomics',
    packages=find_packages(include=['alethiomics', 'alethiomics.*']),
    version='0.2.4',
    install_requires=requirements,
    description='Alethiomics data analysis utils',
    author='Alethiomics Ltd',
    license='MIT',
)
