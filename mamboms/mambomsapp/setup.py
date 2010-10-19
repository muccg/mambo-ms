#from distutils.core import setup
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
setup(
    name='search datastructures',
    author='brad power',
    version='0.1',
    description='support datastructures for MA search',
    author_email='bpower@ccg.murdoch.edu.au',
    #packages=['search_datastructures'],
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("search_datastructures", ["search_datastructures.pyx"])],
    )


