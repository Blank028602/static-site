class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		if self.props is None:
			return ""
		string = ""
		for key in self.props:
			string += f' {key}="{self.props[key]}"'
		return string

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

#LeafNode
class LeafNode(HTMLNode):
	def __init__(self, tag, value, props = None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value == None:
			raise ValueError
		if self.tag == None:
			return self.value
		else:
			if self.props != None:
				props_html = self.props_to_html()
				return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
			return f"<{self.tag}>{self.value}</{self.tag}>"

#ParentNode
class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag == None:
			raise ValueError("Missing tag")

		if self.children == None:
			raise ValueError("Missing children")

		else:
			string = ""
			string += f"<{self.tag}>"
			for i in self.children:
				string += i.to_html()
			string += f"</{self.tag}>"
			return string
