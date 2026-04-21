from textnode import TextNode, TextType

def split_single_node(text, delimiter, text_type):
    parts = text.split(delimiter)

    if len(parts) != 3:
        raise ValueError("Inline element delimiter is wrong")
    
    return [
        TextNode(parts[0], TextType.TEXT),
        TextNode(parts[1], text_type),
        TextNode(parts[2], TextType.TEXT)
    ]

def split_nodes_delimiter(old_node, delimiter, text_type):
    result = []

    valid_delimiter = ["`", "_", "**"]

    if delimiter not in valid_delimiter:
        raise ValueError("This delimiter is not supported")
    
    for node in old_node:
        if node.text_type != TextType.TEXT:
            result.append(node)

        else:
            result.extend(split_single_node(node.text, delimiter, text_type))

    return result
