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

if __name__ == "__main__":
	unittest.main()
