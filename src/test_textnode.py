import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.TEXT_BOLD)
		node2 = TextNode("This is a text node", TextType.TEXT_BOLD)
		self.assertEqual(node, node2)

	def test_not_eq_text(self):
		node = TextNode("Hello", TextType.TEXT_PLAIN)
		node2 = TextNode("Hello2", TextType.TEXT_PLAIN)
		self.assertNotEqual(node, node2)

	def test_eq_link(self):
		node = TextNode("Hello", TextType.TEXT_BOLD, "link")
		node2 = TextNode("Hello", TextType.TEXT_BOLD, "link")
		self.assertEqual(node, node2)

	def test_not_eq_link(self):
		node = TextNode("Hello", TextType.TEXT_ITALIC, "link")
		node2 = TextNode("Hello", TextType.TEXT_ITALIC, "link2")
		self.assertNotEqual(node, node2)

	def test_not_eq_texttype(self):
		node = TextNode("Hello", TextType.TEXT_ITALIC)
		node2 = TextNode("Hello", TextType.TEXT_PLAIN)
		self.assertNotEqual(node, node2)

	def test_not_eq(self):
		node = TextNode("Hello", TextType.TEXT_ITALIC, "link")
		node2 = TextNode("Hello2", TextType.TEXT_BOLD)
		self.assertNotEqual(node, node2)

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT_PLAIN)
		html_node = TextNode.text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_text_bold(self):
		node = TextNode("This is bold text", TextType.TEXT_BOLD)
		html_node = TextNode.text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is bold text")

	def test_text_italic(self):
		node = TextNode("This is italic text", TextType.TEXT_ITALIC)
		html_node = TextNode.text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is italic text")

	def test_text_code(self):
		node = TextNode("This is code", TextType.TEXT_CODE)
		html_node = TextNode.text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is code")

	def test_text_link(self):
		node = TextNode("This is a link", TextType.LINK, "the link")
		html_node = TextNode.text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a link")
		self.assertEqual(html_node.props, {"href": "the link"})

	def test_text_image(self):
		node = TextNode("text for image", TextType.IMAGES, "this is the url")
		html_node = TextNode.text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props, {"src": "this is the url", "alt": "text for image"})

	def test_error(self):
		with self.assertRaises(Exception) as context:
			invalid_node = TextNode("test", None)
			TextNode.text_node_to_html_node(invalid_node)
		self.assertEqual(str(context.exception), "isnt part of TextType")

	def test_text_delimiter_code(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_delimiter([node], "`", TextType.TEXT_CODE)
		self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT_PLAIN), TextNode("code block", TextType.TEXT_CODE), TextNode(" word", TextType.TEXT_PLAIN)])

	def test_text_delimiter_bold(self):
		node = TextNode("This is text with a **bold** word", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_delimiter([node], "**", TextType.TEXT_BOLD)
		self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT_PLAIN), TextNode("bold", TextType.TEXT_BOLD), TextNode(" word", TextType.TEXT_PLAIN)])

	def test_text_delimiter_italic(self):
		node = TextNode("This is text with a _italic_ word", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_delimiter([node], "_", TextType.TEXT_ITALIC)
		self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT_PLAIN), TextNode("italic", TextType.TEXT_ITALIC), TextNode(" word", TextType.TEXT_PLAIN)])

	def test_extract_markdown_images(self):
		matches = TextNode.extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_links(self):
		matches = TextNode.extract_markdown_links("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
		self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_images_links(self):
		matches_images = TextNode.extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
		matches_links = TextNode.extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches_images)
		self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches_links)

	def test_split_images(self):
		node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_image([node])
		self.assertListEqual([TextNode("This is text with an ", TextType.TEXT_PLAIN), TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.TEXT_PLAIN),
		TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png")], new_nodes)

	def test_split_links(self):
		node = TextNode("This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_link([node])
		self.assertListEqual([TextNode("This is text with an ", TextType.TEXT_PLAIN), TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.TEXT_PLAIN),
		TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")], new_nodes)

	def test_split_images_no_text(self):
		node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_image([node])
		self.assertListEqual([TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"), TextNode("second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png")], new_nodes)

	def test_split_links_no_text(self):
		node = TextNode("[link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_link([node])
		self.assertListEqual([TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"), TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")], new_nodes)

	def test_split_images_only_text(self):
		node = TextNode("This node only contains text.", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_image([node])
		self.assertListEqual([TextNode("This node only contains text.", TextType.TEXT_PLAIN)], new_nodes)

	def test_split_links_only_text(self):
		node = TextNode("This node only contains text.", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_link([node])
		self.assertListEqual([TextNode("This node only contains text.", TextType.TEXT_PLAIN)], new_nodes)

	def test_split_images_nothing(self):
		node = TextNode("", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_image([node])
		self.assertListEqual([TextNode("", TextType.TEXT_PLAIN)], new_nodes)

	def test_split_links_nothing(self):
		node = TextNode("", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_link([node])
		self.assertListEqual([TextNode("", TextType.TEXT_PLAIN)], new_nodes)

	def test_split_images_one(self):
		node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_image([node])
		self.assertListEqual([TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)

	def test_split_links_one(self):
		node = TextNode("[link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT_PLAIN)
		new_nodes = TextNode.split_nodes_link([node])
		self.assertListEqual([TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)

	def test_text_to_textnodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		nodes = TextNode.text_to_textnodes(text)
		self.assertListEqual([
			TextNode("This is ", TextType.TEXT_PLAIN),
			TextNode("text", TextType.TEXT_BOLD),
			TextNode(" with an ", TextType.TEXT_PLAIN),
			TextNode("italic", TextType.TEXT_ITALIC),
			TextNode(" word and a ", TextType.TEXT_PLAIN),
			TextNode("code block", TextType.TEXT_CODE),
			TextNode(" and an ", TextType.TEXT_PLAIN),
			TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.TEXT_PLAIN),
			TextNode("link", TextType.LINK, "https://boot.dev")], nodes)

	def test_markdown_to_block(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

		blocks = TextNode.markdown_to_blocks(md)
		self.assertEqual(blocks,["This is **bolded** paragraph", "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", "- This is a list\n- with items"])

	def test_markdown_to_block_empty(self):
		md = ""
		blocks = TextNode.markdown_to_blocks(md)
		self.assertEqual(blocks, [])

	def test_markdown_to_block_many_blank_lines(self):
		md = """






"""
		blocks = TextNode.markdown_to_blocks(md)
		self.assertEqual(blocks, [])

	def test_markdown_to_block_only_whitespace(self):
		md = """
                                                               
"""
		blocks = TextNode.markdown_to_blocks(md)
		self.assertEqual(blocks, [])

	def test_markdown_to_block_single_block(self):
		md = """
# This is a heading
"""
		blocks = TextNode.markdown_to_blocks(md)
		self.assertEqual(blocks, ["# This is a heading"])













if __name__ == "__main__": unittest.main()
































