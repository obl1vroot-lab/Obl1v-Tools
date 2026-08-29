"""Text Case Converter - Transform text between different case formats."""

import customtkinter as ctk
import re
import random


def create_ui(frame, COLORS, FONTS):
    frame.configure(fg_color=COLORS["bg_dark"])

    header = ctk.CTkLabel(frame, text="Text Case Converter", font=FONTS["title"], text_color=COLORS["text"])
    header.pack(pady=(15, 10))

    input_label = ctk.CTkLabel(frame, text="Input Text", font=FONTS["heading"], text_color=COLORS["accent"])
    input_label.pack(anchor="w", padx=15)

    input_text = ctk.CTkTextbox(frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                                text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                                corner_radius=6, height=150)
    input_text.pack(fill="both", expand=True, padx=15, pady=(5, 5))

    def set_result(text):
        result_text.configure(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", text)
        result_text.configure(state="disabled")

    def get_input():
        return input_text.get("1.0", "end-1c")

    def to_upper():
        set_result(get_input().upper())

    def to_lower():
        set_result(get_input().lower())

    def to_title():
        set_result(get_input().title())

    def to_sentence():
        text = get_input()
        result = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text.lower())
        set_result(result)

    def to_alternating():
        text = get_input()
        result = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))
        set_result(result)

    def copy_result():
        frame.clipboard_clear()
        frame.clipboard_append(result_text.get("1.0", "end-1c"))

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=15, pady=5)

    buttons = [
        ("UPPERCASE", to_upper, COLORS["accent"]),
        ("lowercase", to_lower, COLORS["accent"]),
        ("Title Case", to_title, COLORS["accent"]),
        ("Sentence case", to_sentence, COLORS["accent"]),
        ("aLtErNaTiNg", to_alternating, COLORS["accent"]),
        ("Copy", copy_result, COLORS["green"]),
    ]

    for i, (text, cmd, color) in enumerate(buttons):
        btn = ctk.CTkButton(btn_frame, text=text, font=FONTS["button"], fg_color=color,
                            hover_color=COLORS["yellow"], text_color=COLORS["bg_dark"],
                            command=cmd, height=30, width=100)
        btn.grid(row=i // 3, column=i % 3, padx=3, pady=3, sticky="ew")

    for col in range(3):
        btn_frame.columnconfigure(col, weight=1)

    result_label = ctk.CTkLabel(frame, text="Result", font=FONTS["heading"], text_color=COLORS["accent"])
    result_label.pack(anchor="w", padx=15, pady=(5, 0))

    result_text = ctk.CTkTextbox(frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                                 text_color=COLORS["green"], border_width=1, border_color=COLORS["border"],
                                 corner_radius=6, height=150, state="disabled")
    result_text.pack(fill="both", expand=True, padx=15, pady=(5, 15))
