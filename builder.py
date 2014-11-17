import sys

import yaml

# builds the toolbelt
def build_toolbelt(blueprint):

  toolbelt_name = blueprint['name']
  toolbelt_version = blueprint['version']

  print toolbelt_name + ' () {'
  print '  local TOOLBELT_NAME=' + toolbelt_name + ';'
  print '  local TOOLBELT_VERSION=' + toolbelt_version + ';'
  print '  ' + 'if [ "$1"  = "help" ]; then'

  for line in blueprint['help'].split('\n'):
    if line:
      print '    ' + line
  print '  ' + 'else'

  def search(node, level):
    spaces = ''.join(['  ']*(level+1))
    if type(node) == dict:
      index = 0
      for param in node:
        if index < 1:
          print spaces + 'if [ "$'+str(level+1)+'" = "'+param+'" ]; then'
        else:
          print spaces + 'elif [ "$'+str(level+1)+'" = "'+param+'" ]; then'
        search(node[param], level+1)
        if index == len(node) - 1:
          print spaces + 'else'
          print spaces + '  ' + toolbelt_name + ' help'
          print spaces + 'fi'
        index+=1
    else:
      for line in node.split('\n'):
        if line:
          print spaces + line

  search(blueprint['commands'], 0)

  print '  ' + 'fi'

  print '}'

# builds the autocomplete function
def build_autocomplete(blueprint):
  toolbelt_name = blueprint['name']
  toolbelt_version = blueprint['version']

  print ''
  print '_' + toolbelt_name + ' () {'
  print '  local cur opts'
  print '  COMPREPLY=()'
  print '  cur="${COMP_WORDS[COMP_CWORD]}"'
  print '  prev="${COMP_WORDS[COMP_CWORD-1]}"'
  print ''
  autocomplete_list = []
  def search(node, parent, level):
    if type(node) == dict:
      if len(autocomplete_list) == level:
        autocomplete_list.append([(parent, ' '.join([param for param in node]))])
      else:
        autocomplete_list[level].append((parent, ' '.join([param for param in node])))
      for param in node:
        search(node[param], param, level+1)

  search(blueprint['commands'], None, 0)

  for index, item in enumerate(autocomplete_list):
    if index == 0:
      print '  if [ $COMP_CWORD = '+str(index+1)+' ] ; then'
    else:
      print '  elif [ $COMP_CWORD = '+str(index+1)+' ] ; then'
    for position_index, position_item in enumerate(item):
      if position_item[0]:
        if position_index == 0:
          print '    if [ $prev = "'+position_item[0]+'" ] ; then'
        else:
          print '    elif [ $prev = "'+position_item[0]+'" ] ; then'
      print '      opts="'+position_item[1]+' help"'
      print '      COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )'
      print '      return 0'
      if position_item[0] and position_index == len(item)-1:
        print '    fi'
    if index == len(autocomplete_list)-1:
      print '  fi'

  print '}'
  print ''
  print 'complete -F _' + toolbelt_name + ' ' + toolbelt_name

if __name__ == "__main__":
  # get the blueprint and start building the bash script
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

    build_toolbelt(blueprint)

    build_autocomplete(blueprint)

