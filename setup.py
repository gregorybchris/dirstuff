"""Setup module for setuptools."""
import json

from pathlib import Path
from setuptools import setup, find_packages


package_dir = Path(__file__).parent.absolute()
requirements = Path(package_dir, 'requirements.txt').read_text().split('\n')
test_requirements = Path(package_dir, 'test-requirements.txt').read_text().split('\n')
version = Path(package_dir, 'version.txt').read_text().strip()


setup(
    name='dirsum',
    description='Directory summary tool.',
    author='Chris Gregory',
    author_email='christopher.b.gregory@gmail.com',
    url='https://github.com/gregorybchris/semigenre',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['directory', 'file', 'summary'],
    version=version,
    license='Apache Software License',
    install_requires=requirements,
    extras_require={'testing': test_requirements},
    packages=find_packages(exclude=['tests']),
    entry_points={"console_scripts": ["dirsum=dirsum.main:run"]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ]
)
