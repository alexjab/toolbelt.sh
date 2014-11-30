#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import yaml

def get_spaces(number):
  return ''.join(['  ']*(number))

# builds the toolbelt
def build_toolbelt(blueprint):

  def print_toolbelt_function_top(blueprint):
    if 'name' in blueprint:
      print blueprint['name'] + ' () {'
      print '  local TOOLBELT_NAME='+ blueprint['name'] + ';'
    else:
      print 'toolbelt () {'
      print '  local TOOLBELT_NAME=toolbelt;'
    if 'version' in blueprint:
      print '  local TOOLBELT_VERSION=' + blueprint['version'] + ';'
    else:
      print '  local TOOLBELT_VERSION=0.0.1;'
  
  def print_help():
    spaces = get_spaces(1)
    if 'help' in blueprint:
      print spaces + 'if [ "$1" = "help" ]; then'
      for line in blueprint['help'].split('\n'):
        if line:
          print spaces + spaces + line
      print spaces + 'elif [ "$1" = "version" ]; then'
    else:
      print spaces + 'if [ "$1" = "version" ]; then'

    print spaces + spaces + 'echo "$TOOLBELT_NAME v$TOOLBELT_VERSION"'
    print spaces + 'else'

  def print_recursive_conditions(node, level):
    spaces = get_spaces(2 + level)
    # a node, we need to:
    # - print the ifs with the params
    # - recursively go to all sub-nodes
    if type(node) == dict:
      index = 0
      for param in node:
        if index == 0:
          print spaces + 'if [ "$'+str(level+1)+'" = "'+param+'" ]; then'
        else:
          print spaces + 'elif [ "$'+str(level+1)+'" = "'+param+'" ]; then'
        print_recursive_conditions(node[param], level+1)
        if index == len(node) - 1:
          print spaces + 'else'
          print spaces + '  $TOOLBELT_NAME help'
          print spaces + 'fi'
        index+=1
    # a leaf: we just have to print the script
    else:
      for line in node.split('\n'):
        if line:
          print spaces + line

  def print_toolbelt_function_bottom():
    print get_spaces(1) + 'fi'
    print '}'

  print_toolbelt_function_top(blueprint)
  print ''
  print_help()
  print_recursive_conditions(blueprint['commands'], 0)
  print_toolbelt_function_bottom()


# builds the autocomplete function
def build_autocomplete(blueprint):
  def print_if_zsh():
    print 'if [ $ZSH_VERSION ]; then'
    print '  autoload bashcompinit'
    print '  bashcompinit'
    print 'fi'

  if 'name' in blueprint:
    toolbelt_name = blueprint['name']
  else:
    toolbelt_name = 'blueprint'

  def print_ac_function_top():
    print '_' + toolbelt_name + ' () {'
    print '  local cur opts'
    print '  COMPREPLY=()'
    print '  cur="${COMP_WORDS[COMP_CWORD]}"'
    print '  prev="${COMP_WORDS[COMP_CWORD-1]}"'

  def print_ac_commands():
    autocomplete_list = []
    def flatten_command_tree(node, parent, level):
      if type(node) == dict:
        if len(autocomplete_list) == level:
          autocomplete_list.append([(parent, ' '.join([param for param in node]))])
        else:
          autocomplete_list[level].append((parent, ' '.join([param for param in node])))
        for param in node:
          flatten_command_tree(node[param], param, level+1)

    flatten_command_tree(blueprint['commands'], None, 0)

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
        helpers = ''
        if 'help' in blueprint:
          helpers += ' help'
        if index == 0 and 'version' in blueprint:
          helpers += ' version'
        print '      opts="' + position_item[1] + helpers + '"'
        print '      COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )'
        print '      return 0'
        if position_item[0] and position_index == len(item)-1:
          print '    fi'
      if index == len(autocomplete_list)-1:
        print '  fi'

  def print_ac_function_bottom():
    print '}'
    print ''
    print 'complete -F _' + toolbelt_name + ' ' + toolbelt_name

  print ''
  print_if_zsh()
  print ''
  print_ac_function_top()
  print ''
  print_ac_commands()
  print_ac_function_bottom()

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

