import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sbat",
    version="0.0.10",
    author="Alexandra Skyslakova",
    author_email="alexandra.skyslakova@gmail.com",
    description="A tool for strand bias analysis of NGS data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex-skyslakova/strand-bias-analysis-tool",
    install_requires=[
        'Bio==1.4.0',
        'bokeh==2.4.3',
        'matplotlib==3.6.1',
        'numpy==1.22.3',
        'pandas==1.4.2',
        'python_dateutil==2.8.2',
        'pytz==2022.1',
        'setuptools==45.2.0',
        'tornado==6.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'sbat=sbat.main:main',
        ],
    }
)
