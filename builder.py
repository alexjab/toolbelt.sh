import sys

import yaml

if len(sys.argv) > 1:
  filename = sys.argv[1]
  default_file = False
else:
  filename = 'blueprint.yml'
  default_file = True

try:
  f = open(filename, 'r')
  yfile = f.read()
  f.close()
except IOError as e:
  if not default_file:
    print 'Error: file not found:', filename
  else:
    print 'Error: no blueprint file specified/found !'
else:
  blueprint = yaml.load(yfile)

  toolbelt_name = blueprint['name']
  print 'TOOLBELT_NAME=' + toolbelt_name + ';'
  toolbelt_version = blueprint['version']
  print 'TOOLBELT_VERSION=' + toolbelt_version + ';'

  def build_cli(node, level):
    spaces = ''.join(['  ']*(level+1))
    if type(node) == dict:
      index = 0
      for param in node:
        if index < 1:
          print spaces + 'if [ "$'+str(level)+'"  = "'+param+'" ]; then'
        else:
          print spaces + 'elif [ "$'+str(level)+'" = "'+param+'" ]; then'
        build_cli(node[param], level+1)
        if index == len(node) - 1:
          print spaces + 'else'
          print spaces + '  ' + toolbelt_name + ' help'
          print spaces + 'fi'
        index+=1
    else:
      for line in node.split('\n'):
        if line:
          print spaces + line


  print toolbelt_name + ' () {'

  print '  ' + 'if [ "$1"  = "help" ]; then'

  for line in blueprint['help'].split('\n'):
    if line:
      print '    ' + line

  print '  ' + 'else'

  build_cli(blueprint['commands'], 1)

  print '  ' + 'fi'

  print '}'

