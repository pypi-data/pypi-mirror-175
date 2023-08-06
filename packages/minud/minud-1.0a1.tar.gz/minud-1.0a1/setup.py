from setuptools import setup, find_packages


with open('README.md', 'r') as ld:
    long_description = ld.read()

setup(name='minud',
    version='1.0a1',
    author='Gonzalo Vidal',
    author_email='gsvidal@uc.cl',
    description='MINuD: a tool for the analysis of Mitochondrial Nucleoids Distribution',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RudgeLab/MiNuD',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    install_requires=[        
        'numpy', 
	    'scipy',
	    'pandas',
        'matplotlib',
        'seaborn',
        'scikit-image',
        ],
    setup_requires=[
        'numpy', 
	    'scipy',
	    'pandas',
        'matplotlib',
        'seaborn',
        'scikit-image',
        ],
    packages=find_packages(),
    python_requires='>=3'
)
