import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_props_to_html(self):
		node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
		result = node.props_to_html()
		expected =' href="https://www.google.com" target="_blank"'
		self.assertEqual(result, expected)

	def test_props_to_html_none(self):
		node = HTMLNode()
		result = node.props_to_html()
		expected = ""
		self.assertEqual(result, expected)

	def test_props_to_html_single(self):
		node = HTMLNode(props={"class": "container"})
		result = node.props_to_html()
		expected = ' class="container"'
		self.assertEqual(result, expected)


	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		result = node.to_html()
		self.assertEqual(result, "<p>Hello, world!</p>")

	def test_laef_to_html_props(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		result = node.to_html()
		expected = '<a href="https://www.google.com">Click me!</a>'
		self.assertEqual(result, expected)

	def test_leaf_to_html_value(self):
		node = LeafNode("p", None)
		with self.assertRaises(ValueError):
			node.to_html()

	def test_leaf_to_html_tag(self):
		node = LeafNode(None, "Hello")
		result = node.to_html()
		expected = "Hello"
		self.assertEqual(result, expected)

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		expected = "<div><span>child</span></div>"
		self.assertEqual(parent_node.to_html(), expected)

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		expected = "<div><span><b>grandchild</b></span></div>"
		self.assertEqual(parent_node.to_html(), expected)























