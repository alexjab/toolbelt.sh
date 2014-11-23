toolbelt.sh
================

A bash toolbelt generator written in Python.

##TL;DR
```
git clone https://github.com/alexjab/toolbelt.sh.git
cd toolbelt.sh
pip install -r requirements.txt

# ...

python builder.py # to test if everything works
python builder.py > toolbelt.sh # to create your toolbelt

# ...

echo 'source ~/<folder>/toolbelt.sh/toolbelt.sh' >> .profile # add your toolbelt to your environment

# ...

toolbelt foo bar # use your toolbelt
```

##About toolbelt.sh
`toolbelt.sh` is a python script aimed at creating bash toolbelts. A bash toolbelt brings together a set of scripts (usually your scripts) and make them accessible from a common command line function.

Example:

```
toolbelt api start
toolbelt production logs
toolbelt docker clean
toolbelt docker forward 27017
...
```

To write a toolbelt, you write a blueprint file (in YAML) that hierarchically orders your functions, pass it to the builder that will generate a complete .sh file; you then need to `source` it to access your functions.

It was heavily inspired by [nvm](https://github.com/creationix/nvm).

##Installation
You need Python and PyYaml; Python is usually pre-installed on *NIX systems.

```
cd toolbelt.sh/
pip install -r requirements.txt
```

Requirements: Python 2.7 and PyYaml.

##Usage
`builder.py` is in charge of building the toolbelt; you need to pass it a yaml file as argument and redirect the output to a file (default is to stdout);

Example:

```
python builder.py blueprint.yml > toolbelt.sh
```

If you don't specify a file, `builder.py` will look for `blueprint.yml`.

##Structure of the YAML file

The YAML file is your blueprint: your toolbelt will be built according to what's put in there; here is its basic structure:

```
~$ cat blueprint.yml

name: mytoolbelt
version: 0.0.1
help: |
  echo "Usage:"
  echo "mytoolbelt foo start"
  echo "mytoolbelt bar start"
commands:
  foo:
	start: |
		echo 'starting foo...'
		sleep 2
		echo 'foo started'
  bar:
  	start: |
  		echo 'starting bar...'
  		sleep 2
  		echo 'foo started'

```
###Parameters:

 - `name`: your toolbelt's name; it can be anything, `toolbelt` is fine, but you might wanna customize it or build several different ones; you can access this value anywhere in your shell commands using `$TOOLBELT_NAME`;


 - `version`: your toolbelt's version number; it can be anything; you can use this value anywhere in your commands using `$TOOLBELT_VERSION`;


 - `help`: the help commands to be executed; the value of this field is executed when you call the `help` function when you use the toolbelt (ex. `mytoolbelt help`);


 - `commands`: the commands of the toolbelt; these are customs commands that will be offered by your toolbelt; they must be hierachically ordered so that your combination of commands appears clearly; you can nest as many functions as you want but you should keep in mind that:
 	- the last level of indentation of every shell command must be a shell command or a list of command,
 	- using too deep indentations yields a more complicated toolbelt and you don't want to confuse your users.


If a toolbelt command needs a script (i.e. a shell command that takes several lines), you need to put a pipe (`|`) right after the toolbelt command name (see the `start` or `help` command in the example) to tell the YAML interpreter that it is a multiline script.

###License
MIT