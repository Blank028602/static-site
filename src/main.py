import os
import shutil
from textnode import TextNode, TextType

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




def main():
	public = "public"
	static = "static"
	copy(public, static)
	print("Static content copied successfully!")
main()

