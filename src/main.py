import os
import shutil

from markdown_to_html import extract_title, markdown_to_html_node


def copy_recursive(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied file: {dest_path}")
        else:
            copy_recursive(src_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Generate an HTML page for every .md file under dir_path_content, mirroring paths under dest_dir_path."""
    for root, _dirs, files in os.walk(dir_path_content):
        for name in files:
            if not name.endswith(".md"):
                continue
            from_path = os.path.join(root, name)
            rel = os.path.relpath(from_path, dir_path_content)
            dest_rel = os.path.splitext(rel)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, dest_rel)
            generate_page(from_path, template_path, dest_path)


def main():
    print("Generating site...")
    copy_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    print("Site generated successfully!")


if __name__ == "__main__":
    main()