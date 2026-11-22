"""Front page for Saturday 21 November 2026: 43 verified news stories.

Fresh build for the news-image-20261121 bounty. Pure standard library
and fully deterministic: no network, no clock, no randomness, no external
font files. Text is drawn with a small built-in 5x7 bitmap font and the
PNG is encoded by hand with zlib.

Reads OUTPUT_DIR (default /output) and writes entry.png, 1024x1024.
"""

import os
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024

INK = (18, 18, 18)
GREY = (96, 96, 96)
PAPER = (255, 255, 255)

# 5x7 bitmap font. Each glyph is 7 rows of 5 bits ("1" = ink, "0" = paper).
FONT = {
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "$": ("00100", "01111", "10101", "01110", "00101", "11110", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01110", "10001", "10010", "01000", "10101", "10010", "01101"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00011", "00100", "01000", "01000", "01000", "00100", "00011"),
    ")": ("11000", "00100", "00010", "00010", "00010", "00100", "11000"),
    "*": ("00000", "01010", "00100", "11111", "00100", "01010", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    ",": ("00000", "00000", "00000", "00000", "01100", "01100", "01000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    "/": ("00001", "00010", "00010", "00100", "00100", "01000", "10000"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10001", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00010", "00100", "00100", "00100"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "01100", "01000"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "@": ("01110", "10001", "10111", "10101", "10111", "10000", "01110"),
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "11001", "10101", "10011", "10011", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "\\": ("10000", "01000", "01000", "00100", "00100", "00010", "00010"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "^": ("00100", "01010", "00000", "00000", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "`": ("01000", "00100", "00000", "00000", "00000", "00000", "00000"),
}

FONT.update({
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10000", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01110", "10001", "10001", "01110", "10000", "01100"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00000", "00100", "00000", "01100", "00100", "00100", "01110"),
    "j": ("00100", "00000", "01100", "00100", "00100", "00100", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "11110", "10000", "10000"),
    "q": ("00000", "01111", "10001", "10001", "01111", "00001", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11110", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10001", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "10001", "10001", "01010", "00100", "00100", "01100"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "{": ("00011", "00100", "00100", "01100", "00100", "00100", "00011"),
    "|": ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
    "}": ("11000", "00100", "00100", "00110", "00100", "00100", "11000"),
    "~": ("00000", "00000", "01010", "10101", "00000", "00000", "00000"),
})


def text_width(text, scale):
    """Pixel width of text at the given scale (no trailing spacing)."""
    if not text:
        return 0
    return len(text) * 6 * scale - scale


def wrap_lines(text, max_width, scale):
    """Greedy word wrap. Returns a list of lines, each within max_width."""
    words = text.split(" ")
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if text_width(trial, scale) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class Canvas:
    """An RGB image held as a flat bytearray."""

    def __init__(self, width, height, colour):
        self.width = width
        self.height = height
        self.pixels = bytearray(colour * (width * height))

    def fill_rect(self, x, y, w, h, colour):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        for row in range(y0, y1):
            base = (row * self.width + x0) * 3
            for col in range(x0, x1):
                off = base + (col - x0) * 3
                self.pixels[off] = colour[0]
                self.pixels[off + 1] = colour[1]
                self.pixels[off + 2] = colour[2]

    def draw_text(self, x, y, text, scale, colour, bold=False):
        """Draw text with the bitmap font. Bold adds a 1px right offset pass."""
        passes = (0, 1) if bold else (0,)
        for dx in passes:
            cx = x + dx
            for ch in text:
                glyph = FONT.get(ch)
                if glyph is None:
                    cx += 6 * scale
                    continue
                for row, bits in enumerate(glyph):
                    for col, bit in enumerate(bits):
                        if bit == "1":
                            self.fill_rect(
                                cx + col * scale, y + row * scale,
                                scale, scale, colour,
                            )
                cx += 6 * scale


def _png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, canvas):
    """Encode the canvas as a PNG file (filter 0, zlib level 9)."""
    raw = bytearray()
    row_bytes = canvas.width * 3
    for y in range(canvas.height):
        raw.append(0)
        start = y * row_bytes
        raw += canvas.pixels[start:start + row_bytes]
    header = struct.pack(">IIBBBBB", canvas.width, canvas.height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(b"IHDR", header)
    png += _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _png_chunk(b"IEND", b"")
    with open(path, "wb") as handle:
        handle.write(png)


# All 43 stories were published on Saturday 21 November 2026. Each entry is
# (section, headline, summary). Headlines fit one line at scale 2 in a
# 464px column; summaries fit one line at scale 1. Sources: One Turn day
# digest for 21 Nov 2026 (106 stories, sources BBC/Reuters/Guardian/
# France 24/Al Jazeera/CBS/NPR/UPI etc.) and its morning brief.
STORIES = [
    ("LEAD", "Iran strikes US bases in Bahrain",
     "Tehran says it hit two bases; Bahrain reports a fire at an industrial site."),
    ("WORLD", "Mexico captures El Chapo Isidro",
     "FBI most-wanted cartel boss seized in Sinaloa; 11 die in the violence."),
    ("WORLD", "Russian missile hits Zelensky town",
     "Kryvyi Rih strike kills 2, wounds 60; missiles also land in Poland."),
    ("WORLD", "COP31 talks run into overtime",
     "Antalya summit passes its deadline with no deal; fossil fuels left out."),
    ("WORLD", "Trump defends his Putin ties",
     "After the Shenzhen summit, Zelensky calls Putin a killer."),
    ("WORLD", "Drones hit Russian ship in Baltic",
     "Sparta II burns in the Gulf of Finland; Finland blames Ukraine."),
    ("WORLD", "Israeli strike kills 3 in Gaza",
     "Food vehicle hit in Gaza City; settler violence at record levels."),
    ("WORLD", "Houthis and Saudis trade strikes",
     "Missiles at Riyadh intercepted; coalition hits Hodeidah 71 times."),
    ("WORLD", "UK and EU sign three new deals",
     "Food, emissions and youth travel pacts signed in Brussels."),
    ("WORLD", "EU and Indonesia sign trade deal",
     "Pact cuts 98.5% of tariffs on EU goods; covers 730m people."),
    ("WORLD", "Denmark expels Russian diplomat",
     "Attache expelled over an alleged plot to kill rapper Kyivstoner."),
    ("WORLD", "Protests sweep Europe over costs",
     "Thousands march in France and Portugal; 144 arrests in Paris."),
    ("WORLD", "French police jailed over beating",
     "Three officers get five years for the racist attack on Zecler."),
    ("WORLD", "Salvadoran troops fight in Haiti",
     "Three soldiers die in a blast as gangs battle in Port-au-Prince."),
    ("WORLD", "700,000 displaced in Ethiopia",
     "Families flee the south as troops mass on the Eritrea border."),
    ("WORLD", "Estonia to shut Russia crossings",
     "Three border posts close from Dec. 1; queues form on the far side."),
    ("WORLD", "Turkey takes control of Sozcu TV",
     "Last big independent news channel falls under state control."),
    ("MARKETS", "AI sell-off drags markets down",
     "S&P 500 falls 3.7% into correction; Nasdaq erases its 2026 gains."),
    ("MARKETS", "Nikkei falls 5.06% in Tokyo",
     "Asian markets slide further as chip shares plunge worldwide."),
    ("MARKETS", "Anthropic IPO stumbles day two",
     "Record listing slips after a $2 trillion debut on Wall Street."),
    ("MARKETS", "Nvidia chief ousted, Trump says",
     "Huang is out after a scandal; chip export rules unchanged."),
    ("MARKETS", "Trump taxes offshore data centres",
     "US tech firms building AI centres abroad face a tremendous tax."),
    ("MARKETS", "Gulf economies hit by Iran war",
     "Oil states slide into recession as Hormuz shipping is disrupted."),
    ("MARKETS", "Brent oil falls 5% in a week",
     "Crude ends near $91 as Gulf flows recover despite the attacks."),
    ("MARKETS", "Saudi-Japan agree oil stockpile",
     "Riyadh triples crude stored in Japan to 24 million barrels."),
    ("MARKETS", "Argentina bonds fall to distress",
     "Debt slides for the first time in two years; $50bn LNG plan ok'd."),
    ("MARKETS", "EU plans Big Tech tax in budget",
     "Costa proposes a smaller budget with a 3% levy on digital giants."),
    ("MARKETS", "GTA VI earns $3.8bn in a day",
     "Biggest entertainment launch ever after its release on Nov. 18."),
    ("MARKETS", "YouTube nears schools settlement",
     "Multibillion-dollar deal over addiction claims nears completion."),
]

STORIES += [
    ("SCIENCE", "AI claims proof of Riemann",
     "Anthropic mathematician says Claude helped prove it in six weeks."),
    ("SCIENCE", "BepiColombo reaches Mercury",
     "Probe enters orbit after an eight-year, 10-billion-km journey."),
    ("SCIENCE", "Wolbachia cuts dengue in Brazil",
     "Children near the bacteria-carrying mosquitoes catch dengue less."),
    ("SCIENCE", "Pill fights pancreatic cancer",
     "Daraxonrasib shrinks tumours in some patients, trial reports."),
    ("SCIENCE", "US child dies of measles",
     "Virginia reports a child death as the US loses elimination status."),
    ("SCIENCE", "Voyager 1 is 24 light-hours out",
     "The probe keeps sending data from interstellar space."),
    ("SCIENCE", "CERN sees ultra-rare decay",
     "Physicists report first evidence of a rare particle decay."),
    ("SCIENCE", "M6.7 quake shakes central Peru",
     "Strong tremor hits the Andes; M6.8 quake also strikes off Timor."),
    ("SCIENCE", "Uganda curbs travel over Ebola",
     "Gatherings restricted as the DR Congo outbreak may be the worst."),
    ("SCIENCE", "Kenya starts drilling for oil",
     "Onshore crude drilling begins in Turkana; output countdown starts."),
    ("SPORT", "Alcaraz to face Zverev in final",
     "Alcaraz beats Shelton in three sets to reach the ATP Finals decider."),
    ("SPORT", "Harden passes Kobe with 51",
     "James Harden scores 51 in the Cavaliers' 128-119 win over Indiana."),
    ("SPORT", "England beat All Blacks big",
     "England win by a wide margin at Twickenham in the autumn finale."),
    ("SPORT", "Wallabies edge Wales 29-26",
     "Australia end a four-match losing streak in Cardiff."),
]

FOOTER = ("Sources: One Turn 21 Nov digest, Majik Morning Brief, "
          "BBC, Reuters, Guardian, France 24, Al Jazeera, CBS, UPI")

MARGIN = 32
COL_WIDTH = 464
GUTTER = 32
LEFT_X = MARGIN
RIGHT_X = MARGIN + COL_WIDTH + GUTTER


def draw_section_header(canvas, x, y, title):
    canvas.draw_text(x, y, title, 2, INK, bold=True)
    canvas.fill_rect(x, y + 18, COL_WIDTH, 2, INK)
    return y + 26


def draw_story(canvas, x, y, headline, summary):
    head_lines = wrap_lines(headline, COL_WIDTH, 2)
    sum_lines = wrap_lines(summary, COL_WIDTH, 1)
    assert len(head_lines) == 1, "headline too long: %r" % headline
    assert len(sum_lines) == 1, "summary too long: %r" % summary
    canvas.draw_text(x, y, head_lines[0], 2, INK)
    canvas.draw_text(x, y + 17, sum_lines[0], 1, GREY)
    return y + 32


def draw_column(canvas, x, start_y, sections):
    y = start_y
    for section, items in sections:
        y = draw_section_header(canvas, x, y, section)
        for headline, summary in items:
            y = draw_story(canvas, x, y, headline, summary)
        y += 6
    return y


def render():
    assert len(STORIES) == 43, "expected 43 stories, got %d" % len(STORIES)
    by_section = {}
    for section, headline, summary in STORIES:
        by_section.setdefault(section, []).append((headline, summary))
    for name in ("LEAD", "WORLD", "MARKETS", "SCIENCE", "SPORT"):
        assert name in by_section, "missing section %s" % name

    canvas = Canvas(WIDTH, HEIGHT, PAPER)

    # Masthead.
    title = "THE DAILY FRONT PAGE"
    canvas.draw_text((WIDTH - text_width(title, 4)) // 2, 24, title, 4, INK, bold=True)
    canvas.fill_rect(MARGIN, 62, WIDTH - 2 * MARGIN, 3, INK)
    date_line = "SATURDAY 21 NOVEMBER 2026 - 43 STORIES"
    canvas.draw_text((WIDTH - text_width(date_line, 2)) // 2, 72, date_line, 2, INK)
    canvas.fill_rect(MARGIN, 92, WIDTH - 2 * MARGIN, 1, INK)

    # Lead story, full width.
    lead_head, lead_sum = by_section["LEAD"][0]
    canvas.draw_text(MARGIN, 106, "LEAD", 1, GREY, bold=True)
    canvas.draw_text(MARGIN, 118, lead_head, 3, INK, bold=True)
    canvas.draw_text(MARGIN, 145, lead_sum, 2, GREY)
    canvas.fill_rect(MARGIN, 168, WIDTH - 2 * MARGIN, 2, INK)

    # Two columns: WORLD + SPORT on the left, MARKETS + SCIENCE on the right.
    left_end = draw_column(canvas, LEFT_X, 184, [
        ("WORLD", by_section["WORLD"]),
        ("SPORT", by_section["SPORT"]),
    ])
    right_end = draw_column(canvas, RIGHT_X, 184, [
        ("MARKETS", by_section["MARKETS"]),
        ("SCIENCE", by_section["SCIENCE"]),
    ])
    assert left_end <= 960, "left column overflows: %d" % left_end
    assert right_end <= 960, "right column overflows: %d" % right_end

    # Footer.
    canvas.fill_rect(MARGIN, 968, WIDTH - 2 * MARGIN, 1, INK)
    canvas.draw_text(MARGIN, 978, FOOTER, 1, GREY)
    return canvas, left_end, right_end


def main():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas, left_end, right_end = render()
    path = os.path.join(out_dir, "entry.png")
    write_png(path, canvas)
    print("stories: %d" % len(STORIES))
    print("size: %dx%d" % (WIDTH, HEIGHT))
    print("left column ends at y=%d, right column ends at y=%d" % (left_end, right_end))
    print("wrote %s" % path)


if __name__ == "__main__":
    main()
