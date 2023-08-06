from pathlib import Path

from setuptools import find_packages, setup

from gui_api_tkinter.lib import version


mod_name = 'gui-api-tkinter'

this_directory = Path(__file__).parent
long_desc = (this_directory / "README.md").read_text()
long_version = version.version.replace('.', '_')

setup(
    name=mod_name,
    include_package_data=True,
    packages=find_packages(include=f'{mod_name}*', ),
    version=version.version,
    license='MIT',
    description='Base Class for interacting with a GUI based in tkinter',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='JA',
    author_email='cppgent0@gmail.com',
    url=f'https://github.com/cppgent0/{mod_name}',
    download_url=f'https://github.com/cppgent0/{mod_name}/archive/refs/tags/v_{long_version}.tar.gz',
    keywords=['gui', 'tkinter', 'test', 'verification'],
    install_requires=[
        'pytest',
        'socket_oneline',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
