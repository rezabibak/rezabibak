"""Rebuild every static graphic:  python3 scripts/build.py   (edit the text below, then run)."""
import pathlib
from svgkit import *

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"


def pts(*p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def dots(s, step=28):
    s.defs.append(f'<pattern id="dots" width="{step}" height="{step}" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#223047"/></pattern>')
    s.add(f'<rect width="{s.w}" height="{s.h}" rx="22" fill="url(#dots)" opacity=".7"/>')


# ---------------- hero ----------------
def hero():
    s = SVG(1100, 540, "Reza Bibak, Java Backend Engineer from Tehran")
    s.defs.append(f'<linearGradient id="face" gradientUnits="userSpaceOnUse" x1="60" y1="130" x2="520" y2="350"><stop stop-color="{GOLD}"/><stop offset=".45" stop-color="{EMBER}"/><stop offset="1" stop-color="{LEAF}"/></linearGradient>')
    s.defs.append(f'<radialGradient id="glow"><stop stop-color="{EMBER}" stop-opacity=".22"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>')
    s.defs.append(f'<radialGradient id="glow2"><stop stop-color="{LEAF}" stop-opacity=".16"/><stop offset="1" stop-color="{LEAF}" stop-opacity="0"/></radialGradient>')
    s.panel(); dots(s)
    s.add('<ellipse cx="220" cy="190" rx="220" ry="190" fill="url(#glow)"/><ellipse cx="760" cy="320" rx="300" ry="215" fill="url(#glow2)"/>')

    w = s.text("GET", 64, 82, 19, LEAF, "b")
    s.text("/reza-bibak  HTTP/1.1", 64 + w + 14, 82, 19, MUTED)

    # extruded 3D wordmark
    lines = [("REZA", 62, 218, 84), ("BIBAK", 62, 318, 84)]
    for i in range(16, 0, -1):
        shade = f"#{int(120 - i*5.5):02x}{int(48 - i*1.8):02x}{int(30 - i*.4):02x}"
        for t, x, y, z in lines:
            s.text(t, x + i * .9, y + i * .9, z, shade, "d")
    clip = []
    for t, x, y, z in lines:
        assert x + s.width(t, z, "d") < 560, t
        clip += s.uses(t, x, y, z, "d")
    s.defs.append('<clipPath id="word">' + "".join(f'<use href="#{g}" transform="{t}"/>' for g, t in clip) + "</clipPath>")
    s.defs.append('<linearGradient id="shine"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    s.add('<g clip-path="url(#word)"><rect x="40" y="100" width="560" height="260" fill="url(#face)"/>'
          '<g transform="skewX(-20)"><rect y="100" width="90" height="260" fill="url(#shine)" x="-100">'
          '<animate attributeName="x" values="-100;800;800" keyTimes="0;.35;1" dur="6s" repeatCount="indefinite"/></rect></g></g>')

    s.text("Java Backend Engineer", 66, 394, 30, INK, "b")
    s.text("Spring Boot · JPA/Hibernate · PostgreSQL", 66, 432, 19, MUTED)
    s.add(f'<circle cx="73" cy="475" r="6" fill="{LEAF}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    s.text("Tehran, Iran", 90, 481, 18, MUTED)

    # isometric request lifecycle
    cx, W, H, T, y0, gap = 725, 128, 56, 17, 128, 100
    layers = [("@RestController", "validate + map", GOLD), ("@Service", "business rules", EMBER),
              ("@Repository", "JPA / Hibernate", "#C6D94E"), ("PostgreSQL", "ACID storage", LEAF)]
    D = 7  # seconds per request/response cycle
    for i in range(3, -1, -1):
        name, note, c = layers[i]
        y = y0 + i * gap
        top = pts((cx, y - H), (cx + W, y), (cx, y + H), (cx - W, y))
        s.add(f'<polygon points="{pts((cx-W,y),(cx,y+H),(cx,y+H+T),(cx-W,y+T))}" fill="{c}" opacity=".5"/>')
        s.add(f'<polygon points="{pts((cx,y+H),(cx+W,y),(cx+W,y+T),(cx,y+H+T))}" fill="{c}" opacity=".28"/>')
        s.add(f'<polygon points="{top}" fill="{PANEL}" fill-opacity=".94" stroke="{c}" stroke-width="2"/>')
        for k in (.66, .33):
            s.add(f'<polygon points="{pts((cx,y-H*k),(cx+W*k,y),(cx,y+H*k),(cx-W*k,y))}" fill="none" stroke="{c}" opacity=".25"/>')
        down, up = .06 + i * .13, .94 - i * .13
        if i == 3:  # the database is visited once, at the turning point
            keys, vals = [0, down - .05, down, down + .12, 1], "0;0;.55;0;0"
        else:
            keys, vals = [0, down - .05, down, down + .07, up - .05, up, up + .05, 1], "0;0;.55;0;0;.4;0;0"
        s.add(f'<polygon points="{top}" fill="{c}" opacity="0"><animate attributeName="opacity" values="{vals}" '
              f'keyTimes="{";".join(f"{v:.3f}" for v in keys)}" dur="{D}s" repeatCount="indefinite"/></polygon>')
        s.add(f'<path d="M{cx+W+8} {y}H{cx+W+34}" stroke="{c}" stroke-width="2"/><circle cx="{cx+W+8}" cy="{y}" r="3.5" fill="{c}"/>')
        s.text(name, cx + W + 44, y + 1, 19, INK, "b")
        s.text(note, cx + W + 44, y + 25, 15, MUTED)
    ys = [58] + [y0 + i * gap for i in range(4)]
    path = ys + ys[::-1][1:]
    times = [0, .06, .19, .32, .45, .58, .71, .84, .94, 1]
    vals = ";".join(f"{cx} {v}" for v in path + [58])
    kt = ";".join(map(str, times))
    s.add(f'<path d="M{cx} 40V{y0-H}" stroke="{MUTED}" stroke-dasharray="3 6"/>')
    s.add(f'<g transform="translate({cx} 58)"><animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/>'
          f'<circle r="17" fill="#fff" opacity=".13"/><circle r="10" fill="#fff" opacity=".28"/><circle r="5.5" fill="#fff"/></g>')
    for label, c, v in (("request", GOLD, "1;0"), ("200 OK", LEAF, "0;1")):
        s.add(f'<g opacity="{v[0]}"><animate attributeName="opacity" calcMode="discrete" values="{v}" keyTimes="0;.45" dur="{D}s" repeatCount="indefinite"/>')
        s.text(label, cx + 30, 52, 17, c, "b"); s.add("</g>")
    s.save(OUT / "hero.svg")


# ---------------- section headers ----------------
def header(name, route, title, color):
    s = SVG(1100, 76, title)
    s.panel(h=76, r=16)
    s.add(f'<rect x="16" y="18" width="76" height="40" rx="9" fill="{color}"/>')
    s.text("GET", 54, 46, 20, BG, "b", "middle")
    s.text(route, 112, 47, 25, INK, "b")
    s.text(title, 1072, 46, 19, MUTED, anchor="end")
    s.save(OUT / f"h-{name}.svg")


# ---------------- boot log ----------------
PIX = {"R": "11110 10001 10001 11110 10100 10010 10001", "E": "11111 10000 10000 11110 10000 10000 11111",
       "Z": "11111 00001 00010 00100 01000 10000 11111", "A": "01110 10001 10001 11111 10001 10001 10001"}


def boot():
    s = SVG(1100, 560, "Startup log: studied Software Engineering; focused on clean architecture, transactions and reliable APIs")
    s.panel()
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        s.add(f'<circle cx="{34+i*24}" cy="32" r="7" fill="{c}"/>')
    s.text("reza@tehran: ~/backend  $ ./mvnw spring-boot:run", 550, 38, 16, MUTED, anchor="middle")
    s.add(f'<path d="M1 60H1099" stroke="{LINE}"/>')
    cols = [GOLD, GOLD, "#FFA94A", EMBER, "#C6C84C", "#A2D653", LEAF]
    for n, ch in enumerate("REZA"):
        for r, row in enumerate(PIX[ch].split()):
            for c, bit in enumerate(row):
                if bit == "1":
                    s.add(f'<rect x="{44+n*84+c*14}" y="{84+r*14}" width="11" height="11" rx="2.5" fill="{cols[r]}"/>')
    s.text(":: Backend Engineer ::", 420, 128, 24, LEAF, "b")
    s.text("Java 25  ·  Spring Boot", 420, 164, 20, MUTED)
    rows = [("Starting", "RezaApplication in Tehran, Iran"), ("Education", "Software Engineering"),
            ("Focus", "clean architecture, correct transactions,"), ("", "reliable APIs and database behavior"),
            ("Curious", "what happens underneath the annotations"), ("Learning", "Spring Boot -> JPA -> SQL -> System Design"),
            ("Goal", "predictable, testable, maintainable systems")]
    s.css.append("@keyframes in{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}.l{animation:in .45s ease-out both}")
    y = 232
    for i, (k, v) in enumerate(rows):
        s.add(f'<g class="l" style="animation-delay:{.3+i*.35:.2f}s">')
        if k:
            s.text("INFO", 44, y, 19, LEAF, "b"); s.text(k, 114, y, 19, SKY)
        s.text(v, 262, y, 19, INK)
        s.add("</g>"); y += 36
    s.add(f'<g class="l" style="animation-delay:{.3+len(rows)*.35:.2f}s">')
    w = s.text("Started RezaApplication · ready for requests", 44, y + 24, 20, GOLD, "b")
    s.add(f'<rect x="{44+w+12:.0f}" y="{y+6}" width="11" height="22" fill="{INK}"><animate attributeName="opacity" calcMode="discrete" values="1;0" dur="1s" repeatCount="indefinite"/></rect></g>')
    s.save(OUT / "boot.svg")


# ---------------- stack ----------------
def stack():
    groups = [("language", EMBER, ["Java 25", "Collections", "Streams", "Concurrency", "JVM"]),
              ("spring", LEAF, ["Boot", "Web MVC", "Security", "Data JPA", "Hibernate"]),
              ("data", SKY, ["PostgreSQL", "MySQL", "Redis", "SQL"]),
              ("messaging", VIOLET, ["RabbitMQ", "Kafka"]),
              ("ops", GOLD, ["Docker", "Linux", "NGINX", "Maven", "Git"])]
    s = SVG(1100, 438, "Tech stack: " + ", ".join(i for g in groups for i in g[2]))
    s.panel(); dots(s)
    s.add(f'<path d="M222 59V379" stroke="{LINE}" stroke-width="3"/>')
    for r, (name, c, items) in enumerate(groups):
        y = 59 + r * 80
        s.text(name, 44, y + 7, 21, c, "b")
        x = 262
        s.add(f'<path d="M222 {y}H{x}" stroke="{c}" stroke-width="2" opacity=".6"/><circle cx="222" cy="{y}" r="4" fill="{c}"/>')
        for i, t in enumerate(items):
            w = s.width(t, 19, "b") + 40
            s.add(f'<rect x="{x:.0f}" y="{y-26}" width="{w:.0f}" height="52" rx="12" fill="{PANEL}" stroke="{c}" stroke-opacity=".45" stroke-width="1.5">'
                  f'<animate attributeName="stroke-opacity" values=".45;1;.45;.45" keyTimes="0;.08;.18;1" dur="8s" begin="{r*.8+i*.18:.2f}s" repeatCount="indefinite"/></rect>')
            s.text(t, x + 20, y + 7, 19, INK, "b")
            x += w + 16
        assert x < 1090, name
    s.add('<circle cx="222" cy="59" r="6" fill="#fff"><animate attributeName="cy" values="59;379;59" dur="8s" repeatCount="indefinite"/></circle>')
    s.save(OUT / "stack.svg")


# ---------------- project cards ----------------
def card(file, color, title, desc, tags, art):
    s = SVG(540, 370, f"{title}: {' '.join(desc)}")
    s.panel()
    s.add(f'<rect x="14" y="14" width="512" height="176" rx="14" fill="{PANEL}"/>')
    art(s)
    s.text(title, 28, 234, 27, INK, "b")
    for i, d in enumerate(desc):
        assert s.width(d, 18) < 495, d
        s.text(d, 28, 268 + i * 26, 18, MUTED)
    x = 28
    for t in tags:
        w = s.width(t, 15, "b") + 24
        s.add(f'<rect x="{x:.0f}" y="318" width="{w:.0f}" height="32" rx="16" fill="{color}" fill-opacity=".13" stroke="{color}" stroke-opacity=".6"/>')
        s.text(t, x + 12, 339, 15, color, "b")
        x += w + 10
    s.save(OUT / f"p-{file}.svg")


def art_pomodoro(s):
    s.add(f'<circle cx="270" cy="102" r="66" fill="none" stroke="{LINE}" stroke-width="11"/>')
    s.add(f'<circle cx="270" cy="102" r="66" fill="none" stroke="{SKY}" stroke-width="11" stroke-linecap="round" stroke-dasharray="415" stroke-dashoffset="104" transform="rotate(-90 270 102)">'
          '<animate attributeName="stroke-dashoffset" values="415;0" dur="10s" repeatCount="indefinite"/></circle>')
    s.text("25:00", 270, 111, 26, INK, "b", "middle")
    for i in range(4):
        s.add(f'<circle cx="{390+i*24}" cy="102" r="6" fill="{SKY if i < 2 else LINE}"/>')
    s.text("focus", 150, 108, 18, SKY, "b", "end")


def art_university(s):
    for r, row in enumerate((("id", "student", "query"), ("01", "......", "INSERT"), ("02", "......", "SELECT"), ("03", "......", "UPDATE"))):
        y = 54 + r * 36
        if r:
            s.add(f'<rect x="60" y="{y-23}" width="420" height="30" rx="6" fill="{EMBER}" opacity="0"><animate attributeName="opacity" values="0;.2;0;0" keyTimes="0;.12;.3;1" dur="4.5s" begin="{(r-1)*1.3}s" repeatCount="indefinite"/></rect>')
        for t, x in zip(row, (80, 190, 380)):
            s.text(t, x, y - 2, 18, MUTED if r == 0 else EMBER if x == 380 else INK, "b" if r == 0 else "r")
        s.add(f'<path d="M60 {y+11}H480" stroke="{LINE}"/>')


def art_collections(s):
    s.text("capacity * 2  ->  arraycopy", 270, 55, 17, MUTED, anchor="middle")
    for i in range(8):
        x = 46 + i * 57
        dash = "" if i < 4 else 'stroke-dasharray="5 5"'
        s.add(f'<rect x="{x}" y="80" width="49" height="54" rx="8" fill="none" stroke="{LEAF if i < 4 else "#34445E"}" stroke-width="2" {dash}/>')
        s.add(f'<g opacity="{1 if i < 6 else 0}">')
        if i >= 4:
            a = (i - 3) * .14
            s.add(f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{a:.2f};{a+.05:.2f};.94;1" dur="6s" repeatCount="indefinite"/>')
        s.add(f'<rect x="{x+6}" y="86" width="37" height="42" rx="5" fill="{LEAF}" fill-opacity=".2"/>')
        s.text("T", x + 24.5, 115, 22, LEAF, "b", "middle"); s.add("</g>")
        s.text(str(i), x + 24.5, 164, 15, MUTED, anchor="middle")


def art_zed(s):
    code = [[("{", MUTED)], [('  "base_keymap"', VIOLET), (': "JetBrains",', LEAF)],
            [('  "theme"', VIOLET), (': "Aura Dark",', LEAF)], [('  "icon_theme"', VIOLET), (': "Warm Charmed..."', LEAF)], [("}", MUTED)]]
    for i, line in enumerate(code):
        x, y = 78, 50 + i * 29
        s.text(str(i + 1), 52, y, 15, "#4B5A70", anchor="end")
        for t, c in line:
            x += s.text(t, x, y, 18, c)
    s.add(f'<rect x="{78+s.width("}",18)+4:.0f}" y="150" width="3" height="22" fill="{VIOLET}"><animate attributeName="opacity" calcMode="discrete" values="1;0" dur="1.1s" repeatCount="indefinite"/></rect>')


def projects():
    card("pomodoro", SKY, "Pomodoro Sky", ["A glassmorphism Pomodoro timer living", "in the GNOME Shell top bar."], ["GJS", "GNOME 45+"], art_pomodoro)
    card("university", EMBER, "University", ["Student registration system with", "MySQL storage, built on plain JDBC."], ["Java", "HikariCP", "DAO", "Factory"], art_university)
    card("collections", LEAF, "CustomCollections", ["A generic, resizable collection with", "its own Iterator, written by hand."], ["Java", "Generics", "Iterator"], art_collections)
    card("zed", VIOLET, "MyZedConfigure", ["My personal settings for the", "Zed editor."], ["Zed", "JSON", "Aura Dark"], art_zed)


# ---------------- contacts and footer ----------------
def button(file, label, color):
    s = SVG(300, 68, label)
    s.panel(h=68, r=34, fill=PANEL, stroke=color)
    s.text(label, 138, 42, 19, INK, "b", "middle")
    s.add(f'<circle cx="256" cy="34" r="17" fill="{color}"/><path d="M250 40L262 28M252 28H262V38" stroke="{BG}" stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    s.save(OUT / f"btn-{file}.svg")


def footer():
    s = SVG(1100, 250, "HTTP 200 OK. Thanks for visiting, let's build something reliable.")
    s.panel()
    s.defs.append(f'<linearGradient id="bar"><stop stop-color="{GOLD}"/><stop offset=".5" stop-color="{EMBER}"/><stop offset="1" stop-color="{LEAF}"/></linearGradient>')
    s.text("HTTP/1.1", 550, 52, 18, MUTED, anchor="middle")
    s.text("200 OK", 550, 122, 54, LEAF, "d", "middle")
    s.text("Thanks for visiting. Let's build something reliable.", 550, 175, 22, INK, "b", "middle")
    s.add('<rect x="350" y="206" width="400" height="5" rx="2.5" fill="url(#bar)"><animate attributeName="width" values="400;40;400" dur="6s" repeatCount="indefinite"/><animate attributeName="x" values="350;530;350" dur="6s" repeatCount="indefinite"/></rect>')
    s.save(OUT / "footer.svg")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    hero(); boot(); stack(); projects(); footer()
    header("about", "/about", "who is behind the code", GOLD)
    header("beans", "/beans", "what's in my context", LEAF)
    header("projects", "/projects", "built to understand", EMBER)
    header("activity", "/activity", "one tower per day", SKY)
    button("linkedin", "LinkedIn", SKY); button("email", "Email me", EMBER)
