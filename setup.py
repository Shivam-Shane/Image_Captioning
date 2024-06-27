from setuptools import find_packages, setup

def get_requirements(file_path: str):
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements

setup(
    name="ImageCaptioning",
    version="0.1.3",
    author="Shivam",
    author_email='sk0551460@gmail.com',
    description="A package that takes an image as input and returns a caption based on the image's data.",
    url="https://github.com/Shivam-Shane/Image_Captioning.git",  # Update with your actual URL
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)
#---How to use this package --- run in terminal pip install . --------------------------------