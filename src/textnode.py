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
				raise Exception("the given delimiter is not in the text")
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
