import pywordpress
import yaml
from aux import *

class Bot():
	def __init__(self,configfile,wp_config="wordpress.ini"):
		self.wp_config = wp_config
		self.wp = pywordpress.Wordpress.init_from_config(self.wp_config)
		self.config = yaml.safe_load(open(configfile))
		self.data = self.config['source-tree']
		self.ids = []

	def load_data(self):
		self.data = apply_to_tree(self.data, lambda x: get_content(x, self.config['root-dir']))

	def parse_data(self):
		self.data = apply_to_tree(self.data, parse_content)

	def build_pages(self,node):
		"""
		Takes a tree and creates a new WordPress page from its root.
		Propagates the ID of the new page to each child of the root.
		Then builds WP pages for *those* subtrees.
		"""
		if node.has_key("parent"):
			node['id'] = self.wp.new_page(title = node['title'],
										  wp_slug = node['slug'],
										  description = node['content'],
										  wp_page_parent_id = node['parent'])
		else:
			node['id'] = self.wp.new_page(title = node['title'],
										  wp_slug = node['slug'],
										  description = node['content'])
		if node['children']:
			for x in node['children']:
				x['parent'] = node['id']
				self.build_pages(x)
		self.ids.append(node['id'])

	def write_ids(self):
		f = open("kill.yaml", "w")
		f.write(yaml.dump(self.ids))
		f.close()

if __name__ == "__main__":
	b = Bot("post.yaml")
	b.load_data()
	b.parse_data()
	b.build_pages(b.data)
	b.write_ids()