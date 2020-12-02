import io

from PIL import Image, ImageColor
import numpy as np

async def generate_pfp(colour, template_colour):
    disc_template = Image.open('images/discord_logo.png')
    if colour.lower() == "remedy":
        colour = "#19c7fc"
    if template_colour is not None:
        try:
            template_colour = ImageColor.getcolor('#19c7fc', 'P') if template_colour.lower() == "remedy" \
                else ImageColor.getcolor(template_colour, 'P')
        except ValueError:
            template_colour = ImageColor.getcolor(f"#{template_colour}", 'P')
        disc_template = disc_template.convert('RGBA')
        data = np.array(disc_template)
        r, g, b, a = data.T
        white_areas = (r == 255) & (b == 255) & (g == 255)
        data[..., :-1][white_areas.T] = template_colour
        disc_template = Image.fromarray(data)
    try:
        colour = ImageColor.getcolor(colour, 'P')
    except ValueError:
        colour = ImageColor.getcolor(f"#{colour}", 'P')
    with Image.new('RGB', (1350, 1200), color=colour) as img:
        img.paste(disc_template, (225, 200), disc_template)
    with io.BytesIO() as output:
        img.save(output, format="PNG")
        return output.getvalue()
