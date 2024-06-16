from setuptools import setup, find_packages
with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='Enkianthus_tts',
    version='0.1.8',
    url='https://github.com/avilliai/modelscopeTTS',
    author='avillia',
    author_email='larea06@gmail.com',
    description='modelscopeTTS Unofficial api,see https://github.com/avilliai/modelscopeTTS for more information',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'websockets',
        'requests',
     ],
)