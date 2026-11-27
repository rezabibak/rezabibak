"""Draws assets/skyline.svg: an isometric city of the last year's GitHub contributions.
Run by GitHub Actions (needs GITHUB_TOKEN). With --empty it draws the waiting state."""
import datetime as dt, json, os, pathlib, sys, urllib.request
from svgkit import *

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "skyline.svg"
QUERY = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date weekday contributionCount}}}}}}"""


def fetch(user, token):
    req = urllib.request.Request("https://api.github.com/graphql",
                                 json.dumps({"query": QUERY, "variables": {"u": user}}).encode(),
                                 {"Authorization": f"bearer {token}", "User-Agent": "skyline"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        sys.exit(str(data["errors"]))
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def streaks(days):
    best = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        best = max(best, run)
    past = days[:-1] if days and not days[-1]["contributionCount"] else days  # today may still be empty
    cur = 0
    for d in reversed(past):
        if not d["contributionCount"]:
            break
        cur += 1
    return cur, best


def shade(color, k):
    return "#" + "".join(f"{int(int(color[i:i+2], 16) * k):02x}" for i in (1, 3, 5))


def draw(cal, out=OUT):
    live = cal is not None
    if not live:
        cal = {"totalContributions": 0, "weeks": [{"contributionDays": [{"weekday": d, "contributionCount": 0, "date": ""} for d in range(7)]} for _ in range(53)]}
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    peak = max([d["contributionCount"] for d in days] + [1])
    total = cal["totalContributions"]
    s = SVG(1100, 640, f"{total} GitHub contributions in the last year" if live else "Contribution skyline, waiting for the first build")
    s.panel()
    dx, dy, ox, oy = 17, 7.4, 160, 142
    s.css.append("@keyframes up{from{opacity:0;transform:translateY(-24px)}to{opacity:1;transform:none}}.t{animation:up .6s ease-out both}")
    cells = sorted((i + d["weekday"], i, d["weekday"], d["contributionCount"]) for i, w in enumerate(cal["weeks"]) for d in w["contributionDays"])
    for _, i, j, n in cells:  # back to front
        x, y = ox + (i - j) * dx, oy + (i + j) * dy
        r = n / peak
        h = 3 + (105 * r ** .55 if n else 0)
        c = "#1C2739" if not n else LEAF if r <= .25 else "#C6D94E" if r <= .5 else EMBER if r <= .75 else GOLD
        w, v = dx - 1.5, dy - .7
        g = (f'<path d="M{x-w} {y-h:.1f}L{x} {y+v-h:.1f}L{x} {y+v:.1f}L{x-w} {y:.1f}Z" fill="{shade(c,.62)}"/>'
             f'<path d="M{x} {y+v-h:.1f}L{x+w} {y-h:.1f}L{x+w} {y:.1f}L{x} {y+v:.1f}Z" fill="{shade(c,.42)}"/>'
             f'<path d="M{x} {y-v-h:.1f}L{x+w} {y-h:.1f}L{x} {y+v-h:.1f}L{x-w} {y-h:.1f}Z" fill="{c}"/>')
        s.add(f'<g class="t" style="animation-delay:{i*.025:.2f}s">{g}</g>' if n else g)
    if live:
        cur, best = streaks(days)
        s.text(f"{total:,}", 1056, 108, 54, INK, "d", "end")
        s.text("contributions in the last year", 1056, 142, 18, MUTED, anchor="end")
        stats = [(str(sum(1 for d in days if d["contributionCount"])), "active days", EMBER),
                 (str(cur), "current streak", LEAF), (str(best), "longest streak", SKY)]
        for k, (val, label, c) in enumerate(stats):
            y = 446 + k * 68
            s.text(val, 44, y, 30, c, "d"); s.text(label, 44, y + 24, 16, MUTED)
        s.text(f"updated {dt.date.today().isoformat()}", 1056, 612, 15, "#56657C", anchor="end")
    else:
        s.text("building soon", 1056, 100, 32, INK, "d", "end")
        s.text("run the Skyline workflow once", 1056, 138, 18, MUTED, anchor="end")
    s.save(out)


if __name__ == "__main__":
    if "--empty" in sys.argv:
        draw(None)
    else:
        draw(fetch(os.environ.get("GITHUB_REPOSITORY_OWNER", "rezabibak"), os.environ["GITHUB_TOKEN"]))
