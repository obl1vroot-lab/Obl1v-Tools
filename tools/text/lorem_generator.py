"""Lorem Ipsum Generator - Generate placeholder text with configurable length."""

import customtkinter as ctk
import re
import random


LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
    "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
    "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
    "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
    "deserunt", "mollit", "anim", "id", "est", "laborum", "vitae", "elementum",
    "curabitur", "sollicitudin", "purus", "viverra", "accumsan", "nisl", "nunc",
    "faucibus", "ornare", "suspendisse", "potenti", "nullam", "ac", "tortor",
    "dignissim", "convallis", "aenean", "pharetra", "lacus", "vel", "facilisis",
    "volutpat", "blandit", "cursus", "risus", "pellentesque", "habitant", "morbi",
    "tristique", "senectus", "netus", "malesuada", "fames", "turpis", "egestas",
    "maecenas", "ultricies", "mi", "feugiat", "pretium", "donec", "massa",
    "sapien", "nibh", "praesent", "tristique"
]


def create_ui(frame, COLORS, FONTS):
    frame.configure(fg_color=COLORS["bg_dark"])

    header = ctk.CTkLabel(frame, text="Lorem Ipsum Generator", font=FONTS["title"], text_color=COLORS["text"])
    header.pack(pady=(15, 10))

    controls = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1,
                            border_color=COLORS["border"])
    controls.pack(fill="x", padx=15, pady=(0, 10))
    controls.columnconfigure(1, weight=1)

    ctk.CTkLabel(controls, text="Paragraphs:", font=FONTS["body"], text_color=COLORS["text"]).grid(
        row=0, column=0, padx=(10, 5), pady=8, sticky="w")
    para_var = ctk.IntVar(value=3)
    para_slider = ctk.CTkSlider(controls, from_=1, to=10, number_of_steps=9, variable=para_var,
                                button_color=COLORS["accent"], progress_color=COLORS["accent"],
                                button_hover_color=COLORS["green"])
    para_slider.grid(row=0, column=1, padx=5, pady=8, sticky="ew")
    para_val_label = ctk.CTkLabel(controls, textvariable=para_var, font=FONTS["mono"],
                                  text_color=COLORS["accent"], width=30)
    para_val_label.grid(row=0, column=2, padx=(5, 10), pady=8)

    ctk.CTkLabel(controls, text="Words/para:", font=FONTS["body"], text_color=COLORS["text"]).grid(
        row=1, column=0, padx=(10, 5), pady=8, sticky="w")
    word_var = ctk.IntVar(value=50)
    word_slider = ctk.CTkSlider(controls, from_=10, to=150, number_of_steps=14, variable=word_var,
                                button_color=COLORS["accent"], progress_color=COLORS["accent"],
                                button_hover_color=COLORS["green"])
    word_slider.grid(row=1, column=1, padx=5, pady=8, sticky="ew")
    word_val_label = ctk.CTkLabel(controls, textvariable=word_var, font=FONTS["mono"],
                                  text_color=COLORS["accent"], width=30)
    word_val_label.grid(row=1, column=2, padx=(5, 10), pady=8)

    def generate():
        num_paras = para_var.get()
        words_per = word_var.get()
        paragraphs = []
        for _ in range(num_paras):
            words = random.sample(LOREM_WORDS, min(words_per, len(LOREM_WORDS)))
            while len(words) < words_per:
                words.extend(random.sample(LOREM_WORDS, min(words_per - len(words), len(LOREM_WORDS))))
            words = words[:words_per]
            words[0] = words[0].capitalize()
            para = " ".join(words) + "."
            paragraphs.append(para)
        text = "\n\n".join(paragraphs)
        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("1.0", text)
        output.configure(state="disabled")

    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(output.get("1.0", "end-1c"))

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=15, pady=5)

    ctk.CTkButton(btn_frame, text="Generate", font=FONTS["button"], fg_color=COLORS["accent"],
                  hover_color=COLORS["green"], text_color=COLORS["bg_dark"],
                  command=generate, height=32).pack(side="left", padx=(0, 5))
    ctk.CTkButton(btn_frame, text="Copy", font=FONTS["button"], fg_color=COLORS["green"],
                  hover_color=COLORS["yellow"], text_color=COLORS["bg_dark"],
                  command=copy, height=32).pack(side="left")

    output_label = ctk.CTkLabel(frame, text="Generated Text", font=FONTS["heading"], text_color=COLORS["accent"])
    output_label.pack(anchor="w", padx=15, pady=(10, 0))

    output = ctk.CTkTextbox(frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                            text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                            corner_radius=6, state="disabled")
    output.pack(fill="both", expand=True, padx=15, pady=(5, 15))

    generate()
