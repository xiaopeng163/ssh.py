from setuptools import setup


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='ssh.py',
    version='0.1',
    url='https://github.com/xiaopeng163/ssh.py',
    license='Apache 2.0',
    author='Peng Xiao',
    author_email='xiaoquwl@gmail.com',
    keywords='GitHub SSH',
    description='SSH configuration management',
    long_description=long_description,
    platforms='any',
    install_requires=[
        'cliff>=2.2.0'
    ],
    scripts=['ssh.py'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
