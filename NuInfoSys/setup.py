from distutils.core import setup
setup(name="NuInfoSys",
      version="1.0",
      description="NuInfoSys",
      author="Adam Brewer",
      author_email="adamhb321@gmail.com",
      packages=["NuInfoSys"],
      package_dir={"NuInfoSys": "."},
      py_modules=["betabrite", "framecontrolbytes", "memory"],
     )