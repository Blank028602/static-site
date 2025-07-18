import os
import shutil
import sys
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

def generate_page(from_path, template_path, dest_path, basepath):
	with open(from_path) as md_1:
		content_from_path = md_1.read()
	with open(template_path) as md_2:
		content_temp_path = md_2.read()
	markdown = TextNode.markdown_to_html_node(content_from_path)
	html = markdown.to_html()
	title = TextNode.extract_title(content_from_path)
	output_html = content_temp_path.replace("{{ Title }}", title)
	output_html = output_html.replace("{{ Content }}", html)
	output_html = output_html.replace('href="/', f'href="{basepath}')
	output_html = output_html.replace('src="/', f'src="{basepath}')
	dir_path = os.path.dirname(dest_path)
	os.makedirs(dir_path, exist_ok = True)
	with open(dest_path, "w") as f:
		f.write(output_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
	list_items = os.listdir(dir_path_content)
	for item in list_items:
		path = os.path.join(dir_path_content, item)
		if os.path.isfile(path) and item.endswith(".md"):
			root, ext = os.path.splitext(item)
			full_name = root + ".html"
			full_html_path = os.path.join(dest_dir_path, full_name)
			generate_page(path, template_path, full_html_path, basepath)
		elif os.path.isfile(path):
			continue
		else:
			dest_path = os.path.join(dest_dir_path, item)
			generate_pages_recursive(path, template_path, dest_path, basepath)

def convert_to_html(directory):
	list_items = os.listdir(directory)
	for item in list_items:
		path = os.path.join(directory, item)
		if path == "content/index.md":
			continue
		elif os.path.isfile(path) and item.endswith(".md"):
			with open(path) as md:
				md_content = md.read()
				html_node = TextNode.markdown_to_html_node(md_content)
				html = html_node.to_html()
			relative_path = os.path.relpath(path, "content")
			html_path = os.path.join("public", relative_path)
			root, ext = os.path.splitext(html_path)
			final_html_path = root + ".html"
			output_dir = os.path.dirname(final_html_path)
			os.makedirs(output_dir, exist_ok = True)
			with open(final_html_path, "w") as f:
				f.write(html)
		elif os.path.isfile(path):
			continue
		else:
			convert_to_html(path)

def main():
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	else:
		basepath = "/"
	public = "docs"
	static = "static"
	content = "content"
	copy(public, static)
	generate_pages_recursive(content, "template.html", public, basepath)

main()

