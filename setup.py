import setuptools

setuptools.setup(
    name="visdag",
    packages=setuptools.find_packages(exclude=["visdag_tests"]),
    install_requires=[
        "dagster==0.15.7",
        "dagit==0.15.7",
        "pytest",
    ],
)
