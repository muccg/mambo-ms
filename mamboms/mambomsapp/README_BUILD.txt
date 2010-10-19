The MA search requires a python extension module to be compiled from C code
(for speed). The C code is generated from a pyx file by the Cython compiler.

To get this ready to deploy, follow these steps (ON THE TARGET MACHINE or a
clone):
1. From the mambomsapp directory, clean out all build artifacts, if any
(build, dist, egg directories, .c and .so files)
2. From the project root, run scons. This installs the application files to
the destination, and sets up the virtual python environment. The latter part
is what is important right now.
3. From the mambomsapp directory, we will now build the .so library using the
virtual python environment we just installed.

Something like:
<installed apps root>/.../mamboms/virtualpython/bin/python build_package.py
build_ext --inplace

This builds the library in place. From here, we can make an egg out of it.

UPDATE: the instructions below describe building the egg and it being
deployed in the virtualpython section of the deployment - this turns
out not to be sufficient for our needs since this code needs to access
mamboms code and has no way to import it from there. For now
(temporary solution) simply build the .so, check it into git inside the
mambomsapp directory, clean other build artifacts, and deploy. Ignore
the below instructions until further notice.


<installed apps root>/.../mamboms/virtualpython/bin/python setup.py bdist_egg

4. Copy the egg from dist/search_datastructures_blah.egg to
<projecthome>/eggs/

5. Clean out the crud (as in step 1) from the mambomsapp directory. This will
be the build and dist directory, a <packagename>.egg dirtectory, and the .so
and .c files.

6. Optionally, you can check the egg into subversion if you like.

7. From the project root, run scons again. The egg will be copied across and
installed. You may have to blow away the virtualpython section of the
installed app dir to force the virtual python to be recreated, and the eggs
installed.
