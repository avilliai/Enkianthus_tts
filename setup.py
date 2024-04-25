from setuptools import setup, find_packages

setup(
    name='modelscope_tts',
    version='0.1.0',
    url='https://github.com/avilliai/modelscopeTTS',
    author='avillia',
    author_email='larea06@gmail.com',
    description='modelscopeTTS Unofficial api',
    packages=find_packages(),
    install_requires=[
        'httpx',
     ],
)