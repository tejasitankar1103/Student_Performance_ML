# find_packages is used to find all packages in the current directory
# setup is used to define the package metadata and configuration
from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."
# This is a variable that will be used to store the name of the file that contains the list of requirements
def get_requirements(file_path: str) -> List[str]:
    """
    This function reads a requirements file and returns a list of packages(requirements).
    It removes any empty lines and comments.
    """
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]  # remove new line characters
        requirements = [req for req in requirements if req]  # remove empty lines
        requirements = [req for req in requirements if not req.startswith("#")]  # remove comments
        
        # If the requirement is in the form of -e . then we remove it
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name = "Student_Performance_ML_Project",
    version = "0.0.1",
    author = "Tejas Itankar",
    author_email="tejasitankar10@gmail.com",
    packages=find_packages(),
    # install_requires=[  this is can get a lot big and messy, 
    # so we can use a requirements.txt file instead and get it by 
    #creating a function to read the file(requirements.txt) 
    #     "numpy",
    #     "pandas",
    #     "scikit-learn",
    #     "matplotlib",
    #     "seaborn",
    #     "jupyterlab",
    #     "ipython",
    #     "requests"
    # ]
    install_requires=get_requirements("requirements.txt"),
    description="A machine learning project to predict student performance"
)