"""Regex Tester - Test regular expressions against text with match highlighting."""

import customtkinter as ctk
import re
import random


def create_ui(frame, COLORS, FONTS):
    frame.configure(fg_color=COLORS["bg_dark"])

    header = ctk.CTkLabel(frame, text="Regex Tester", font=FONTS["title"], text_color=COLORS["text"])
    header.pack(pady=(15, 10))

    pattern_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8, border_width=1,
                                border_color=COLORS["border"])
    pattern_frame.pack(fill="x", padx=15, pady=(0, 5))
    pattern_frame.columnconfigure(1, weight=1)

    ctk.CTkLabel(pattern_frame, text="Pattern:", font=FONTS["heading"], text_color=COLORS["accent"]).grid(
        row=0, column=0, padx=(10, 5), pady=8, sticky="w")
    pattern_entry = ctk.CTkEntry(pattern_frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                                 text_color=COLORS["green"], border_width=1, border_color=COLORS["border"],
                                 placeholder_text=r"e.g. \b\w+\b")
    pattern_entry.grid(row=0, column=1, padx=5, pady=8, sticky="ew")

    ctk.CTkLabel(pattern_frame, text="Flags:", font=FONTS["heading"], text_color=COLORS["accent"]).grid(
        row=1, column=0, padx=(10, 5), pady=8, sticky="w")

    flags_frame = ctk.CTkFrame(pattern_frame, fg_color="transparent")
    flags_frame.grid(row=1, column=1, padx=5, pady=8, sticky="w")

    flag_i = ctk.CTkCheckBox(flags_frame, text="i (ignore case)", font=FONTS["body"],
                              text_color=COLORS["text"], fg_color=COLORS["accent"],
                              hover_color=COLORS["green"])
    flag_i.pack(side="left", padx=(0, 10))
    flag_m = ctk.CTkCheckBox(flags_frame, text="m (multiline)", font=FONTS["body"],
                              text_color=COLORS["text"], fg_color=COLORS["accent"],
                              hover_color=COLORS["green"])
    flag_m.pack(side="left", padx=(0, 10))
    flag_s = ctk.CTkCheckBox(flags_frame, text="s (dotall)", font=FONTS["body"],
                              text_color=COLORS["text"], fg_color=COLORS["accent"],
                              hover_color=COLORS["green"])
    flag_s.pack(side="left")

    input_label = ctk.CTkLabel(frame, text="Test Text", font=FONTS["heading"], text_color=COLORS["accent"])
    input_label.pack(anchor="w", padx=15, pady=(5, 0))

    input_text = ctk.CTkTextbox(frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                                text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                                corner_radius=6, height=100)
    input_text.pack(fill="both", expand=True, padx=15, pady=(0, 5))

    def test_regex():
        pattern = pattern_entry.get()
        test_str = input_text.get("1.0", "end-1c")
        flags = 0
        if flag_i.get():
            flags |= re.IGNORECASE
        if flag_m.get():
            flags |= re.MULTILINE
        if flag_s.get():
            flags |= re.DOTALL

        result_box.configure(state="normal")
        result_box.delete("1.0", "end")

        if not pattern:
            result_box.insert("1.0", "Enter a regex pattern above.")
            result_box.configure(state="disabled")
            return

        try:
            compiled = re.compile(pattern, flags)
        except re.error as e:
            result_box.insert("1.0", f"Invalid regex:\n{e}")
            result_box.configure(state="disabled")
            return

        matches = list(compiled.finditer(test_str))
        if not matches:
            result_box.insert("1.0", "No matches found.")
            result_box.configure(state="disabled")
            return

        lines = [f"Matches found: {len(matches)}\n"]
        for i, m in enumerate(matches, 1):
            lines.append(f"  {i}: \"{m.group()}\" at position {m.start()}-{m.end()}")
            if m.groups():
                for gi, g in enumerate(m.groups(), 1):
                    lines.append(f"      Group {gi}: \"{g}\"")

        highlighted = test_str
        offset = 0
        for m in reversed(matches):
            start = m.start() + offset
            end = m.end() + offset
            highlighted = highlighted[:start] + f"[{m.group()}]" + highlighted[end:]
            offset += 2

        lines.append(f"\nHighlighted:\n{highlighted}")
        result_box.insert("1.0", "\n".join(lines))
        result_box.configure(state="disabled")

    test_btn = ctk.CTkButton(frame, text="Test Regex", font=FONTS["button"], fg_color=COLORS["accent"],
                             hover_color=COLORS["green"], text_color=COLORS["bg_dark"],
                             command=test_regex, height=32)
    test_btn.pack(pady=5)

    result_label = ctk.CTkLabel(frame, text="Results", font=FONTS["heading"], text_color=COLORS["accent"])
    result_label.pack(anchor="w", padx=15, pady=(5, 0))

    result_box = ctk.CTkTextbox(frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                                text_color=COLORS["green"], border_width=1, border_color=COLORS["border"],
                                corner_radius=6, state="disabled")
    result_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
