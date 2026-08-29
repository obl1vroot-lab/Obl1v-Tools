#!/usr/bin/env python3
"""
Obl1v-Tools - Main Application Window
"""

import customtkinter as ctk
from gui.styles import COLORS, FONTS, APP_NAME, APP_VERSION
from gui.sidebar import Sidebar


class ToolPlaceholder(ctk.CTkFrame):
    def __init__(self, master, tool_name, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_card"], corner_radius=10, **kwargs)
        ctk.CTkLabel(
            self, text=tool_name,
            font=FONTS["title"], text_color=COLORS["text"]
        ).pack(expand=True)
        ctk.CTkLabel(
            self, text="Select a tool from the sidebar",
            font=FONTS["body"], text_color=COLORS["text_dim"]
        ).pack(expand=True)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("1100x700")
        self.minsize(900, 600)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=COLORS["bg_dark"])

        self.tool_modules = {}
        self._load_tool_modules()

        self.sidebar = Sidebar(self, on_tool_select=self._on_tool_select)
        self.sidebar.pack(side="left", fill="y")

        sep = ctk.CTkFrame(self, fg_color=COLORS["border"], width=1)
        sep.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"], corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

        self.status_bar = ctk.CTkFrame(self, fg_color=COLORS["bg_card"], height=28)
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_bar, text="Ready",
            font=FONTS["status"], text_color=COLORS["text_dim"]
        )
        self.status_label.pack(side="left", padx=10)

        ctk.CTkLabel(
            self.status_bar, text=f"40 tools loaded",
            font=FONTS["status"], text_color=COLORS["text_dim"]
        ).pack(side="right", padx=10)

        self._show_welcome()

    def _load_tool_modules(self):
        from tools.password import generator, strength, hasher, breach_checker, passphrase
        from tools.hashing import hash_calc, base64_tool, url_codec, hex_codec, caesar_cipher
        from tools.network import ip_lookup, dns_lookup, port_scanner, ping_tool, whois_lookup
        from tools.files import file_hasher, duplicate_finder, file_info, bulk_renamer, file_shredder
        from tools.text import word_counter, case_converter, lorem_generator, regex_tester, text_diff
        from tools.image import image_resizer, image_to_base64, qr_generator
        from tools.security import subdomain_finder, email_header, url_scanner, service_identifier
        from tools.system import sys_info, process_list, disk_usage, net_connections
        from tools.utility import timestamp_converter, uuid_generator, json_formatter, color_picker

        self.tool_modules = {
            "password_gen": generator,
            "password_strength": strength,
            "password_hasher": hasher,
            "breach_checker": breach_checker,
            "passphrase_gen": passphrase,
            "hash_calc": hash_calc,
            "base64_tool": base64_tool,
            "url_codec": url_codec,
            "hex_codec": hex_codec,
            "caesar_cipher": caesar_cipher,
            "ip_lookup": ip_lookup,
            "dns_lookup": dns_lookup,
            "port_scanner": port_scanner,
            "ping_tool": ping_tool,
            "whois_lookup": whois_lookup,
            "file_hasher": file_hasher,
            "duplicate_finder": duplicate_finder,
            "file_info": file_info,
            "bulk_renamer": bulk_renamer,
            "file_shredder": file_shredder,
            "word_counter": word_counter,
            "case_converter": case_converter,
            "lorem_gen": lorem_generator,
            "regex_tester": regex_tester,
            "text_diff": text_diff,
            "image_resizer": image_resizer,
            "image_to_base64": image_to_base64,
            "qr_generator": qr_generator,
            "subdomain_finder": subdomain_finder,
            "email_header": email_header,
            "url_scanner": url_scanner,
            "service_id": service_identifier,
            "sys_info": sys_info,
            "process_list": process_list,
            "disk_usage": disk_usage,
            "net_connections": net_connections,
            "timestamp_conv": timestamp_converter,
            "uuid_gen": uuid_generator,
            "json_formatter": json_formatter,
            "color_picker": color_picker,
        }

    def _on_tool_select(self, tool_id, tool_name):
        for widget in self.content.winfo_children():
            widget.destroy()

        mod = self.tool_modules.get(tool_id)
        if mod and hasattr(mod, "create_ui"):
            panel = ctk.CTkFrame(self.content, fg_color=COLORS["bg_dark"])
            panel.pack(fill="both", expand=True, padx=15, pady=15)
            mod.create_ui(panel, COLORS, FONTS)
            self.status_label.configure(text=f"Active: {tool_name}")
        else:
            ToolPlaceholder(self.content, tool_name).pack(fill="both", expand=True)
            self.status_label.configure(text=f"Active: {tool_name}")

    def _show_welcome(self):
        frame = ctk.CTkFrame(self.content, fg_color=COLORS["bg_card"], corner_radius=10)
        frame.pack(expand=True, fill="both", padx=30, pady=30)

        ctk.CTkLabel(
            frame, text="Obl1v Tools",
            font=("Consolas", 32, "bold"), text_color=COLORS["accent"]
        ).pack(pady=(60, 5))

        ctk.CTkLabel(
            frame, text="Multi-Tool Suite  |  40 Tools",
            font=FONTS["subtitle"], text_color=COLORS["text_dim"]
        ).pack(pady=(0, 30))

        ctk.CTkLabel(
            frame, text="Select a tool from the sidebar to get started",
            font=FONTS["body"], text_color=COLORS["text_dim"]
        ).pack()

        categories = [
            "Password Tools", "Hashing & Encoding", "Network Tools",
            "File Tools", "Text Tools", "Image Tools",
            "Security Tools", "System Tools", "Utility Tools"
        ]

        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(pady=30)

        for i, cat in enumerate(categories):
            lbl = ctk.CTkLabel(
                grid, text=f"  {cat}",
                font=FONTS["mono_small"], text_color=COLORS["text"],
                anchor="w", width=200
            )
            lbl.grid(row=i // 3, column=i % 3, padx=15, pady=6, sticky="w")
