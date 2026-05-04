from setuptools import setup, find_packages

setup(
    name="riemann-sniper",
    version="0.1.0",
    author="Твое Имя/Ник",
    author_email="твоя@почта.com",
    description="Fast and accurate hybrid solver for finding Riemann zeta function zeros.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/твой-юзернейм/riemann-sniper",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "mpmath"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)