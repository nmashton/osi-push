import re
import urllib2
from copy import copy

def apply_to_tree(tree,f):
	"""
	Recursively apply a function f to a dictionary representing a tree.

	Dictionary must be in the form:
	{
		children: [...]
		...
	}
	"""
	newtree = f(copy(tree))
	if newtree['children']:
		newtree['children'] = [f(x) for x in newtree['children']]
	return newtree

def get_content(node,root=""):
	"""
	Takes a tree dictionary whose root has a 'url' attribute, returns
	a new tree whose root has an additional 'content' attribute containing
	the string read from the given URL.
	"""
	newnode = copy(node)
	newnode['content'] = urllib2.urlopen(root + newnode['url']).read()
	return newnode

def parse_content(node):
	"""
	Takes a tree dictionary and reconfigures its root in two ways:
	- extracts a new "title" attribute from its "content"
	- fixes "content" to omit metadata
	"""
	newnode = copy(node)
	newnode['title'] = re.search(r'(?<=---\ntitle: ).*(?=\n)', newnode['content']).group(0)
	newnode['content'] = re.sub(r'---\n.*\n---\n\n', r'', newnode['content'], flags=re.DOTALL)
	return newnode