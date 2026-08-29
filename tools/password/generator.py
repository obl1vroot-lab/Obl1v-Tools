"""Password Generator - Secure password generation using secrets module."""

import customtkinter as ctk
import secrets
import string


def create_ui(frame, COLORS, FONTS):
    options = {
        "uppercase": {"var": ctk.BooleanVar(value=True), "label": "Uppercase (A-Z)"},
        "lowercase": {"var": ctk.BooleanVar(value=True), "label": "Lowercase (a-z)"},
        "digits": {"var": ctk.BooleanVar(value=True), "label": "Digits (0-9)"},
        "symbols": {"var": ctk.BooleanVar(value=True), "label": "Symbols (!@#$...)"},
    }
    output_var = ctk.StringVar()

    ctk.CTkLabel(frame, text="Password Generator", font=FONTS["heading"],
                 text_color=COLORS["text"], anchor="w").pack(fill="x", padx=16, pady=(16, 8))

    slider_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    slider_frame.pack(fill="x", padx=16, pady=(0, 8))

    length_var = ctk.IntVar(value=20)
    ctk.CTkLabel(slider_frame, text="Length", font=FONTS["body"],
                 text_color=COLORS["text"]).pack(side="left", padx=(12, 4), pady=10)
    ctk.CTkLabel(slider_frame, textvariable=length_var, font=FONTS["mono"],
                 text_color=COLORS["accent"], width=30).pack(side="right", padx=(4, 12), pady=10)
    ctk.CTkSlider(slider_frame, from_=8, to=64, variable=length_var,
                  button_color=COLORS["accent"], button_hover_color=COLORS["accent"],
                  fg_color=COLORS["bg_input"], progress_color=COLORS["accent"]
                  ).pack(side="right", fill="x", expand=True, padx=8, pady=10)

    checks_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    checks_frame.pack(fill="x", padx=16, pady=(0, 8))

    for key in ["uppercase", "lowercase", "digits", "symbols"]:
        ctk.CTkCheckBox(checks_frame, text=options[key]["label"], variable=options[key]["var"],
                        font=FONTS["body"], text_color=COLORS["text"],
                        fg_color=COLORS["accent"], hover_color=COLORS["accent"]
                        ).pack(anchor="w", padx=12, pady=4)

    def generate(*_):
        length = length_var.get()
        pools = []
        if options["uppercase"]["var"].get():
            pools.append(string.ascii_uppercase)
        if options["lowercase"]["var"].get():
            pools.append(string.ascii_lowercase)
        if options["digits"]["var"].get():
            pools.append(string.digits)
        if options["symbols"]["var"].get():
            pools.append(string.punctuation)
        if not pools:
            output_var.set("Select at least one option")
            return
        required = [secrets.choice(pool) for pool in pools]
        all_chars = "".join(pools)
        remaining = [secrets.choice(all_chars) for _ in range(length - len(required))]
        combined = required + remaining
        secrets.SystemRandom().shuffle(combined)
        output_var.set("".join(combined))

    ctk.CTkButton(frame, text="Generate", font=FONTS["button"], fg_color=COLORS["accent"],
                  hover_color=COLORS["green"], command=generate).pack(fill="x", padx=16, pady=(0, 8))

    out_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    out_frame.pack(fill="x", padx=16, pady=(0, 16))

    ctk.CTkLabel(out_frame, text="Output", font=FONTS["body"],
                 text_color=COLORS["text_dim"]).pack(anchor="w", padx=12, pady=(8, 0))

    row = ctk.CTkFrame(out_frame, fg_color="transparent")
    row.pack(fill="x", padx=12, pady=(4, 10))
    entry = ctk.CTkEntry(row, textvariable=output_var, font=FONTS["mono"],
                         fg_color=COLORS["bg_input"], text_color=COLORS["text"],
                         border_color=COLORS["border"], state="readonly", height=36)
    entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(output_var.get())

    ctk.CTkButton(row, text="Copy", font=FONTS["button"], width=60,
                  fg_color=COLORS["border"], hover_color=COLORS["accent"],
                  command=copy).pack(side="right", ipady=2)

    generate()
