"""
QR Code Generator Tool
Generate QR codes from text or URLs and save as PNG.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import io
import base64

try:
    import qrcode
except ImportError:
    qrcode = None


def create_ui(frame, COLORS, FONTS):
    state = {"qr_img": None}

    SIZES = {
        "Small (150x150)": 150,
        "Medium (300x300)": 300,
        "Large (500x500)": 500,
    }

    def generate():
        if qrcode is None:
            messagebox.showerror("Missing Dependency", "Install qrcode library:\npip install qrcode[pil]")
            return
        text = text_box.get("0.0", "end").strip()
        if not text:
            messagebox.showwarning("Warning", "Enter text or a URL.")
            return
        size_label = size_var.get()
        px = SIZES.get(size_label, 300)
        try:
            qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            img = img.resize((px, px), Image.LANCZOS)
            state["qr_img"] = img
            display(img)
        except Exception as e:
            messagebox.showerror("Error", f"QR generation failed:\n{e}")

    def display(img):
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        pil_img = Image.open(buf)
        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(min(pil_img.width, 280), min(pil_img.height, 280)))
        preview_label.configure(image=ctk_img, text="")
        preview_label._ctk_img = ctk_img

    def save():
        img = state.get("qr_img")
        if not img:
            messagebox.showwarning("Warning", "Generate a QR code first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("All", "*.*")],
        )
        if not path:
            return
        try:
            img.save(path)
            messagebox.showinfo("Saved", f"QR code saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed:\n{e}")

    # --- Build UI ---
    frame.configure(fg_color=COLORS["bg_dark"])

    ctk.CTkLabel(frame, text="QR Code Generator", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=(16, 4))
    ctk.CTkLabel(frame, text="Generate QR codes from text or URLs", font=FONTS["subtitle"], text_color=COLORS["text_dim"]).pack(pady=(0, 12))

    # Text input
    input_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8)
    input_card.pack(fill="x", padx=16, pady=(0, 8))
    ctk.CTkLabel(input_card, text="Text / URL", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=12, pady=(8, 4))
    text_box = ctk.CTkTextbox(input_card, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                              text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, height=60)
    text_box.pack(fill="x", padx=8, pady=(0, 8))

    # Size selector
    size_frame = ctk.CTkFrame(frame, fg_color="transparent")
    size_frame.pack(fill="x", padx=16, pady=(0, 8))
    ctk.CTkLabel(size_frame, text="Size", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(side="left")
    size_var = ctk.StringVar(value="Medium (300x300)")
    size_menu = ctk.CTkOptionMenu(size_frame, variable=size_var, values=list(SIZES.keys()),
                                  font=FONTS["body"], fg_color=COLORS["bg_input"], button_color=COLORS["accent"],
                                  button_hover_color=COLORS["green"], dropdown_fg_color=COLORS["bg_card"])
    size_menu.pack(side="left", padx=(8, 0))

    # Generate button
    ctk.CTkButton(frame, text="Generate", font=FONTS["button"], fg_color=COLORS["accent"],
                  hover_color=COLORS["green"], command=generate).pack(fill="x", padx=16, pady=(0, 8))

    # Preview
    preview_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8)
    preview_card.pack(fill="both", expand=True, padx=16, pady=(0, 8))
    preview_label = ctk.CTkLabel(preview_card, text="QR code will appear here", font=FONTS["body"],
                                 text_color=COLORS["text_dim"], fg_color=COLORS["bg_input"], corner_radius=6)
    preview_label.pack(fill="both", expand=True, padx=8, pady=8)

    # Save button
    ctk.CTkButton(frame, text="Save as PNG", font=FONTS["button"], fg_color=COLORS["accent"],
                  hover_color=COLORS["green"], command=save).pack(fill="x", padx=16, pady=(0, 16))
