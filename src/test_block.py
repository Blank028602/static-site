import unittest
from block import BlockType, block_to_block_type

class TestBlock(unittest.TestCase):
	def test_heading(self):
		block = "# This is a heading"
		type = block_to_block_type(block)
		self.assertEqual(type, BlockType.HEADING)
