from textnode import TextType, TextNode

def split_helper(text, delimeter, type):
    splited = text.split(delimeter)

    if len(splited) != 3:
        raise Exception("nigga there's something wrong with the delimeter!!!")
    
    node1 = TextNode(splited[0], TextType.TEXT)
    node2 = TextNode(splited[1], type)
    node3 = TextNode(splited[2], TextType.TEXT)

    return [node1, node2, node3]

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    result = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            result.append(node)

        else:
            result.extend(split_helper(node.text, delimeter, text_type))

    return result

        