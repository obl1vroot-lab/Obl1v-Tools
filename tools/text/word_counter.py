"""Word/Char/Line Counter - Analyze text statistics including word frequencies."""

import customtkinter as ctk
import re
import random


def create_ui(frame, COLORS, FONTS):
    stats_labels = {}

    def analyze(event=None):
        text = input_text.get("1.0", "end-1c")
        chars = len(text)
        chars_no_spaces = len(text.replace(" ", "").replace("\n", ""))
        words = len(text.split()) if text.strip() else 0
        lines = text.count("\n") + 1 if text else 0
        sentences = len(re.findall(r'[.!?]+', text))
        paragraphs = len([p for p in text.split("\n\n") if p.strip()]) if text.strip() else 0

        stats_labels["chars_val"].configure(text=str(chars))
        stats_labels["chars_ns_val"].configure(text=str(chars_no_spaces))
        stats_labels["words_val"].configure(text=str(words))
        stats_labels["lines_val"].configure(text=str(lines))
        stats_labels["sentences_val"].configure(text=str(sentences))
        stats_labels["paragraphs_val"].configure(text=str(paragraphs))

        if text.strip():
            clean = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            freq = {}
            for w in clean:
                freq[w] = freq.get(w, 0) + 1
            top5 = sorted(freq.items(), key=lambda x: -x[1])[:5]
            top5_text = "\n".join(f"  {w}: {c}" for w, c in top5) if top5 else "  No words found"
        else:
            top5_text = "  No words found"
        top5_display.configure(state="normal")
        top5_display.delete("1.0", "end")
        top5_display.insert("1.0", top5_text)
        top5_display.configure(state="disabled")

    frame.configure(fg_color=COLORS["bg_dark"])

    header = ctk.CTkLabel(frame, text="Word / Char / Line Counter", font=FONTS["title"], text_color=COLORS["text"])
    header.pack(pady=(15, 10))

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="both", expand=True, padx=15, pady=(0, 5))

    input_label = ctk.CTkLabel(input_frame, text="Input Text", font=FONTS["heading"], text_color=COLORS["accent"])
    input_label.pack(anchor="w")

    input_text = ctk.CTkTextbox(input_frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                                text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                                corner_radius=6, height=150)
    input_text.pack(fill="both", expand=True)
    input_text.bind("<KeyRelease>", analyze)

    analyze_btn = ctk.CTkButton(frame, text="Analyze", font=FONTS["button"],
                                fg_color=COLORS["accent"], hover_color=COLORS["green"],
                                text_color=COLORS["bg_dark"], command=analyze, height=32)
    analyze_btn.pack(pady=5)

    stats_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1,
                               border_color=COLORS["border"])
    stats_frame.pack(fill="x", padx=15, pady=(5, 5))

    stat_items = ["chars", "chars_ns", "words", "lines", "sentences", "paragraphs"]
    stat_names = ["Characters", "Chars (no spaces)", "Words", "Lines", "Sentences", "Paragraphs"]

    grid_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
    grid_frame.pack(fill="x", padx=10, pady=8)
    grid_frame.columnconfigure((0, 1, 2), weight=1)

    for i, (key, name) in enumerate(zip(stat_items, stat_names)):
        r, c = divmod(i, 3)
        cell = ctk.CTkFrame(grid_frame, fg_color="transparent")
        cell.grid(row=r, column=c, padx=5, pady=3, sticky="w")
        ctk.CTkLabel(cell, text=name, font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w")
        lbl = ctk.CTkLabel(cell, text="0", font=FONTS["mono"], text_color=COLORS["accent"])
        lbl.pack(anchor="w")
        stats_labels[f"{key}_val"] = lbl

    top5_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1,
                              border_color=COLORS["border"])
    top5_frame.pack(fill="x", padx=15, pady=(0, 15))

    ctk.CTkLabel(top5_frame, text="Top 5 Words", font=FONTS["heading"], text_color=COLORS["accent"]).pack(
        anchor="w", padx=10, pady=(8, 2))

    top5_display = ctk.CTkTextbox(top5_frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                                  text_color=COLORS["text"], border_width=0, height=80, state="disabled")
    top5_display.pack(fill="x", padx=10, pady=(0, 8))

    analyze()
