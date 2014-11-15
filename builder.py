import yaml

f = open('blueprint.yml', 'r')

doc = yaml.load(f)

print doc

toolbelt_name = doc['name']

def search(tree, name):
  if type(tree) == dict:
    for command in tree:
      search(tree[command], name+' '+command)
  else:
    print name, tree

search(doc['commands'], toolbelt_name)

print toolbelt_name, '() {'

print '}'
