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


if __name__ == "__main__": unittest.main()
