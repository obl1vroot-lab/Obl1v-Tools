"""Caesar Cipher / ROT13 - Shift-based text encryption and decryption."""

import customtkinter as ctk


def create_ui(frame, COLORS, FONTS):
    mode_var = ctk.StringVar(value="Encrypt")
    shift_var = ctk.IntVar(value=3)

    def caesar(text, shift, decrypt=False):
        if decrypt:
            shift = -shift
        result = []
        for ch in text:
            if ch.isalpha():
                base = ord("A") if ch.isupper() else ord("a")
                result.append(chr((ord(ch) - base + shift) % 26 + base))
            else:
                result.append(ch)
        return "".join(result)

    def process():
        text = input_box.get("1.0", "end-1c")
        shift = shift_var.get()
        decrypt = mode_var.get() == "Decrypt"
        result = caesar(text, shift, decrypt)
        show_output(result)

    def rot13():
        text = input_box.get("1.0", "end-1c")
        result = caesar(text, 13)
        show_output(result)

    def show_output(text):
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", text)
        output_box.configure(state="disabled")

    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(output_box.get("1.0", "end-1c"))

    ctk.CTkLabel(frame, text="Caesar Cipher / ROT13", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w", padx=10, pady=(10, 5))

    input_box = ctk.CTkTextbox(frame, height=100, fg_color=COLORS["bg_input"], text_color=COLORS["text"], font=FONTS["mono"], border_width=1, border_color=COLORS["border"], corner_radius=6)
    input_box.pack(fill="x", padx=10, pady=(0, 8))

    shift_frame = ctk.CTkFrame(frame, fg_color="transparent")
    shift_frame.pack(fill="x", padx=10, pady=(0, 5))
    ctk.CTkLabel(shift_frame, text="Shift:", font=FONTS["body"], text_color=COLORS["text"]).pack(side="left")
    shift_label = ctk.CTkLabel(shift_frame, text="3", font=FONTS["mono"], text_color=COLORS["accent"], width=30)
    shift_label.pack(side="right")

    def on_shift(val):
        shift_label.configure(text=str(int(float(val))))

    ctk.CTkSlider(shift_frame, from_=0, to=25, variable=shift_var, command=on_shift, progress_color=COLORS["accent"], button_color=COLORS["accent"], button_hover_color=COLORS["green"], width=200).pack(side="left", padx=(10, 10))

    mode_frame = ctk.CTkFrame(frame, fg_color="transparent")
    mode_frame.pack(anchor="w", padx=10, pady=(0, 8))
    ctk.CTkRadioButton(mode_frame, text="Encrypt", variable=mode_var, value="Encrypt", font=FONTS["body"], text_color=COLORS["text"], fg_color=COLORS["accent"], hover_color=COLORS["accent"]).pack(side="left", padx=(0, 12))
    ctk.CTkRadioButton(mode_frame, text="Decrypt", variable=mode_var, value="Decrypt", font=FONTS["body"], text_color=COLORS["text"], fg_color=COLORS["accent"], hover_color=COLORS["accent"]).pack(side="left")

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=10, pady=(0, 8))
    ctk.CTkButton(btn_frame, text="Process", command=process, fg_color=COLORS["accent"], hover_color=COLORS["green"], font=FONTS["button"], corner_radius=6).pack(side="left", expand=True, fill="x", padx=(0, 4))
    ctk.CTkButton(btn_frame, text="ROT13", command=rot13, fg_color=COLORS["yellow"], hover_color=COLORS["green"], text_color="#000000", font=FONTS["button"], corner_radius=6).pack(side="left", expand=True, fill="x", padx=(4, 0))

    output_box = ctk.CTkTextbox(frame, height=100, fg_color=COLORS["bg_input"], text_color=COLORS["green"], font=FONTS["mono"], border_width=1, border_color=COLORS["border"], corner_radius=6, state="disabled")
    output_box.pack(fill="x", padx=10, pady=(0, 5))

    ctk.CTkButton(frame, text="Copy", command=copy, fg_color=COLORS["bg_card"], hover_color=COLORS["border"], text_color=COLORS["text"], font=FONTS["button"], corner_radius=6, height=30).pack(padx=10, pady=(0, 10))
