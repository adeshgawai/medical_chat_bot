from setuptools import find_packages, setup
setup(
    name='RAG based medical chatbot',
    version='0.1',
    author='Adesh Gawai',
    author_email='adesh@gmail.com',
    packages=find_packages(), 
    install_requires=[]
)

# this particular code is there to set our project as a package so that we can import it in other files.
# after creating this go to requirements.txt and add -e . to it.
# then run pip install -r requirements.txt to install the package in editable mode.