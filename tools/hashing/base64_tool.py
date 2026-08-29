"""Base64 Encoder/Decoder - Encode and decode Base64 strings."""

import customtkinter as ctk
import base64


def create_ui(frame, COLORS, FONTS):
    def encode():
        text = input_box.get("1.0", "end-1c")
        try:
            result = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            show_output(result)
        except Exception as e:
            show_output(f"Error: {e}")

    def decode():
        text = input_box.get("1.0", "end-1c").strip()
        try:
            result = base64.b64decode(text.encode("utf-8")).decode("utf-8")
            show_output(result)
        except Exception:
            show_output("Error: Invalid Base64 string")

    def show_output(text):
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", text)
        output_box.configure(state="disabled")

    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(output_box.get("1.0", "end-1c"))

    ctk.CTkLabel(frame, text="Base64 Encoder / Decoder", font=FONTS["title"], text_color=COLORS["text"]).pack(anchor="w", padx=10, pady=(10, 5))

    input_box = ctk.CTkTextbox(frame, height=120, fg_color=COLORS["bg_input"], text_color=COLORS["text"], font=FONTS["mono"], border_width=1, border_color=COLORS["border"], corner_radius=6)
    input_box.pack(fill="x", padx=10, pady=(0, 8))

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=10, pady=(0, 8))
    ctk.CTkButton(btn_frame, text="Encode", command=encode, fg_color=COLORS["accent"], hover_color=COLORS["green"], font=FONTS["button"], corner_radius=6).pack(side="left", expand=True, fill="x", padx=(0, 4))
    ctk.CTkButton(btn_frame, text="Decode", command=decode, fg_color=COLORS["accent"], hover_color=COLORS["green"], font=FONTS["button"], corner_radius=6).pack(side="left", expand=True, fill="x", padx=(4, 0))

    output_box = ctk.CTkTextbox(frame, height=100, fg_color=COLORS["bg_input"], text_color=COLORS["green"], font=FONTS["mono"], border_width=1, border_color=COLORS["border"], corner_radius=6, state="disabled")
    output_box.pack(fill="x", padx=10, pady=(0, 5))

    ctk.CTkButton(frame, text="Copy", command=copy, fg_color=COLORS["bg_card"], hover_color=COLORS["border"], text_color=COLORS["text"], font=FONTS["button"], corner_radius=6, height=30).pack(padx=10, pady=(0, 10))
