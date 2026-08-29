"""
Image to Base64 Tool
Convert images to Base64 strings and decode Base64 back to images.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import io
import base64


def create_ui(frame, COLORS, FONTS):
    state = {"image": None, "path": "", "base64_str": ""}

    def browse():
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tiff")]
        )
        if not path:
            return
        try:
            img = Image.open(path)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open image:\n{e}")
            return
        state["image"] = img
        state["path"] = path
        enc_var.set(f"{os.path.basename(path)}  |  {img.format or 'N/A'}  |  {img.size[0]}x{img.size[1]}")
        path_var.set(path)
        out_textbox.configure(state="normal")
        out_textbox.delete("0.0", "end")
        out_textbox.configure(state="disabled")

    def encode():
        img = state["image"]
        if not img:
            messagebox.showwarning("Warning", "Select an image first.")
            return
        buf = io.BytesIO()
        fmt = img.format or "PNG"
        img.save(buf, format=fmt)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        state["base64_str"] = b64
        if data_uri_var.get():
            mime = {"PNG": "image/png", "JPEG": "image/jpeg", "GIF": "image/gif", "BMP": "image/bmp"}.get(fmt, f"image/{fmt.lower()}")
            b64 = f"data:{mime};base64,{b64}"
        out_textbox.configure(state="normal")
        out_textbox.delete("0.0", "end")
        out_textbox.insert("0.0", b64)
        out_textbox.configure(state="disabled")

    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(state.get("base64_str", ""))
        messagebox.showinfo("Copied", "Base64 string copied to clipboard.")

    def decode():
        raw = out_textbox.get("0.0", "end").strip()
        if not raw:
            messagebox.showwarning("Warning", "No Base64 data to decode.")
            return
        if raw.startswith("data:"):
            raw = raw.split(",", 1)[1] if "," in raw else ""
        try:
            img_bytes = base64.b64decode(raw)
            img = Image.open(io.BytesIO(img_bytes))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Base64 data:\n{e}")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=f".{img.format.lower() if img.format else 'png'}",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All", "*.*")],
        )
        if path:
            try:
                img.save(path)
                messagebox.showinfo("Saved", f"Image saved to:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed:\n{e}")

    # --- Build UI ---
    frame.configure(fg_color=COLORS["bg_dark"])

    ctk.CTkLabel(frame, text="Image to Base64", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=(16, 4))
    ctk.CTkLabel(frame, text="Encode images to Base64 or decode Base64 to image", font=FONTS["subtitle"], text_color=COLORS["text_dim"]).pack(pady=(0, 12))

    # Browse
    browse_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8)
    browse_card.pack(fill="x", padx=16, pady=(0, 8))
    ctk.CTkButton(browse_card, text="Browse", width=90, font=FONTS["button"],
                  fg_color=COLORS["accent"], hover_color=COLORS["green"], command=browse).pack(side="left", padx=8, pady=8)
    path_var = ctk.StringVar(value="No file selected")
    ctk.CTkLabel(browse_card, textvariable=path_var, font=FONTS["mono_small"], text_color=COLORS["text_dim"], anchor="w").pack(side="left", fill="x", expand=True, padx=(0, 8))

    # Info
    info_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8)
    info_card.pack(fill="x", padx=16, pady=(0, 8))
    enc_var = ctk.StringVar(value="No image loaded")
    ctk.CTkLabel(info_card, textvariable=enc_var, font=FONTS["mono"], text_color=COLORS["yellow"]).pack(padx=12, pady=10)

    # Options
    opt_frame = ctk.CTkFrame(frame, fg_color="transparent")
    opt_frame.pack(fill="x", padx=16, pady=(0, 8))
    data_uri_var = ctk.BooleanVar(value=False)
    ctk.CTkCheckBox(opt_frame, text="Data URI format", variable=data_uri_var, font=FONTS["body"],
                    text_color=COLORS["text"], fg_color=COLORS["accent"], hover_color=COLORS["green"]).pack(side="left")

    # Output
    out_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8)
    out_card.pack(fill="both", expand=True, padx=16, pady=(0, 8))
    ctk.CTkLabel(out_card, text="Base64 Output", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=12, pady=(8, 4))
    out_textbox = ctk.CTkTextbox(out_card, font=FONTS["mono_small"], fg_color=COLORS["bg_input"],
                                 text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, height=120, state="disabled")
    out_textbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # Buttons
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=16, pady=(0, 16))
    ctk.CTkButton(btn_frame, text="Encode", font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=encode).pack(side="left", expand=True, fill="x", padx=(0, 4))
    ctk.CTkButton(btn_frame, text="Copy", font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=copy).pack(side="left", expand=True, fill="x", padx=4)
    ctk.CTkButton(btn_frame, text="Decode to Image", font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=decode).pack(side="left", expand=True, fill="x", padx=(4, 0))
