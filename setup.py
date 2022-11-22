from setuptools import setup
from mypyc.build import mypycify


sources = ("__init__.py", "lib.py", "rule.py", "common.py")
ext_modules = mypycify([f"src/crossandra/{i}" for i in sources])

setup(
    name="crossandra",
    packages=["src/crossandra"],
    ext_modules=ext_modules,
)
