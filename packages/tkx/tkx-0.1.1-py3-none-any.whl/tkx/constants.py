# Property name translations.
CSS_PROPERTY_NAME_TRANSLATIONS = {
    "background": "bg",
    "background-color": "bg",
    "border-style": "relief",
    "border-width": "bd",
    "color": "fg",
}

# Supported properties which inherit from
# the parent element by default.
INHERITED_PROPERTIES: list[str] = [
    "background",
    "color",
]

# Properties not supported by container objects.
INVALID_CONTAINER_PROPERTIES: list[str] = [
    "color",
]

# Regular expressions to help parse CSS.
MATCH_COMMENT = r"/\*.+?\*/"
MATCH_BLOCK = r"\{.*?\}"
MATCH_BRACES = r"[\{\}]"
MATCH_DELIMITER_SPACE = r"(?<=[:,])\s"
MATCH_SELECTOR = r"[:\w\.#\-]+\{"
MATCH_SPACE = r"\s"
MATCH_VAR_NAME = r"--\w+"

# tk.Widget options not associated with style.
NON_STYLE_CONFIG_OPTIONS: set[str] = {
    "class",
    "colormap",
    "command",
    "container",
    "default",
    "from_",
    "repeatdelay",
    "repeatinterval",
    "takefocus",
    "text",
    "textvariable",
    "to",
    "visual",
}

STYLE_CONFIG_OPTIONS: set[str] = {
    "bd",
    "borderwidth",
    "relief",
    "background",
    "bg",
    "cursor",
    "height",
    "highlightbackground",
    "highlightcolor",
    "highlightthickness",
    "padx",
    "pady",
    "width",
}
