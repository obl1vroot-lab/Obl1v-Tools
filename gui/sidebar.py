#!/usr/bin/env python3
"""
Obl1v-Tools - Sidebar Navigation
"""

import customtkinter as ctk
from gui.styles import COLORS, FONTS, SIDEBAR_WIDTH

TOOL_REGISTRY = {
    "PASSWORD": [
        ("Password Generator", "password_gen"),
        ("Password Strength", "password_strength"),
        ("Password Hasher", "password_hasher"),
        ("Breach Checker", "breach_checker"),
        ("Passphrase Generator", "passphrase_gen"),
    ],
    "HASHING & ENCODING": [
        ("Hash Calculator", "hash_calc"),
        ("Base64 Tool", "base64_tool"),
        ("URL Codec", "url_codec"),
        ("Hex Codec", "hex_codec"),
        ("Caesar Cipher", "caesar_cipher"),
    ],
    "NETWORK": [
        ("IP Lookup", "ip_lookup"),
        ("DNS Lookup", "dns_lookup"),
        ("Port Scanner", "port_scanner"),
        ("Ping Tool", "ping_tool"),
        ("WHOIS Lookup", "whois_lookup"),
    ],
    "FILES": [
        ("File Hasher", "file_hasher"),
        ("Duplicate Finder", "duplicate_finder"),
        ("File Info", "file_info"),
        ("Bulk Renamer", "bulk_renamer"),
        ("File Shredder", "file_shredder"),
    ],
    "TEXT": [
        ("Word Counter", "word_counter"),
        ("Case Converter", "case_converter"),
        ("Lorem Ipsum Generator", "lorem_gen"),
        ("Regex Tester", "regex_tester"),
        ("Text Diff", "text_diff"),
    ],
    "IMAGE": [
        ("Image Resizer", "image_resizer"),
        ("Image to Base64", "image_to_base64"),
        ("QR Code Generator", "qr_generator"),
    ],
    "SECURITY": [
        ("Subdomain Finder", "subdomain_finder"),
        ("Email Header Analyzer", "email_header"),
        ("URL Scanner", "url_scanner"),
        ("Service Identifier", "service_id"),
    ],
    "SYSTEM": [
        ("System Info", "sys_info"),
        ("Process List", "process_list"),
        ("Disk Usage", "disk_usage"),
        ("Net Connections", "net_connections"),
    ],
    "UTILITY": [
        ("Timestamp Converter", "timestamp_conv"),
        ("UUID Generator", "uuid_gen"),
        ("JSON Formatter", "json_formatter"),
        ("Color Picker", "color_picker"),
    ],
}


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_tool_select=None, **kwargs):
        super().__init__(master, width=SIDEBAR_WIDTH, fg_color=COLORS["sidebar_bg"],
                         corner_radius=0, **kwargs)
        self.on_tool_select = on_tool_select
        self.tool_buttons = {}
        self.active_tool = None
        self.pack_propagate(False)
        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header, text="Obl1v Tools",
            font=FONTS["title"], text_color=COLORS["accent"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            header, text="v1.0.0  |  40 Tools",
            font=FONTS["status"], text_color=COLORS["text_dim"]
        ).pack(anchor="w")

        sep = ctk.CTkFrame(self, fg_color=COLORS["border"], height=1)
        sep.pack(fill="x", padx=15, pady=(10, 5))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self._filter_tools)
        search = ctk.CTkEntry(
            self, placeholder_text="Search tools...",
            font=FONTS["body"], fg_color=COLORS["bg_input"],
            text_color=COLORS["text"], border_color=COLORS["border"],
            textvariable=self.search_var, height=32
        )
        search.pack(fill="x", padx=15, pady=(0, 10))

        scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent"]
        )
        scroll.pack(fill="both", expand=True, padx=(5, 0))

        for category, tools in TOOL_REGISTRY.items():
            cat_frame = ctk.CTkFrame(scroll, fg_color="transparent")
            cat_frame.pack(fill="x", padx=10, pady=(8, 0))

            ctk.CTkLabel(
                cat_frame, text=category,
                font=FONTS["sidebar_category"], text_color=COLORS["accent"]
            ).pack(anchor="w", pady=(0, 3))

            for display_name, tool_id in tools:
                btn = ctk.CTkButton(
                    cat_frame, text=f"  {display_name}",
                    font=FONTS["sidebar_item"], fg_color="transparent",
                    text_color=COLORS["text_dim"], hover_color=COLORS["sidebar_hover"],
                    anchor="w", height=26, corner_radius=4,
                    command=lambda tid=tool_id, dn=display_name: self._select_tool(tid, dn)
                )
                btn.pack(fill="x", padx=(10, 0))
                self.tool_buttons[tool_id] = btn

    def _select_tool(self, tool_id, display_name):
        if self.active_tool and self.active_tool in self.tool_buttons:
            self.tool_buttons[self.active_tool].configure(
                fg_color="transparent", text_color=COLORS["text_dim"]
            )
        self.tool_buttons[tool_id].configure(
            fg_color=COLORS["sidebar_active"], text_color=COLORS["accent"]
        )
        self.active_tool = tool_id
        if self.on_tool_select:
            self.on_tool_select(tool_id, display_name)

    def _filter_tools(self, *args):
        query = self.search_var.get().lower()
        for tool_id, btn in self.tool_buttons.items():
            if query in btn.cget("text").lower():
                btn.pack(fill="x", padx=(10, 0))
            else:
                btn.pack_forget()
