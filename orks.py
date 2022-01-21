import itertools
import os
import random
import tempfile

from PyPDF2 import PdfFileReader, PdfFileWriter, pdf
import easygui
from PIL import Image, ImageFont, ImageDraw


def main(font_name="CHILLER.TTF", font_size=110):
    resp = easygui.msgbox("First, choose how many sheets you want.\n"
                          "Then select a file which contains 'cheats', one on each line.\n"
                          "Then select a save location.\n"
                          "Profit!")

    num_sheets = easygui.integerbox("How many Ork?", "Am you wanting Ork?")
    if num_sheets is None:
        exit(0)

    cheat_strings_path = easygui.fileopenbox(msg="Where cheats?", default="*.txt", filetypes=["*.txt", "*.*"])
    if cheat_strings_path is None:
        exit(0)

    output_path = easygui.filesavebox(msg="Where am Ork going?", default="orks.pdf", filetypes=["*.pdf"])
    if output_path is None:
        exit(0)

    with open(cheat_strings_path, "r") as fh:
        cheat_strings = [line.strip() for line in fh.readlines()]

    sizes = {
        "ork_points": font_size,
        "dice": round(font_size * 1.2),
        "stats": font_size,
        "cheat": font_size,
        "wounds": round(font_size * 1.1)
    }

    dice_x_positions = [280, 690, 1110, 1490]
    dice_y_position = 1310
    stats_x_positions = [345, 740, 1140, 1550]
    stats_y_positions = [1470, 1620, 1775]

    locations_and_sizes = {
        "ork_points": ((110, 1120), sizes["ork_points"]),
        "meat": ((dice_x_positions[0], dice_y_position), sizes["dice"]),
        "bones": ((dice_x_positions[1], dice_y_position), sizes["dice"]),
        "twitch": ((dice_x_positions[2], dice_y_position), sizes["dice"]),
        "mojo": ((dice_x_positions[3], dice_y_position), sizes["dice"]),
        "fight": ((stats_x_positions[0], stats_y_positions[0]), sizes["stats"]),
        "jock": ((stats_x_positions[0], stats_y_positions[1]), sizes["stats"]),
        "might": ((stats_x_positions[0], stats_y_positions[2]), sizes["stats"]),
        "endure": ((stats_x_positions[1], stats_y_positions[0]), sizes["stats"]),
        "patch": ((stats_x_positions[1], stats_y_positions[1]), sizes["stats"]),
        "resist": ((stats_x_positions[1], stats_y_positions[2]), sizes["stats"]),
        "aim": ((stats_x_positions[2], stats_y_positions[0]), sizes["stats"]),
        "duck": ((stats_x_positions[2], stats_y_positions[1]), sizes["stats"]),
        "loot": ((stats_x_positions[2], stats_y_positions[2]), sizes["stats"]),
        "boss": ((stats_x_positions[3], stats_y_positions[0]), sizes["stats"]),
        "kenning": ((stats_x_positions[3], stats_y_positions[1]), sizes["stats"]),
        "magic": ((stats_x_positions[3], stats_y_positions[2]), sizes["stats"]),
        "cheat": ((110, 2000), sizes["cheat"]),
        "wounds": ((2590, 290), sizes["wounds"]),
    }

    pos_stat_dice = []
    for c in itertools.combinations_with_replacement([4, 6, 8, 12], 4):
        if sum(c) == 32:
            for p in itertools.permutations(c):
                if p not in pos_stat_dice:
                    pos_stat_dice.append(p)
    skill_values = (
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1),
        (2, 2, 2)
    )

    base_image = Image.open("base.jpg")
    new_images = []
    for _ in range(num_sheets):
        skill_dice = random.choice(pos_stat_dice)
        meat_values = random.choice(skill_values)
        bones_values = random.choice(skill_values)
        twitch_values = random.choice(skill_values)
        mojo_values = random.choice(skill_values)

        values = {
            "ork_points": "|",
            "meat": f"d{skill_dice[0]}",
            "bones": f"d{skill_dice[1]}",
            "twitch": f"d{skill_dice[2]}",
            "mojo": f"d{skill_dice[3]}",
            "fight": str(meat_values[0]),
            "jock": str(meat_values[1]),
            "might": str(meat_values[2]),
            "endure": str(bones_values[0]),
            "patch": str(bones_values[1]),
            "resist": str(bones_values[2]),
            "aim": str(twitch_values[0]),
            "duck": str(twitch_values[1]),
            "loot": str(twitch_values[2]),
            "boss": str(mojo_values[0]),
            "kenning": str(mojo_values[1]),
            "magic": str(mojo_values[2]),
            "cheat": random.choice(cheat_strings) if len(cheat_strings) > 0 else "",
            "wounds": str(skill_dice[0] + skill_dice[1] + 10)
        }

        new_image = base_image.copy()
        editable_image = ImageDraw.Draw(new_image)
        for name, (location, size) in locations_and_sizes.items():
            font = ImageFont.truetype(font_name, size)
            editable_image.text(
                location,
                values[name],
                (1, 1, 1),
                font
            )
        new_path = tempfile.mktemp(suffix=".pdf")
        new_image.convert("RGB")
        new_image.save(new_path)
        new_images.append(new_path)

    writer = PdfFileWriter()
    for img in new_images:
        reader = PdfFileReader(img)
        writer.addPage(reader.getPage(0))
        os.remove(img)
    with open(output_path, "wb") as fh:
        writer.write(fh)

    os.system(output_path)


if __name__ == '__main__':
    main()
