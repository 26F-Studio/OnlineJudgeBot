import imgkit
import markdown


async def markdown_to_image(markdown_str: str):
    html = markdown.markdown(markdown_str)
    img = imgkit.from_string(html, False)
    return img
