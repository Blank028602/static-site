from enum import Enum

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING= "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
	if block.startswith("#"):
		count = 0
		for char in block:
			if char == "#":
				count += 1
			else:
				break
		if 1 <= count <= 6:
			if len(block) > count and block[count] == " ":
				return BlockType.HEADING
			return BlockType.PARAGRAPH
	elif block.startswith("```"):
		if block.endswith("```"):
			return BlockType.CODE
		return BlockType.PARAGRAPH
	elif block.startswith(">"):
		lines = block.split("\n")
		for line in lines:
			if not line.startswith(">"):
				return BlockType.PARAGRAPH
		return BlockType.QUOTE
	elif block.startswith("- "):
		lines = block.split("\n")
		for line in lines:
			if not line.startswith("- "):
				return BlockType.PARAGRAPH
		return BlockType.UNORDERED_LIST
	elif block.startswith("1. "):
		lines = block.split("\n")
		expected_number = 1
		for line in lines:
			if line.startswith(f"{expected_number}. "):
				expected_number += 1
			else:
				return BlockType.PARAGRAPH
		return BlockType.ORDERED_LIST
	else:
		return BlockType.PARAGRAPH
