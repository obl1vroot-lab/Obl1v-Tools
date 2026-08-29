"""
Color Picker & Converter - Pick, preview, and convert colors between formats.

Supports HEX input, RGB sliders, preview display, and auto-conversion
to RGB, HSL, HSV, CMYK, and named HTML/CSS colors.
"""

import customtkinter as ctk
from tkinter import messagebox
import uuid
import json
import time
import colorsys
import random
from datetime import datetime


CSS_COLORS = {
    "aliceblue": "#f0f8ff", "antiquewhite": "#faebd7", "aqua": "#00ffff", "aquamarine": "#7fffd4",
    "azure": "#f0ffff", "beige": "#f5f5dc", "bisque": "#ffe4c4", "black": "#000000",
    "blanchedalmond": "#ffebcd", "blue": "#0000ff", "blueviolet": "#8a2be2", "brown": "#a52a2a",
    "burlywood": "#deb887", "cadetblue": "#5f9ea0", "chartreuse": "#7fff00", "chocolate": "#d2691e",
    "coral": "#ff7f50", "cornflowerblue": "#6495ed", "cornsilk": "#fff8dc", "crimson": "#dc143c",
    "cyan": "#00ffff", "darkblue": "#00008b", "darkcyan": "#008b8b", "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9", "darkgreen": "#006400", "darkkhaki": "#bdb76b", "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f", "darkorange": "#ff8c00", "darkorchid": "#9932cc", "darkred": "#8b0000",
    "darksalmon": "#e9967a", "darkseagreen": "#8fbc8f", "darkslateblue": "#483d8b", "darkslategray": "#2f4f4f",
    "darkturquoise": "#00ced1", "darkviolet": "#9400d3", "deeppink": "#ff1493", "deepskyblue": "#00bfff",
    "dimgray": "#696969", "dodgerblue": "#1e90ff", "firebrick": "#b22222", "floralwhite": "#fffaf0",
    "forestgreen": "#228b22", "fuchsia": "#ff00ff", "gainsboro": "#dcdcdc", "ghostwhite": "#f8f8ff",
    "gold": "#ffd700", "goldenrod": "#daa520", "gray": "#808080", "green": "#008000",
    "greenyellow": "#adff2f", "honeydew": "#f0fff0", "hotpink": "#ff69b4", "indianred": "#cd5c5c",
    "indigo": "#4b0082", "ivory": "#fffff0", "khaki": "#f0e68c", "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5", "lawngreen": "#7cfc00", "lemonchiffon": "#fffacd", "lightblue": "#add8e6",
    "lightcoral": "#f08080", "lightcyan": "#e0ffff", "lightgoldenrodyellow": "#fafad2", "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90", "lightpink": "#ffb6c1", "lightsalmon": "#ffa07a", "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa", "lightslategray": "#778899", "lightsteelblue": "#b0c4de", "lightyellow": "#ffffe0",
    "lime": "#00ff00", "limegreen": "#32cd32", "linen": "#faf0e6", "magenta": "#ff00ff",
    "maroon": "#800000", "mediumaquamarine": "#66cdaa", "mediumblue": "#0000cd", "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db", "mediumseagreen": "#3cb371", "mediumslateblue": "#7b68ee", "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc", "mediumvioletred": "#c71585", "midnightblue": "#191970", "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1", "moccasin": "#ffe4b5", "navajowhite": "#ffdead", "navy": "#000080",
    "oldlace": "#fdf5e6", "olive": "#808000", "olivedrab": "#6b8e23", "orange": "#ffa500",
    "orangered": "#ff4500", "orchid": "#da70d6", "palegoldenrod": "#eee8aa", "palegreen": "#98fb98",
    "paleturquoise": "#afeeee", "palevioletred": "#db7093", "papayawhip": "#ffefd5", "peachpuff": "#ffdab9",
    "peru": "#cd853f", "pink": "#ffc0cb", "plum": "#dda0dd", "powderblue": "#b0e0e6",
    "purple": "#800080", "rebeccapurple": "#663399", "red": "#ff0000", "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1", "saddlebrown": "#8b4513", "salmon": "#fa8072", "sandybrown": "#f4a460",
    "seagreen": "#2e8b57", "seashell": "#fff5ee", "sienna": "#a0522d", "silver": "#c0c0c0",
    "skyblue": "#87ceeb", "slateblue": "#6a5acd", "slategray": "#708090", "snow": "#fffafa",
    "springgreen": "#00ff7f", "steelblue": "#4682b4", "tan": "#d2b48c", "teal": "#008080",
    "thistle": "#d8bfd8", "tomato": "#ff6347", "turquoise": "#40e0d0", "violet": "#ee82ee",
    "wheat": "#f5deb3", "white": "#ffffff", "whitesmoke": "#f5f5f5", "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}

NAME_TO_HEX = {name.lower(): hex_val for name, hex_val in CSS_COLORS.items()}
HEX_TO_NAME = {v: k for k, v in NAME_TO_HEX.items()}


def hex_to_rgb(hex_str):
    h = hex_str.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_hsl(r, g, b):
    r_n, g_n, b_n = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r_n, g_n, b_n)
    return int(h * 360), int(s * 100), int(l * 100)


def rgb_to_hsv(r, g, b):
    r_n, g_n, b_n = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(r_n, g_n, b_n)
    return int(h * 360), int(s * 100), int(v * 100)


def rgb_to_cmyk(r, g, b):
    if r == 0 and g == 0 and b == 0:
        return 0, 0, 0, 100
    c = 1 - r / 255.0
    m = 1 - g / 255.0
    y = 1 - b / 255.0
    k = min(c, m, y)
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return int(c * 100), int(m * 100), int(y * 100), int(k * 100)


def create_ui(frame, COLORS, FONTS):
    """Build the Color Picker GUI inside the given frame."""

    rgb_sliders = [None, None, None]
    hex_entry_ref = [None]

    # --- Header ---
    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(20, 10))
    ctk.CTkLabel(header, text="Color Picker & Converter", font=FONTS["title"], text_color=COLORS["accent"]).pack(anchor="w")
    ctk.CTkLabel(header, text="Pick colors, preview, and convert between formats", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w")

    content = ctk.CTkFrame(frame, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    # === Left side: Input and Preview ===
    left = ctk.CTkFrame(content, fg_color="transparent")
    left.pack(side="left", fill="both", expand=True, padx=(0, 8))

    # Hex input
    input_card = ctk.CTkFrame(left, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    input_card.pack(fill="x", pady=(0, 8))

    ctk.CTkLabel(input_card, text="Color Input", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 5))

    hex_row = ctk.CTkFrame(input_card, fg_color="transparent")
    hex_row.pack(fill="x", padx=15, pady=(0, 10))
    ctk.CTkLabel(hex_row, text="HEX:", font=FONTS["body"], text_color=COLORS["text_dim"], width=40).pack(side="left")
    hex_entry = ctk.CTkEntry(hex_row, placeholder_text="#00d4ff", font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"])
    hex_entry.pack(side="left", fill="x", expand=True, padx=(4, 4))
    hex_entry_ref[0] = hex_entry

    def set_random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        hex_val = rgb_to_hex(r, g, b)
        hex_entry.delete(0, "end")
        hex_entry.insert(0, hex_val)
        apply_color_from_hex()

    ctk.CTkButton(hex_row, text="Random", width=70, font=FONTS["mono_small"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=set_random_color).pack(side="left", padx=(4, 0))

    # RGB sliders
    slider_card = ctk.CTkFrame(left, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    slider_card.pack(fill="x", pady=(0, 8))

    ctk.CTkLabel(slider_card, text="RGB Sliders", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 5))

    slider_vars = [ctk.IntVar(value=0) for _ in range(3)]
    slider_labels = []

    for i, (label, color) in enumerate([("R", "#ff4444"), ("G", "#44ff44"), ("B", "#4444ff")]):
        row = ctk.CTkFrame(slider_card, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=2)
        ctk.CTkLabel(row, text=label, font=FONTS["mono"], text_color=COLORS["text"], width=20).pack(side="left")
        sl = ctk.CTkSlider(row, from_=0, to=255, variable=slider_vars[i], progress_color=color, button_color=color, button_hover_color=color, fg_color=COLORS["bg_input"], width=180)
        sl.pack(side="left", padx=(4, 4))
        lbl = ctk.CTkLabel(row, text="0", font=FONTS["mono_small"], text_color=COLORS["text_dim"], width=35, anchor="e")
        lbl.pack(side="left")
        slider_labels.append(lbl)
        rgb_sliders[i] = (sl, slider_vars[i], lbl)

    # Preview
    preview_card = ctk.CTkFrame(left, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    preview_card.pack(fill="x", pady=(0, 8))

    ctk.CTkLabel(preview_card, text="Preview", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 5))

    preview_frame = ctk.CTkFrame(preview_card, fg_color="#000000", corner_radius=8, height=120, border_width=2, border_color=COLORS["border"])
    preview_frame.pack(fill="x", padx=15, pady=(0, 15))
    preview_frame.pack_propagate(False)

    color_name_label = ctk.CTkLabel(preview_card, text="", font=FONTS["body"], text_color=COLORS["text_dim"])
    color_name_label.pack(anchor="w", padx=15, pady=(0, 10))

    # === Right side: Conversions ===
    right = ctk.CTkFrame(content, fg_color="transparent")
    right.pack(side="left", fill="both", expand=True, padx=(8, 0))

    conv_card = ctk.CTkFrame(right, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    conv_card.pack(fill="both", expand=True)

    ctk.CTkLabel(conv_card, text="Color Conversions", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))

    conversion_outputs = {}
    for label_text in ["HEX", "RGB", "HSL", "HSV", "CMYK", "CSS Name"]:
        row = ctk.CTkFrame(conv_card, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=3)
        ctk.CTkLabel(row, text=label_text + ":", font=FONTS["body"], text_color=COLORS["text_dim"], width=80, anchor="w").pack(side="left")
        txt = ctk.CTkEntry(row, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"])
        txt.pack(side="left", fill="x", expand=True, padx=(4, 4))
        txt.configure(state="disabled")
        conversion_outputs[label_text] = txt

        def copy_cb(entry=txt):
            entry.configure(state="normal")
            val = entry.get()
            entry.configure(state="disabled")
            if val:
                frame.clipboard_clear()
                frame.clipboard_append(val)

        ctk.CTkButton(row, text="Copy", width=50, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], hover_color=COLORS["accent"], text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, command=copy_cb).pack(side="left")

    def update_conversion_output(label, value):
        entry = conversion_outputs[label]
        entry.configure(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        entry.configure(state="disabled")

    def apply_color_from_hex():
        hex_str = hex_entry.get().strip()
        if not hex_str.startswith("#"):
            hex_str = "#" + hex_str
        if len(hex_str) != 7:
            return
        try:
            r, g, b = hex_to_rgb(hex_str)
        except ValueError:
            return

        preview_frame.configure(fg_color=hex_str)

        for i, val in enumerate([r, g, b]):
            slider_vars[i].set(val)
            slider_labels[i].configure(text=str(val))

        h, s, l = rgb_to_hsl(r, g, b)
        hsv_h, hsv_s, hsv_v = rgb_to_hsv(r, g, b)
        c, m, y, k = rgb_to_cmyk(r, g, b)

        update_conversion_output("HEX", hex_str.upper())
        update_conversion_output("RGB", f"rgb({r}, {g}, {b})")
        update_conversion_output("HSL", f"hsl({h}, {s}%, {l}%)")
        update_conversion_output("HSV", f"hsv({hsv_h}, {sv_s}%, {hsv_v}%)" if False else f"hsv({hsv_h}, {hsv_s}%, {hsv_v}%)")
        update_conversion_output("CMYK", f"cmyk({c}%, {m}%, {y}%, {k}%)")

        css_name = HEX_TO_NAME.get(hex_str.lower(), "")
        update_conversion_output("CSS Name", css_name if css_name else "No CSS name")

        color_name_label.configure(text=css_name.title() if css_name else "")

    def apply_color_from_sliders():
        r = slider_vars[0].get()
        g = slider_vars[1].get()
        b = slider_vars[2].get()

        for i, val in enumerate([r, g, b]):
            slider_labels[i].configure(text=str(val))

        hex_val = rgb_to_hex(r, g, b)
        preview_frame.configure(fg_color=hex_val)

        hex_entry.delete(0, "end")
        hex_entry.insert(0, hex_val.upper())

        h, s, l = rgb_to_hsl(r, g, b)
        hsv_h, hsv_s, hsv_v = rgb_to_hsv(r, g, b)
        c, m, y, k = rgb_to_cmyk(r, g, b)

        update_conversion_output("HEX", hex_val.upper())
        update_conversion_output("RGB", f"rgb({r}, {g}, {b})")
        update_conversion_output("HSL", f"hsl({h}, {s}%, {l}%)")
        update_conversion_output("HSV", f"hsv({hsv_h}, {hsv_s}%, {hsv_v}%)")
        update_conversion_output("CMYK", f"cmyk({c}%, {m}%, {y}%, {k}%)")

        css_name = HEX_TO_NAME.get(hex_val.lower(), "")
        update_conversion_output("CSS Name", css_name if css_name else "No CSS name")
        color_name_label.configure(text=css_name.title() if css_name else "")

    hex_entry.bind("<KeyRelease>", lambda e: apply_color_from_hex())

    for i in range(3):
        def on_slider_change(var=slider_vars[i]):
            apply_color_from_sliders()
        slider_vars[i].trace_add("write", on_slider_change)

    apply_color_from_hex()
