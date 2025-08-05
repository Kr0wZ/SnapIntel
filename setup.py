from setuptools import setup

setup(
    name="SnapIntel",
    description="Investigate Snapchat users with SnapIntel",
    author="Kr0wZ",
    license="AGPL-3.0",
    py_modules=["main", "display", "snap_parser", "heatmap", "ssd"],
    install_requires=[
        "datetime",
        "pandas",
        "seaborn",
        "argparse",
        "colorama",
        "requests",
        "matplotlib",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "snapintel = main:main",  # This tells setuptools to create a command 'snapintel'
        ],
    },
)