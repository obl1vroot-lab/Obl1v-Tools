"""Passphrase Generator - Generate memorable passphrases from a built-in word list."""

import customtkinter as ctk
import secrets
import string

WORD_LIST = [
    "about", "above", "absent", "accept", "across", "action", "actual", "adapt", "admit", "adult",
    "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert", "alien", "align",
    "alive", "alley", "allow", "alone", "along", "alter", "among", "angel", "anger", "angle",
    "angry", "anime", "ankle", "annex", "apart", "apple", "apply", "arena", "argue", "army",
    "arrow", "aside", "asset", "atlas", "audio", "avoid", "awake", "award", "aware", "babel",
    "badge", "badly", "bagel", "basic", "basis", "beach", "beard", "begin", "being", "below",
    "bench", "berry", "bible", "bikes", "birth", "blade", "blame", "blank", "blast", "blaze",
    "bleed", "blend", "bless", "blind", "block", "blood", "bloom", "board", "bonus", "booth",
    "bound", "brain", "brand", "brave", "bread", "break", "brick", "brief", "bring", "broad",
    "brook", "broom", "brush", "build", "burst", "buyer", "cabin", "cable", "camel", "candy",
    "cards", "cargo", "carry", "catch", "cause", "cease", "chain", "chair", "chaos", "charm",
    "chart", "chase", "cheap", "check", "chess", "chest", "chief", "child", "china", "chord",
    "chunk", "civic", "civil", "claim", "clash", "class", "clean", "clear", "climb", "cling",
    "clock", "clone", "close", "cloth", "cloud", "coach", "coast", "color", "comet", "comic",
    "coral", "could", "count", "court", "cover", "crack", "craft", "crane", "crash", "crawl",
    "crazy", "cream", "crest", "crime", "crisp", "cross", "crowd", "crown", "cruel", "crush",
    "curve", "cycle", "daily", "dance", "debug", "decay", "delay", "delta", "dense", "depth",
    "derby", "desk", "dev", "devil", "diary", "dirty", "disco", "ditch", "dizzy", "dodge",
    "doubt", "dozen", "draft", "drain", "drake", "drama", "dream", "dress", "drift", "drill",
    "drink", "drive", "drown", "eager", "early", "earth", "easel", "eight", "elder", "elite",
    "ember", "empty", "enemy", "enjoy", "enter", "entry", "equal", "error", "essay", "event",
    "every", "exact", "exile", "exist", "extra", "fable", "faith", "false", "fancy", "fatal",
    "fault", "feast", "fence", "ferry", "fiber", "field", "final", "first", "flame", "flash",
    "fleet", "flesh", "float", "flood", "floor", "flora", "flour", "fluid", "flush", "focal",
    "focus", "force", "forge", "found", "frame", "frank", "fraud", "fresh", "front", "frost",
    "froze", "fruit", "fully", "funny", "gamer", "ghost", "giant", "given", "glad", "gland",
    "glass", "globe", "glory", "going", "grace", "grade", "grain", "grand", "grant", "grape",
    "graph", "grasp", "grass", "grave", "great", "greed", "green", "greet", "grief", "grind",
    "grips", "gross", "group", "grove", "grown", "guard", "guess", "guest", "guide", "guild",
    "guilt", "habit", "happy", "harsh", "hasty", "haunt", "haven", "heart", "heavy", "hedge",
    "hence", "herbs", "hobby", "honey", "honor", "horse", "hotel", "house", "human", "humor",
    "hurry", "ideal", "image", "imply", "index", "inner", "input", "irony", "ivory", "jewel",
    "joint", "joker", "judge", "juice", "juicy", "jumbo", "jumps", "karma", "kayak", "kebab",
    "knack", "kneel", "knife", "knock", "label", "lance", "large", "laser", "later", "laugh",
    "layer", "learn", "lease", "leave", "legal", "lemon", "level", "lever", "light", "limit",
    "linen", "liver", "lobby", "local", "logic", "login", "loose", "lover", "lower", "loyal",
    "lucky", "lunar", "lunch", "lyric", "magic", "major", "maker", "manga", "manor", "march",
    "marry", "match", "maybe", "mayor", "medal", "media", "melon", "merge", "merit", "merry",
    "metal", "meter", "midst", "might", "mimic", "minor", "minus", "mixer", "model", "money",
    "month", "moral", "motor", "mount", "mouse", "mouth", "movie", "muddy", "music", "naval",
    "nerve", "never", "night", "noble", "noise", "north", "noted", "novel", "nurse", "ocean",
    "offer", "onset", "opera", "orbit", "order", "organ", "other", "outer", "oxide", "ozone",
    "paint", "panel", "panic", "paper", "party", "pasta", "patch", "pause", "peace", "peach",
    "pearl", "pedal", "penny", "perch", "phase", "phone", "photo", "piano", "piece", "pilot",
    "pinch", "pitch", "pixel", "pizza", "place", "plain", "plane", "plant", "plate", "plaza",
    "plead", "pluck", "plumb", "point", "polar", "pound", "power", "press", "price", "pride",
    "prime", "print", "prior", "prize", "proof", "proud", "prove", "proxy", "pulse", "pump",
    "punch", "pupil", "purse", "queen", "quest", "quick", "quiet", "quite", "quota", "quote",
    "radar", "radio", "raise", "rally", "ranch", "range", "rapid", "ratio", "reach", "react",
    "realm", "rebel", "refer", "reign", "relax", "relay", "renal", "renew", "reply", "rider",
    "ridge", "rifle", "right", "rigid", "risky", "rival", "river", "robot", "rocky", "rouge",
    "rough", "round", "route", "royal", "rugby", "ruler", "rural", "saint", "salad", "sauce",
    "scale", "scare", "scene", "scope", "score", "scout", "scrap", "sense", "serve", "seven",
    "shade", "shake", "shall", "shame", "shape", "share", "shark", "sharp", "shave", "shelf",
    "shell", "shift", "shine", "shirt", "shock", "shore", "short", "shout", "shown", "sight",
    "since", "sixth", "sixty", "skate", "skill", "skull", "slash", "slave", "sleep", "slice",
    "slide", "slope", "small", "smart", "smell", "smile", "smoke", "snake", "solar", "solid",
    "solve", "sorry", "sound", "south", "space", "spare", "speak", "speed", "spell", "spend",
    "spice", "spine", "spite", "split", "spoke", "sport", "spray", "squad", "stack", "staff",
    "stage", "stain", "stake", "stale", "stalk", "stall", "stamp", "stand", "stare", "stark",
    "start", "state", "steal", "steam", "steel", "steep", "steer", "stern", "stick", "still",
    "stock", "stone", "stood", "store", "storm", "story", "stove", "strap", "straw", "strip",
    "stuck", "study", "stuff", "style", "sugar", "suite", "super", "surge", "swamp", "swarm",
    "swear", "sweet", "swept", "swift", "swing", "sword", "syrup", "table", "taste", "teach",
    "tempo", "tense", "thank", "theft", "theme", "there", "thick", "thing", "think", "third",
    "thorn", "those", "three", "threw", "throw", "thumb", "tidal", "tiger", "tight", "timer",
    "tired", "title", "toast", "today", "token", "total", "touch", "tough", "towel", "tower",
    "toxic", "trace", "track", "trade", "trail", "train", "trait", "trash", "treat", "trend",
    "trial", "tribe", "trick", "troop", "truck", "truly", "trump", "trunk", "trust", "truth",
    "tumor", "tuner", "twice", "twist", "ultra", "under", "union", "unity", "until", "upper",
    "upset", "urban", "usage", "usual", "utter", "vague", "valid", "value", "valve", "vapor",
    "venue", "verse", "vigor", "vinyl", "viral", "virus", "visit", "vista", "vital", "vivid",
    "vocal", "vodka", "voice", "voter", "vowel", "wages", "waste", "watch", "water", "weary",
    "weird", "whale", "wheat", "wheel", "where", "which", "while", "white", "whole", "whose",
    "width", "witch", "woman", "world", "worry", "worse", "worst", "worth", "would", "wound",
    "wrist", "write", "wrong", "wrote", "yacht", "yield", "young", "yours", "youth", "zebra",
]


def create_ui(frame, COLORS, FONTS):
    count_var = ctk.IntVar(value=4)
    sep_var = ctk.StringVar(value="-")
    capitalize_var = ctk.BooleanVar(value=False)
    output_var = ctk.StringVar()

    ctk.CTkLabel(frame, text="Passphrase Generator", font=FONTS["heading"],
                 text_color=COLORS["text"], anchor="w").pack(fill="x", padx=16, pady=(16, 8))

    opt_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    opt_frame.pack(fill="x", padx=16, pady=(0, 8))

    row1 = ctk.CTkFrame(opt_frame, fg_color="transparent")
    row1.pack(fill="x", padx=12, pady=(10, 4))
    ctk.CTkLabel(row1, text="Words", font=FONTS["body"], text_color=COLORS["text"]).pack(side="left")
    ctk.CTkLabel(row1, textvariable=count_var, font=FONTS["mono"], text_color=COLORS["accent"],
                 width=24).pack(side="right")
    ctk.CTkSlider(row1, from_=3, to=8, variable=count_var,
                  button_color=COLORS["accent"], button_hover_color=COLORS["accent"],
                  fg_color=COLORS["bg_input"], progress_color=COLORS["accent"]
                  ).pack(side="right", fill="x", expand=True, padx=8)

    row2 = ctk.CTkFrame(opt_frame, fg_color="transparent")
    row2.pack(fill="x", padx=12, pady=(4, 4))
    ctk.CTkLabel(row2, text="Separator", font=FONTS["body"], text_color=COLORS["text"]).pack(side="left")
    ctk.CTkOptionMenu(row2, variable=sep_var, values=["-", "_", ".", " "],
                      fg_color=COLORS["bg_input"], button_color=COLORS["accent"],
                      button_hover_color=COLORS["green"], font=FONTS["body"], width=80,
                      dropdown_fg_color=COLORS["bg_card"]).pack(side="right")

    row3 = ctk.CTkFrame(opt_frame, fg_color="transparent")
    row3.pack(fill="x", padx=12, pady=(4, 10))
    ctk.CTkLabel(row3, text="Capitalize", font=FONTS["body"], text_color=COLORS["text"]).pack(side="left")
    ctk.CTkSwitch(row3, text="", variable=capitalize_var,
                  fg_color=COLORS["bg_input"], progress_color=COLORS["accent"],
                  button_color=COLORS["text"], button_hover_color=COLORS["accent"]).pack(side="right")

    def generate(*_):
        words = [secrets.choice(WORD_LIST) for _ in range(count_var.get())]
        if capitalize_var.get():
            words = [w.capitalize() for w in words]
        output_var.set(sep_var.get().join(words))

    ctk.CTkButton(frame, text="Generate", font=FONTS["button"], fg_color=COLORS["accent"],
                  hover_color=COLORS["green"], command=generate).pack(fill="x", padx=16, pady=(0, 8))

    out_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    out_frame.pack(fill="x", padx=16, pady=(0, 16))

    ctk.CTkLabel(out_frame, text="Output", font=FONTS["body"],
                 text_color=COLORS["text_dim"]).pack(anchor="w", padx=12, pady=(8, 0))

    row = ctk.CTkFrame(out_frame, fg_color="transparent")
    row.pack(fill="x", padx=12, pady=(4, 10))
    ctk.CTkEntry(row, textvariable=output_var, font=FONTS["mono"],
                 fg_color=COLORS["bg_input"], text_color=COLORS["text"],
                 border_color=COLORS["border"], state="readonly", height=36).pack(side="left", fill="x", expand=True, padx=(0, 8))

    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(output_var.get())

    ctk.CTkButton(row, text="Copy", font=FONTS["button"], width=60,
                  fg_color=COLORS["border"], hover_color=COLORS["accent"],
                  command=copy).pack(side="right", ipady=2)

    generate()
