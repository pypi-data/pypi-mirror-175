from setuptools import setup, find_packages

setup(
    name="kandinsky",
    version="2.1.dev1",
    author="ZetaMap",
    description="A small module allowing to link the kandinsky module, from the Numworks, to a window.",
    license='MIT',
    long_description=open("README.md", "rt", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ZetaMap/Kandinsky-Numworks",
    project_urls={
        "GitHub Project": "https://github.com/ZetaMap/Kandinsky-Numworks",
        "My GitHub Page": "https://github.com/ZetaMap/"
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
    ],
    package_dir={"": "src"},
    include_dirs=find_packages(where="src", include=".*"),
    install_requires=["pysdl2", "pysdl2-dll"],
    include_package_data=True
)
