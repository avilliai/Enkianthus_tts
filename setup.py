from setuptools import setup, find_packages
with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='modelscope_tts',
    version='0.1.2',
    url='https://github.com/avilliai/modelscopeTTS',
    author='avillia',
    author_email='larea06@gmail.com',
    description='modelscopeTTS Unofficial api',
    packages=find_packages(),
    install_requires=[
        'httpx',
     ],
)