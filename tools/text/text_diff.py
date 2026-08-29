"""Text Diff Tool - Compare two texts and highlight differences line by line."""

import customtkinter as ctk
import re
import random


def create_ui(frame, COLORS, FONTS):
    frame.configure(fg_color=COLORS["bg_dark"])

    header = ctk.CTkLabel(frame, text="Text Diff Tool", font=FONTS["title"], text_color=COLORS["text"])
    header.pack(pady=(15, 10))

    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(fill="both", expand=True, padx=15, pady=(0, 5))
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=1)

    left_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
    left_frame.grid(row=0, column=0, padx=(0, 3), sticky="nsew")
    ctk.CTkLabel(left_frame, text="Original", font=FONTS["heading"], text_color=COLORS["accent"]).pack(anchor="w")
    left_text = ctk.CTkTextbox(left_frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                               text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                               corner_radius=6)
    left_text.pack(fill="both", expand=True)

    right_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
    right_frame.grid(row=0, column=1, padx=(3, 0), sticky="nsew")
    ctk.CTkLabel(right_frame, text="Modified", font=FONTS["heading"], text_color=COLORS["accent"]).pack(anchor="w")
    right_text = ctk.CTkTextbox(right_frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                                text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                                corner_radius=6)
    right_text.pack(fill="both", expand=True)

    def compare():
        left_lines = left_text.get("1.0", "end-1c").split("\n")
        right_lines = right_text.get("1.0", "end-1c").split("\n")

        max_lines = max(len(left_lines), len(right_lines))
        left_lines.extend([""] * (max_lines - len(left_lines)))
        right_lines.extend([""] * (max_lines - len(right_lines)))

        results = []
        added = removed = unchanged = 0

        for i in range(max_lines):
            l, r = left_lines[i], right_lines[i]
            num = f"{i + 1:>3}"
            if l == r:
                results.append(f"  {num}  |  {l}")
                unchanged += 1
            else:
                if l:
                    results.append(f"- {num}  |  {l}")
                    removed += 1
                if r:
                    results.append(f"+ {num}  |  {r}")
                    added += 1

        summary = f"Summary: {added} added, {removed} removed, {unchanged} unchanged\n"
        summary += "-" * 50 + "\n"
        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("1.0", summary + "\n".join(results))
        output.configure(state="disabled")

    compare_btn = ctk.CTkButton(frame, text="Compare", font=FONTS["button"], fg_color=COLORS["accent"],
                                hover_color=COLORS["green"], text_color=COLORS["bg_dark"],
                                command=compare, height=32)
    compare_btn.pack(pady=5)

    output_label = ctk.CTkLabel(frame, text="Differences", font=FONTS["heading"], text_color=COLORS["accent"])
    output_label.pack(anchor="w", padx=15, pady=(5, 0))

    output = ctk.CTkTextbox(frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                            text_color=COLORS["text"], border_width=1, border_color=COLORS["border"],
                            corner_radius=6, state="disabled")
    output.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    compare()
