
P:\Python\Lib\site-packages\Pyjamas-0.5>python setup.py install
running install
running bdist_egg
running egg_info
writing Pyjamas.egg-info\PKG-INFO
writing top-level names to Pyjamas.egg-info\top_level.txt
writing dependency_links to Pyjamas.egg-info\dependency_links.txt
writing entry points to Pyjamas.egg-info\entry_points.txt
reading manifest file 'Pyjamas.egg-info\SOURCES.txt'
writing manifest file 'Pyjamas.egg-info\SOURCES.txt'
installing library code to build\bdist.win32\egg
running install_lib
running build_py
creating build
creating build\lib
creating build\lib\pyjs
copying pyjs\build.py -> build\lib\pyjs
copying pyjs\pyjs.py -> build\lib\pyjs
copying pyjs\__init__.py -> build\lib\pyjs
creating build\bdist.win32
creating build\bdist.win32\egg
creating build\bdist.win32\egg\pyjs
copying build\lib\pyjs\build.py -> build\bdist.win32\egg\pyjs
copying build\lib\pyjs\pyjs.py -> build\bdist.win32\egg\pyjs
copying build\lib\pyjs\__init__.py -> build\bdist.win32\egg\pyjs
byte-compiling build\bdist.win32\egg\pyjs\build.py to build.pyc
byte-compiling build\bdist.win32\egg\pyjs\pyjs.py to pyjs.pyc
byte-compiling build\bdist.win32\egg\pyjs\__init__.py to __init__.pyc
installing package data to build\bdist.win32\egg
running install_data
Traceback (most recent call last):
  File "setup.py", line 97, in <module>
    "Programming Language :: Python"
  File "P:\Python\lib\distutils\core.py", line 151, in setup
    dist.run_commands()
  File "P:\Python\lib\distutils\dist.py", line 974, in run_commands
    self.run_command(cmd)
  File "P:\Python\lib\distutils\dist.py", line 994, in run_command
    cmd_obj.run()
  File "P:\Python\Lib\site-packages\setuptools\command\install.py", line 76, in
run
    self.do_egg_install()
  File "P:\Python\Lib\site-packages\setuptools\command\install.py", line 96, in
do_egg_install
    self.run_command('bdist_egg')
  File "P:\Python\lib\distutils\cmd.py", line 333, in run_command
    self.distribution.run_command(command)
  File "P:\Python\lib\distutils\dist.py", line 994, in run_command
    cmd_obj.run()
  File "P:\Python\lib\site-packages\setuptools\command\bdist_egg.py", line 195,
in run
    self.do_install_data()
  File "P:\Python\lib\site-packages\setuptools\command\bdist_egg.py", line 145,
in do_install_data
    self.call_command('install_data', force=0, root=None)
  File "P:\Python\lib\site-packages\setuptools\command\bdist_egg.py", line 161,
in call_command
    self.run_command(cmdname)
  File "P:\Python\lib\distutils\cmd.py", line 333, in run_command
    self.distribution.run_command(command)
  File "P:\Python\lib\distutils\dist.py", line 994, in run_command
    cmd_obj.run()
  File "P:\Python\lib\distutils\command\install_data.py", line 62, in run
    dir = convert_path(f[0])
  File "P:\Python\lib\distutils\util.py", line 138, in convert_path
    raise ValueError, "path '%s' cannot be absolute" % pathname
ValueError: path '/usr/share/pyjamas/library' cannot be absolute

P:\Python\Lib\site-packages\Pyjamas-0.5>