"""
Image Resizer Tool
Resize images by dimensions or percentage with aspect ratio lock.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os


def create_ui(frame, COLORS, FONTS):
    state = {
        "image": None,
        "path": "",
        "orig_w": 0,
        "orig_h": 0,
        "ratio": 1.0,
        "link_ratio": True,
    }

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
        state["orig_w"], state["orig_h"] = img.size
        state["ratio"] = state["orig_w"] / state["orig_h"] if state["orig_h"] else 1.0

        path_var.set(path)
        info_var.set(f"{state['orig_w']} x {state['orig_h']} px")
        w_entry.delete(0, "end")
        w_entry.insert(0, str(state["orig_w"]))
        h_entry.delete(0, "end")
        h_entry.insert(0, str(state["orig_h"]))
        pct_entry.delete(0, "end")
        pct_entry.insert(0, "100")
        preview_var.set(f"Output: {state['orig_w']} x {state['orig_h']} px")

    def on_width_change(*_):
        if not state["link_ratio"] or not state["image"]:
            return
        try:
            w = int(w_var.get())
            h = int(w / state["ratio"])
            h_var.set(str(h))
            update_preview()
        except (ValueError, ZeroDivisionError):
            pass

    def on_height_change(*_):
        if not state["link_ratio"] or not state["image"]:
            return
        try:
            h = int(h_var.get())
            w = int(h * state["ratio"])
            w_var.set(str(w))
            update_preview()
        except (ValueError, ZeroDivisionError):
            pass

    def on_pct_change(*_):
        if not state["image"]:
            return
        try:
            pct = float(pct_var.get())
            nw = int(state["orig_w"] * pct / 100)
            nh = int(state["orig_h"] * pct / 100)
            w_var.set(str(nw))
            h_var.set(str(nh))
            update_preview()
        except (ValueError, ZeroDivisionError):
            pass

    def update_preview():
        try:
            nw = int(w_var.get())
            nh = int(h_var.get())
            preview_var.set(f"Output: {nw} x {nh} px")
        except ValueError:
            preview_var.set("Output: ---")

    def toggle_link():
        state["link_ratio"] = not state["link_ratio"]
        link_var.set("Locked" if state["link_ratio"] else "Unlocked")

    def resize():
        if not state["image"]:
            messagebox.showwarning("Warning", "Select an image first.")
            return
        try:
            nw = int(w_var.get())
            nh = int(h_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid width or height.")
            return
        if nw <= 0 or nh <= 0:
            messagebox.showerror("Error", "Dimensions must be positive.")
            return
        try:
            resized = state["image"].resize((nw, nh), Image.LANCZOS)
        except Exception as e:
            messagebox.showerror("Error", f"Resize failed:\n{e}")
            return
        state["resized"] = resized
        preview_var.set(f"Output: {nw} x {nh} px")
        messagebox.showinfo("Done", f"Resized to {nw} x {nh}.")

    def save():
        resized = state.get("resized")
        if not resized:
            messagebox.showwarning("Warning", "Resize an image first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All", "*.*")],
        )
        if not path:
            return
        try:
            resized.save(path)
            messagebox.showinfo("Saved", f"Saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed:\n{e}")

    # --- Build UI ---
    frame.configure(fg_color=COLORS["bg_dark"])

    ctk.CTkLabel(frame, text="Image Resizer", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=(16, 4))
    ctk.CTkLabel(frame, text="Resize images by dimensions or percentage", font=FONTS["subtitle"], text_color=COLORS["text_dim"]).pack(pady=(0, 12))

    # Browse
    browse_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8)
    browse_frame.pack(fill="x", padx=16, pady=(0, 8))
    ctk.CTkButton(browse_frame, text="Browse", width=90, font=FONTS["button"],
                  fg_color=COLORS["accent"], hover_color=COLORS["green"], command=browse).pack(side="left", padx=8, pady=8)
    path_var = ctk.StringVar(value="No file selected")
    ctk.CTkLabel(browse_frame, textvariable=path_var, font=FONTS["mono_small"], text_color=COLORS["text_dim"], anchor="w").pack(side="left", fill="x", expand=True, padx=(0, 8))
    info_var = ctk.StringVar(value="")
    ctk.CTkLabel(browse_frame, textvariable=info_var, font=FONTS["body"], text_color=COLORS["yellow"]).pack(side="right", padx=8)

    # Dimensions
    dim_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8)
    dim_card.pack(fill="x", padx=16, pady=(0, 8))
    ctk.CTkLabel(dim_card, text="Dimensions", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=12, pady=(8, 4))

    inputs_row = ctk.CTkFrame(dim_card, fg_color="transparent")
    inputs_row.pack(fill="x", padx=12, pady=(0, 4))

    ctk.CTkLabel(inputs_row, text="Width", font=FONTS["body"], text_color=COLORS["text_dim"]).grid(row=0, column=0, padx=(0, 4))
    w_var = ctk.StringVar()
    w_entry = ctk.CTkEntry(inputs_row, textvariable=w_var, width=100, font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"])
    w_entry.grid(row=1, column=0, padx=(0, 8))

    link_var = ctk.StringVar(value="Locked")
    ctk.CTkButton(inputs_row, textvariable=link_var, width=70, font=FONTS["body"],
                  fg_color=COLORS["green"], text_color="#000000", command=toggle_link).grid(row=1, column=1, padx=4)

    ctk.CTkLabel(inputs_row, text="Height", font=FONTS["body"], text_color=COLORS["text_dim"]).grid(row=0, column=2, padx=(8, 4))
    h_var = ctk.StringVar()
    h_entry = ctk.CTkEntry(inputs_row, textvariable=h_var, width=100, font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"])
    h_entry.grid(row=1, column=2, padx=(8, 0))

    w_var.trace_add("write", on_width_change)
    h_var.trace_add("write", on_height_change)

    # Percentage
    pct_frame = ctk.CTkFrame(dim_card, fg_color="transparent")
    pct_frame.pack(fill="x", padx=12, pady=(4, 8))
    ctk.CTkLabel(pct_frame, text="Percentage", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(side="left")
    pct_var = ctk.StringVar()
    pct_entry = ctk.CTkEntry(pct_frame, textvariable=pct_var, width=80, font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"])
    pct_entry.pack(side="left", padx=(8, 4))
    ctk.CTkLabel(pct_frame, text="%", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(side="left")
    pct_var.trace_add("write", on_pct_change)

    # Preview
    preview_card = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=8)
    preview_card.pack(fill="x", padx=16, pady=(0, 8))
    preview_var = ctk.StringVar(value="Output: ---")
    ctk.CTkLabel(preview_card, textvariable=preview_var, font=FONTS["mono"], text_color=COLORS["green"]).pack(padx=12, pady=10)

    # Buttons
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=16, pady=(4, 16))
    ctk.CTkButton(btn_frame, text="Resize", font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=resize).pack(side="left", expand=True, fill="x", padx=(0, 4))
    ctk.CTkButton(btn_frame, text="Save", font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=save).pack(side="left", expand=True, fill="x", padx=(4, 0))
