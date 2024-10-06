from setuptools import Extension , setup
from Cython.Build import cythonize
from pathlib import Path
import numpy as np
import os

SOURCE_DIR=Path("artifact")
BUILD_DIR=Path("build")

CYTHON_COMPILER_DIRECTIVES = {
    "language_level": 3,
    "cdivision": True,  # If division is as per C with no check for zero (35% speed up)
    "embedsignature": True,  # If docstrings should be embedded into C signatures
    "warn.maybe_uninitialized": True
}


def get_extensions():

    ext_list=[]
    define_macros = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]

    for file in SOURCE_DIR.rglob("*.py*"):


        module_name=str(file.with_suffix("")).replace("/",".")

        extension=Extension(
            name=module_name,
            sources=[str(file)],
            include_dirs=[np.get_include()],
            define_macros=define_macros,


        )

        ext_list.append(extension)



    return ext_list


if __name__=="__main__":
    
    extensions = get_extensions()
    
    setup(
        name='artifact-dev',
        ext_modules=cythonize(
            module_list=extensions,
            build_dir=BUILD_DIR,
            compiler_directives=CYTHON_COMPILER_DIRECTIVES,
            annotate=True,
            nthreads=os.cpu_count() or 1,    
        ),
    )
    






