import os
import re


def loadHTMLContent(directory, filename, font_family):
    base_dir = os.path.dirname(__file__)  # path to /app/utils
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))  # path to project root
    html_file_path = os.path.join(base_dir, directory, filename)

    try:
        with open(html_file_path, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()
    except FileNotFoundError:
        return f"""
        <div style="color: red; text-align: center; font-size: 18px; padding: 20px;">
            Error: Could not find the content file at <code>{html_file_path}</code>.
        </div>
        """
    except Exception as e:
        return f"""
        <div style="color: red; text-align: center; font-size: 18px; padding: 20px;">
            Error: An unexpected error occurred while reading the content file.<br>
            Details: {str(e)}
        </div>
        """

    # Fix asset paths to use the absolute path under the root-level assets folder
    # this function to replace the relative path with an absolute path while rendering HTML content
    def replace_relative_path(match):
        quote = match.group(1)
        rel_path = match.group(2)
        abs_path = os.path.join(project_root, "assets", rel_path)
        return f'{quote}file://{abs_path}'

    # Replace paths like src="../icons/..." or url("../fonts/...")
    html_content = re.sub(r'(src=["\'])\.\./([^"\']+)', replace_relative_path, html_content)
    html_content = re.sub(r'(url\(["\'])\.\./([^"\')]+)', replace_relative_path, html_content)

    # Inject font family
    if "{}" in html_content:
        return html_content.format(font_family)
    else:
        return f"<div style='font-family: {font_family};'>{html_content}</div>"
