from textnode import TextNode, TextType

def main():
    node = TextNode("bla bla blah", TextType.TEXT)
    node2 = TextNode("heres the chicken nigga", TextType.LINK, "jjjii.oisvhj")

    print(node)
    print(node2)

main()