import os

# Define the paths to the image directories and output markdown file
png_base_path = "./PNG"
svg_base_path = "./SVG"
output_file = "Phoebus_Symbols.md"


# Helper function to create markdown image tag with a caption
def create_image_tag_with_caption(image_path):
    image_name = os.path.basename(image_path)
    formatted_image_path = image_path.replace(' ', '%20').replace('\\', '/')
    image_tag = f"![{image_name}]({formatted_image_path})"
    caption = f"*{image_name}*"
    return f"{image_tag}\n\n{caption}"


# Function to recursively scan directories and create markdown content
def generate_markdown(directory, relative_path):
    markdown_content = ""
    folder_name = os.path.basename(directory)

    # Add the folder name as a section or subsection heading
    if relative_path == "":
        markdown_content += f"# {folder_name}\n\n"
    else:
        heading_level = relative_path.count(os.sep) + 1
        markdown_content += f"{'#' * heading_level} {folder_name}\n\n"

    # Get all the files and directories in the current directory
    items = sorted(os.listdir(directory))

    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            # If it's a directory, recursively process it
            new_relative_path = os.path.join(relative_path, item)
            markdown_content += generate_markdown(item_path, new_relative_path)
        else:
            # If it's a file, create a markdown image tag with caption for PNG or SVG files
            if item.endswith(".png") or item.endswith(".svg"):
                markdown_content += f"{create_image_tag_with_caption(os.path.join(relative_path, item))}\n\n"

    return markdown_content


# Function to generate a single markdown file containing both PNG and SVG
def generate_combined_markdown():
    # Initialize the content
    markdown_content = "# Images\n\n"

    # Process PNG and SVG directories and generate content
    if os.path.exists(png_base_path):
        markdown_content += "## PNG Images\n\n"
        markdown_content += generate_markdown(png_base_path, os.path.relpath(png_base_path))

    if os.path.exists(svg_base_path):
        markdown_content += "## SVG Images\n\n"
        markdown_content += generate_markdown(svg_base_path, os.path.relpath(svg_base_path))

    # Write the markdown content to a file
    with open(output_file, "w") as f:
        f.write(markdown_content)

    print(f"Markdown file generated: {output_file}")


if __name__ == "__main__":
    generate_combined_markdown()
