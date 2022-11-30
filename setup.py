<<<<<<< Updated upstream
from setuptools import find_packages, setup

if __name__ == "__main__":
    setup(
        name="visdag",
        packages=find_packages(exclude=["visdag_tests"]),
        install_requires=[
            "dagster",
            "matplotlib",
            "pandas",
            "nbconvert",
            "nbformat",
            "ipykernel",
            "jupytext",
            "vipersci @ file://localhost/Work/VIPER/vipersci#egg=vipersci"
    
        ],
        extras_require={"dev": ["dagit", "pytest"]},
    )
=======
import setuptools

setuptools.setup(
    name="visds",
    packages=setuptools.find_packages(exclude=["visds_tests"]),
    install_requires=[
        "dagster==0.15.7",
        "dagit==0.15.7",
        "pytest",
    ],
)
>>>>>>> Stashed changes
