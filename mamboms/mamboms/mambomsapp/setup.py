from distutils.core import setup
#from setuptools import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    print "Could not find Cython.Distutils"
    use_cython=False
else:
    use_cython=True

cmdclass = {}
ext_modules = []

if use_cython:
    ext_modules += [
        Extension("search_datastructures", ["search_datastructures.pyx"]),
    ]
    cmdclass.update({'build_ext':build_ext})
else:
    ext_modules += [
        Extension("search_datastructures", ["search_datastructures.c"]),
        ]

setup(
    name='search_datastructures',
    author='brad power',
    version='0.1',
    description='support datastructures for MA search',
    author_email='bpower@ccg.murdoch.edu.au',
    #packages=['search_datastructures'],
    cmdclass = cmdclass, 
    ext_modules = ext_modules,
)


