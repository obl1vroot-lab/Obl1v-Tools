"""
UUID Generator - Generate UUIDs in multiple formats and versions.

Supports v1 (time-based), v4 (random), and v5 (name-based) UUIDs
with configurable count, format options, and copy-to-clipboard.
"""

import customtkinter as ctk
from tkinter import messagebox
import uuid
import json
import time
from datetime import datetime


NAMESPACES = {
    "DNS": uuid.NAMESPACE_DNS,
    "URL": uuid.NAMESPACE_URL,
    "OID": uuid.NAMESPACE_OID,
    "X500": uuid.NAMESPACE_X500,
}


def create_ui(frame, COLORS, FONTS):
    """Build the UUID Generator GUI inside the given frame."""

    # --- Header ---
    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(20, 10))
    ctk.CTkLabel(header, text="UUID Generator", font=FONTS["title"], text_color=COLORS["accent"]).pack(anchor="w")
    ctk.CTkLabel(header, text="Generate UUIDs in various versions and formats", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w")

    content = ctk.CTkFrame(frame, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    # === Left: Controls ===
    controls = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"], width=320)
    controls.pack(side="left", fill="y", padx=(0, 8))
    controls.pack_propagate(False)

    ctk.CTkLabel(controls, text="Options", font=FONTS["heading"], text_color=COLORS["text"]).pack(anchor="w", padx=15, pady=(15, 10))

    # Version selector
    ctk.CTkLabel(controls, text="UUID Version:", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15)
    version_var = ctk.StringVar(value="v4")
    version_menu = ctk.CTkOptionMenu(controls, variable=version_var, values=["v1 (Time-based)", "v4 (Random)", "v5 (Name-based)"], font=FONTS["body"], fg_color=COLORS["bg_input"], button_color=COLORS["accent"], button_hover_color=COLORS["green"], dropdown_fg_color=COLORS["bg_card"], text_color=COLORS["text"])
    version_menu.pack(fill="x", padx=15, pady=(2, 10))

    # Namespace (for v5)
    ns_frame = ctk.CTkFrame(controls, fg_color="transparent")
    ns_frame.pack(fill="x", padx=15, pady=(0, 10))
    ctk.CTkLabel(ns_frame, text="Namespace (v5):", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w")
    namespace_var = ctk.StringVar(value="DNS")
    ns_menu = ctk.CTkOptionMenu(ns_frame, variable=namespace_var, values=list(NAMESPACES.keys()), font=FONTS["body"], fg_color=COLORS["bg_input"], button_color=COLORS["accent"], button_hover_color=COLORS["green"], dropdown_fg_color=COLORS["bg_card"], text_color=COLORS["text"])
    ns_menu.pack(fill="x", pady=(2, 0))

    # Name (for v5)
    name_frame = ctk.CTkFrame(controls, fg_color="transparent")
    name_frame.pack(fill="x", padx=15, pady=(0, 10))
    ctk.CTkLabel(name_frame, text="Name (v5):", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w")
    name_entry = ctk.CTkEntry(name_frame, placeholder_text="e.g. example.com", font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"])
    name_entry.pack(fill="x", pady=(2, 0))

    # Count
    ctk.CTkLabel(controls, text="Count (1-100):", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15)
    count_var = ctk.StringVar(value="1")
    count_entry = ctk.CTkEntry(controls, textvariable=count_var, font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"], width=80)
    count_entry.pack(anchor="w", padx=15, pady=(2, 10))

    # Format options
    ctk.CTkLabel(controls, text="Format:", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15)
    format_var = ctk.StringVar(value="standard")
    fmt_frame = ctk.CTkFrame(controls, fg_color="transparent")
    fmt_frame.pack(fill="x", padx=15, pady=(2, 10))
    for fmt_text, fmt_val in [("Standard", "standard"), ("Uppercase", "uppercase"), ("No Dashes", "nodash")]:
        ctk.CTkRadioButton(fmt_frame, text=fmt_text, variable=format_var, value=fmt_val, font=FONTS["body"], text_color=COLORS["text"], fg_color=COLORS["accent"], hover_color=COLORS["green"]).pack(anchor="w", pady=1)

    # Generate button
    ctk.CTkButton(controls, text="Generate", font=FONTS["button"], fg_color=COLORS["accent"], hover_color=COLORS["green"], command=lambda: generate_uuids()).pack(fill="x", padx=15, pady=(10, 15))

    # === Right: Output ===
    output_frame = ctk.CTkFrame(content, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border"])
    output_frame.pack(side="left", fill="both", expand=True)

    out_header = ctk.CTkFrame(output_frame, fg_color="transparent")
    out_header.pack(fill="x", padx=15, pady=(15, 5))
    ctk.CTkLabel(out_header, text="Generated UUIDs", font=FONTS["heading"], text_color=COLORS["text"]).pack(side="left")

    def copy_all():
        val = output_box.get("1.0", "end").strip()
        if val:
            frame.clipboard_clear()
            frame.clipboard_append(val)

    ctk.CTkButton(out_header, text="Copy All", width=80, font=FONTS["mono_small"], fg_color=COLORS["bg_input"], hover_color=COLORS["accent"], text_color=COLORS["text"], border_color=COLORS["border"], border_width=1, command=copy_all).pack(side="right")

    output_box = ctk.CTkTextbox(output_frame, font=FONTS["mono"], fg_color=COLORS["bg_input"], border_color=COLORS["border"], border_width=1, text_color=COLORS["text"])
    output_box.pack(fill="both", expand=True, padx=15, pady=(5, 15))

    def generate_uuids():
        version_str = version_var.get()
        count_str = count_var.get()
        fmt = format_var.get()

        try:
            count = int(count_str)
            if count < 1 or count > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Count", "Count must be an integer between 1 and 100.")
            return

        uuids = []
        for _ in range(count):
            try:
                if version_str.startswith("v1"):
                    u = uuid.uuid1()
                elif version_str.startswith("v4"):
                    u = uuid.uuid4()
                elif version_str.startswith("v5"):
                    ns_name = namespace_var.get()
                    name = name_entry.get().strip()
                    if not name:
                        messagebox.showerror("Input Required", "v5 requires a name value.")
                        return
                    u = uuid.uuid5(NAMESPACES[ns_name], name)
                else:
                    continue

                s = str(u)
                if fmt == "uppercase":
                    s = s.upper()
                elif fmt == "nodash":
                    s = s.replace("-", "")
                uuids.append(s)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate UUID: {e}")
                return

        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", "\n".join(uuids))
        output_box.configure(state="disabled")
