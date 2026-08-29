"""Hash Calculator - Compute MD5, SHA1, SHA256, SHA512 hashes."""

import customtkinter as ctk
import hashlib


def create_ui(frame, COLORS, FONTS):
    hash_var = ctk.StringVar(value="SHA256")

    def calculate():
        text = input_box.get("1.0", "end-1c").encode("utf-8")
        algo = hash_var.get().lower().replace("sha", "sha")
        algo_map = {"md5": "md5", "sha1": "sha1", "sha256": "sha256", "sha512": "sha512"}
        if algo not in algo_map:
            return
        h = hashlib.new(algo_map[algo], text)
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", h.hexdigest().upper())
        output_box.configure(state="disabled")

    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(output_box.get("1.0", "end-1c"))

    ctk.CTkLabel(frame, text="Hash Calculator", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w", padx=10, pady=(10, 5))

    input_box = ctk.CTkTextbox(frame, height=120, fg_color=COLORS["bg_input"], text_color=COLORS["text"], font=FONTS["mono"], border_width=1, border_color=COLORS["border"], corner_radius=6)
    input_box.pack(fill="x", padx=10, pady=(0, 8))

    radio_frame = ctk.CTkFrame(frame, fg_color="transparent")
    radio_frame.pack(anchor="w", padx=10, pady=(0, 8))
    for algo in ["MD5", "SHA1", "SHA256", "SHA512"]:
        ctk.CTkRadioButton(radio_frame, text=algo, variable=hash_var, value=algo, font=FONTS["body"], text_color=COLORS["text"], fg_color=COLORS["accent"], hover_color=COLORS["accent"]).pack(side="left", padx=(0, 12))

    ctk.CTkButton(frame, text="Calculate", command=calculate, fg_color=COLORS["accent"], hover_color=COLORS["green"], font=FONTS["button"], corner_radius=6).pack(fill="x", padx=10, pady=(0, 8))

    output_box = ctk.CTkTextbox(frame, height=50, fg_color=COLORS["bg_input"], text_color=COLORS["green"], font=FONTS["mono"], border_width=1, border_color=COLORS["border"], corner_radius=6, state="disabled")
    output_box.pack(fill="x", padx=10, pady=(0, 5))

    ctk.CTkButton(frame, text="Copy", command=copy, fg_color=COLORS["bg_card"], hover_color=COLORS["border"], text_color=COLORS["text"], font=FONTS["button"], corner_radius=6, height=30).pack(padx=10, pady=(0, 10))
