import re
from enum import Enum
from htmlnode import LeafNode, ParentNode

class TextType(Enum):
	TEXT_PLAIN = "plain text"
	TEXT_ITALIC = "italic text"
	TEXT_BOLD = "bold text"
	TEXT_CODE = "code text"
	LINK = "link"
	IMAGES = "image"

class TextNode:
	def __init__(self, text, text_type, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		if not isinstance(other, TextNode):
			return False
		if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
			return True
		return False

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

	def text_node_to_html_node(text_node):
		if text_node.text_type == TextType.TEXT_PLAIN:
			return LeafNode(None, text_node.text)
		elif text_node.text_type == TextType.TEXT_BOLD:
			return LeafNode("b", text_node.text)
		elif text_node.text_type == TextType.TEXT_ITALIC:
			return LeafNode("i", text_node.text)
		elif text_node.text_type == TextType.TEXT_CODE:
			return LeafNode("code", text_node.text)
		elif text_node.text_type == TextType.LINK:
			props_dict = {"href": text_node.url}
			return LeafNode("a", text_node.text, props_dict)
		elif text_node.text_type == TextType.IMAGES:
			props_dict = {"src": text_node.url, "alt": text_node.text}
			return LeafNode("img", "", props_dict)
		else:
			raise Exception("isnt part of TextType")

	def split_nodes_delimiter(old_nodes, delimiter, text_type):
		text_nodes = []
		for old_node in old_nodes:
			char_to_find = delimiter
			if old_node.text_type != TextType.TEXT_PLAIN:
				text_nodes.append(old_node)
				continue
			if char_to_find not in old_node.text:
				return [old_node]
			node_list = old_node.text.split(delimiter)
			if len(node_list) < 3 or len(node_list) > 3:
				raise Exception("thats invalid Markdown syntax")
			node_1 = TextNode(node_list[0], old_node.text_type)
			text_nodes.append(node_1)
			node_2 = TextNode(node_list[1], text_type)
			text_nodes.append(node_2)
			node_3 = TextNode(node_list[2], old_node.text_type)
			text_nodes.append(node_3)
		return text_nodes

	def extract_markdown_images(text):
		match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
		return match

	def extract_markdown_links(text):
		match = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
		return match

	def split_nodes_image(old_nodes):
		text_nodes = []
		for old_node in old_nodes:
			text = old_node.text
			images = TextNode.extract_markdown_images(text)
			if images == []:
				text_nodes.append(old_node)
				continue
			first_image = images[0]
			image_alt = first_image[0]
			image_url = first_image[1]
			full_image_markdown = f"![{image_alt}]({image_url})"
			parts = text.split(full_image_markdown, 1)
			if parts[0] != "":
				node_1 = TextNode(parts[0], TextType.TEXT_PLAIN)
				text_nodes.append(node_1)
			node_2 = TextNode(image_alt, TextType.IMAGES, image_url)
			text_nodes.append(node_2)
			if parts[1] != "":
				node_3 = TextNode(parts[1], TextType.TEXT_PLAIN)
				remaining_nodes = TextNode.split_nodes_image([node_3])
				text_nodes.extend(remaining_nodes)
		return text_nodes

	def split_nodes_link(old_nodes):
		text_nodes = []
		for old_node in old_nodes:
			text = old_node.text
			links = TextNode.extract_markdown_links(text)
			if links == []:
				text_nodes.append(old_node)
				continue
			first_link = links[0]
			link_alt = first_link[0]
			link_url = first_link[1]
			full_link_markdown = f"[{link_alt}]({link_url})"
			parts = text.split(full_link_markdown, 1)
			if parts[0] != "":
				node_1 = TextNode(parts[0], TextType.TEXT_PLAIN)
				text_nodes.append(node_1)
			node_2 = TextNode(link_alt, TextType.LINK, link_url)
			text_nodes.append(node_2)
			if parts[1] != "":
				node_3 = TextNode(parts[1], TextType.TEXT_PLAIN)
				remaining_nodes = TextNode.split_nodes_link([node_3])
				text_nodes.extend(remaining_nodes)
		return text_nodes

	def text_to_textnodes(text):
		nodes = [TextNode(text, TextType.TEXT_PLAIN)]
		splitters = [
			(TextNode.split_nodes_image, []),
			(TextNode.split_nodes_link, []),
			(TextNode.split_nodes_delimiter, ["**", TextType.TEXT_BOLD]),
			(TextNode.split_nodes_delimiter, ["_", TextType.TEXT_ITALIC]),
			(TextNode.split_nodes_delimiter, ["`", TextType.TEXT_CODE])]
		for splitter, args in splitters:
			new_nodes = []
			for node in nodes:
				if node.text_type == TextType.TEXT_PLAIN:
					new_nodes.extend(splitter([node], *args) if args else splitter ([node]))
				else:
					new_nodes.append(node)
			nodes = new_nodes
		return [node for node in nodes if node.text != ""]

































