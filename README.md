# autotest
Automatically detect changes within target directories and run a shell command when changes are detected. Defaults are setup for testing a python project with pytest, but this could be configured to run any command and work with any filetypes.

# usage
 
 To use with the default pytest configuration:
 First cd into the root where the tests should be executed from, then run:
 
 ```sh
 python tdd.py tests proj
 ```
 
 In this minimal example "tests" and "proj" are the directories we are going to watch for changes. These names should be relative to the CWD. 
 The default command to be run is "pytest -x -q --no-header". This can be cutomized:
 
 ```sh
 python tdd.py tests proj --cmd="literally any shell command"
 ```
 
 Finally, this will only watch certain filetypes. By default this is just [".py"]. This, too can be customized:
 
 ```sh
 python tdd.py tests proj --ft .py .c .xml
 ```
 
 I like to alias this for ease of use:
 
 ```sh
 alias gamelib-tdd="cd ~/dev/gamelib && . venv/bin/activate && python tdd.py tests gamelib"
 ```
 
 I haven't tested this against windows environments or old versions of python, but it aught to be quite portable as is. 
