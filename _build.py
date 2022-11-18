from mypyc.build import mypycify

sources = ("__init__.py", "lib.py", "rule.py", "common.py")
ext_modules = mypycify([f"src/crossandra/{i}" for i in sources])


def build(setup_kwargs):
    setup_kwargs["ext_modules"] = ext_modules
    setup_kwargs["packages"] = ["crossandra"]