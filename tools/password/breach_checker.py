"""Breach Checker - Check if a password has been exposed in known data breaches (HIBP)."""

import customtkinter as ctk
import secrets
import string
import hashlib

try:
    import requests
except ImportError:
    requests = None


def _check_breach(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"Add-Padding": "true"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        for line in resp.text.splitlines():
            hash_suffix, count = line.split(":")
            if hash_suffix.strip() == suffix:
                return int(count.strip())
        return 0
    except Exception as e:
        raise RuntimeError(f"API request failed: {e}")


def create_ui(frame, COLORS, FONTS):
    input_var = ctk.StringVar()
    result_var = ctk.StringVar(value="")
    count_var = ctk.StringVar(value="")
    status_var = ctk.StringVar(value="")

    ctk.CTkLabel(frame, text="Breach Checker", font=FONTS["heading"],
                 text_color=COLORS["text"], anchor="w").pack(fill="x", padx=16, pady=(16, 8))

    if requests is None:
        ctk.CTkLabel(frame, text="Install requests: pip install requests",
                     font=FONTS["body"], text_color=COLORS["yellow"]).pack(fill="x", padx=16, pady=(0, 8))

    ctk.CTkLabel(frame, text="Uses Have I Been Pwned (k-anonymity). Your password never leaves this device.",
                 font=FONTS["body"], text_color=COLORS["text_dim"], wraplength=400).pack(fill="x", padx=16, pady=(0, 8))

    inp_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    inp_frame.pack(fill="x", padx=16, pady=(0, 8))

    ctk.CTkEntry(inp_frame, textvariable=input_var, placeholder_text="Enter password to check...",
                 font=FONTS["mono"], fg_color=COLORS["bg_input"], text_color=COLORS["text"],
                 border_color=COLORS["border"], height=36).pack(fill="x", padx=12, pady=10)

    def check():
        pw = input_var.get()
        if not pw:
            status_var.set("Enter a password first")
            return
        if requests is None:
            status_var.set("requests module not installed")
            return
        status_var.set("Checking...")
        frame.update_idletasks()
        try:
            count = _check_breach(pw)
            if count > 0:
                result_var.set(f"Found in {count:,} breaches!")
                count_var.set(COLORS["red"])
            else:
                result_var.set("Not found in any known breaches")
                count_var.set(COLORS["green"])
            status_var.set(f"Count: {count:,}")
        except RuntimeError as e:
            result_var.set(str(e))
            count_var.set(COLORS["yellow"])
            status_var.set("")

    ctk.CTkButton(frame, text="Check Breaches", font=FONTS["button"], fg_color=COLORS["accent"],
                  hover_color=COLORS["green"], command=check).pack(fill="x", padx=16, pady=(0, 8))

    result_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    result_frame.pack(fill="x", padx=16, pady=(0, 16))

    ctk.CTkLabel(result_frame, textvariable=result_var, font=FONTS["heading"],
                 text_color=COLORS["text"], anchor="w").pack(fill="x", padx=12, pady=(12, 4))

    ctk.CTkLabel(result_frame, textvariable=status_var, font=FONTS["mono_small"],
                 text_color=COLORS["text_dim"], anchor="w").pack(fill="x", padx=12, pady=(0, 12))
