import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from block import BlockType, block_to_block_type

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

	@staticmethod
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

	@staticmethod
	def split_nodes_delimiter(old_nodes, delimiter, text_type):
		new_nodes = []
		for old_node in old_nodes:
			if old_node.text_type != TextType.TEXT_PLAIN:
				new_nodes.append(old_node)
				continue
			parts = old_node.text.split(delimiter, 1)
			if len(parts) < 2:
				new_nodes.append(old_node)
				continue
			closing_delim_index = parts[1].find(delimiter)
			if closing_delim_index == -1:
				raise Exception("Invalid Markdown syntax: Unclosed delimiter")
			text_between_delims = parts[1][:closing_delim_index]
			text_after_second_delim = parts[1][closing_delim_index + len(delimiter):]
			if parts[0] != "":
				new_nodes.append(TextNode(parts[0], TextType.TEXT_PLAIN))
			new_nodes.append(TextNode(text_between_delims, text_type))
			remaining_nodes = TextNode.split_nodes_delimiter([TextNode(text_after_second_delim, TextType.TEXT_PLAIN)], delimiter, text_type)
			new_nodes.extend(remaining_nodes)
		return new_nodes

	@staticmethod
	def extract_markdown_images(text):
		match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
		return match

	@staticmethod
	def extract_markdown_links(text):
		match = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
		return match

	@staticmethod
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

	@staticmethod
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

	@staticmethod
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

	@staticmethod
	def markdown_to_blocks(markdown):
		markdown = markdown.strip()
		list = markdown.split("\n\n")
		final_list = []
		for block in list:
			new_block = block.strip()
			if new_block == "":
				continue
			final_list.append(new_block)
		return final_list

	@staticmethod
	def text_to_children(text):
		text_nodes = TextNode.text_to_textnodes(text)
		html_nodes = []
		for text_node in text_nodes:
			html_node = TextNode.text_node_to_html_node(text_node)
			html_nodes.append(html_node)
		return html_nodes

	@staticmethod
	def markdown_to_html_node(markdown):
		mblocks = TextNode.markdown_to_blocks(markdown)
		block_nodes = []
		for mblock in mblocks:
			mblock_type = block_to_block_type(mblock)
			if mblock_type == BlockType.PARAGRAPH:
				node = ParentNode("p", None)
				paragraph_text = mblock.replace("\n", " ")
				children = TextNode.text_to_children(paragraph_text)
				node = ParentNode("p", children)
				block_nodes.append(node)
			elif mblock_type == BlockType.HEADING:
				heading_level = 0
				for char in mblock:
					if char == "#":
						heading_level += 1
					else:
						break
				tag = f"h{heading_level}"
				node = ParentNode(tag, None)
				heading_text = mblock[heading_level:].strip()
				children = TextNode.text_to_children(heading_text)
				node = ParentNode(tag, children)
				block_nodes.append(node)
			elif mblock_type == BlockType.CODE:
				lines = mblock.split("\n")
				code_lines = lines[1:-1]
				code_content = "\n".join(code_lines) + "\n"
				text_node = TextNode(code_content, TextType.TEXT_PLAIN)
				code_child = TextNode.text_node_to_html_node(text_node)
				code_node = ParentNode("code", [code_child])
				node = ParentNode("pre", [code_node])
				block_nodes.append(node)
			elif mblock_type == BlockType.QUOTE:
				node = ParentNode("blockquote", None)
				quote_text = mblock[1:].strip()
				children = TextNode.text_to_children(quote_text)
				node = ParentNode("blockquote", children)
				block_nodes.append(node)
			elif mblock_type == BlockType.UNORDERED_LIST:
				child_list = []
				items = mblock.split("\n")
				for item in items:
					parts = item.split(" ", 1)
					if len(parts) > 1:
						item_text = parts[1]
					else:
						item_text = ""
					children = TextNode.text_to_children(item_text)
					child_node = ParentNode("li", children)
					child_list.append(child_node)
				node = ParentNode("ul", child_list)
				block_nodes.append(node)
			elif mblock_type == BlockType.ORDERED_LIST:
				child_list = []
				items = mblock.split("\n")
				for item in items:
					parts = item.split(" ", 1)
					if len(parts) > 1:
						item_text = parts[1]
					else:
						item_text = ""
					children = TextNode.text_to_children(item_text)
					child_node = ParentNode("li", children)
					child_list.append(child_node)
				node = ParentNode("ol", child_list)
				block_nodes.append(node)
		parent_node = ParentNode("div", block_nodes)
		return parent_node

	@staticmethod
	def extract_title(markdown):
		lines = markdown.split("\n")
		for line in lines:
			line = line.strip()
			if line.startswith("# "):
				line = line[2:]
				line = line.strip()
				return line
		raise Exception("no h1 header")































