import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_to_block_type_headings(self):
        self.assertEqual(block_to_block_type("# Heading-1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading-2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading-3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading-4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading-5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading-6"), BlockType.HEADING)


    def test_block_to_block_type_code(self):
        md = """
```
print("hello world")
```
"""

        self.assertEqual(block_to_block_type(md.strip()), BlockType.CODE)


    def test_block_to_block_type_quote(self):
        md = """
> best
> quote
> ever
"""

        self.assertEqual(block_to_block_type(md.strip()), BlockType.QUOTE)


    def test_block_to_block_type_unordered_list(self):
        md = """
- first
- second
- third
"""

        self.assertEqual(block_to_block_type(md.strip()), BlockType.UNORDERED_LIST)


    def test_block_to_block_type_ordered_list(self):
        md = """
1. First
2. Second
3. Third
"""

        self.assertEqual(block_to_block_type(md.strip()), BlockType.ORDERED_LIST)

        invalid_md = """
2. Milk
33. Sugar
42. Life
"""

        self.assertNotEqual(block_to_block_type(invalid_md.strip()), BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
