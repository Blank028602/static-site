import os
import shutil
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

def copy(public, static):
	if os.path.exists(public):
		shutil.rmtree(public)
		os.mkdir(public)
	else:
		os.mkdir(public)
	list_items = os.listdir(static)
	for item in list_items:
		path = os.path.join(static, item)
		d_path = os.path.join(public, item)
		if os.path.isfile(path):
			print(f"Copying file: {path} to {d_path}")
			shutil.copy(path, public)
		else:
			print(f"Entering directory: {path}")
			path_p = os.path.join(public, item)
			path_s = os.path.join(static, item)
			copy(path_p, path_s)

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	content_from_path = from_path.read()
	content_temp_path = template_path.read()
	markdown = TextNode.markdown_to_html_node(content_from_path)
	html = markdown.to_html()
	title = TextNode.extract_title(content_from_path)
	output_html = content_temp_path.replace("{{ Title }}", title)
	output_html = output_html.replace("{{ Content }}", html)
	dir_path = os.path.dirname(dest_path)
	os.makedirs(dir_path, exist_ok = True)
	with open(dest_path, "w") as f:
		f.write(output_html)



def main():
	public = "public"
	static = "static"
	copy(public, static)
	print("Static content copied successfully!")
	with open("content/index.md") as from_file, open("template.html") as template_file:
		generate_page(from_file, template_file, "public/index.html")

main()

