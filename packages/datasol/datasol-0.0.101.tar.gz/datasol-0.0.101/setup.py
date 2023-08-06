from setuptools import setup

def readme():
    if open('README.md'):
        with open('README.md') as f:
            return f.read()
    else:
        return None
    
setup(
    name='datasol',
    version = '0.0.101',
    description ='Anomaly Detetion',
    long_description=readme(),
    long_description_content_type= 'text/markdown',
    classifiers=['Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9'
    ],
    url='https://github.com/maxmelichov/DATASOL-package',
    author='Maxim Melichov',
    author_email='maxme006@gmail.com',
    license= 'MIT',
    # packages=['roconfiguration'],
    # install_requires=['pandas>=1.5','numpy>=1.2','matplotlib>=3.6','scikit-learn>=1.1','tensorflow>=2.6','keras>=2.6','tensorflow-gpu>=2.9','tensorboard>=2.10'],
    # include_package_data=True,
    extras_require ={"dev":["pytest>=3.7"]},
    zip_safe=False,
    py_modules=["datasol"],
    package_dir={'':'src'},
)