"""Generate hazemezz123's profile card with live GitHub stats and auto-aging uptime.

Run daily via GitHub Actions (see .github/workflows/build.yaml). Stdlib only.
"""

import datetime
import html
import json
import urllib.request

USER_NAME = "hazemezz123"
BIRTHDAY = datetime.datetime(2007, 4, 14)

ART = """\
+++++++++********#####**###%%%%%%%%%%%%%########
***++++++++****%%##***#*****##%%%%%%%%%%%#######
**++++++++***%%%%%%%%%#*#%%#**##%%%%%%%%%%%#%%##
***++**++**%@@@@@@@%%%%%*#%%%%#*%%%%%%%%%%%%#%##
**+++++++*@@@@@@@@%%%@%%#%%%%%%*#%%%%%%%%%%%####
+++*+**+*%@@@@@@@@@@@%%%%#==+%%**#%@@@@@@%*%%###
*+++*****%@@@@@%%%%@%%%%*=:::*%**%@@@@@@@@%+*###
*+++*****#@@@@%%%%%%%%%*==:::-+**%@@@@@@@@@%%#*#
++++++****#@@%%%%%%%%##**+==---=+*@@@@@@@@@@@%##
++==+++****@@@%%%%%%%###**===--=+%@@@@@@@@@@%@@%
====++++++**%@%%%%%%%#####**##*==%@@@@@@@%%@%%@%
====++====*%%@%%%%%%%%#%%%%%#==-+%@@@@@@%%%%%@%%
===========*%@%%%%%%%%%%%+*##*=-+%@@@@%%%%%%%%%%
============*%%%%%%%%#%%%#==**+=*%%@@@@%%@@%%%@%
===========+#%#**#%%%%%%%%+=*#=*##%@@@%%%@%%%%%%
========+%%%%##**%#%%%%%%%%%###%%##%@@@@@@%%%%%%
========+#%%%%%*==*%@@@@@@%%%%%%%%%@@@@@%%@@%%%%
==========#%%%##*=-%%%@@%%%%#%@%%=#%%%%%%%%%%%%%
=========+%%%#***=:-+%@@@@@%%@@%#=%#%%##**#%%%%%
=+===+*%@@%**++=---:=#@@@@@@@%%%*-%**####****###
+++**%%@%%%%#**==-=*#@@@@@@@@@@%%%@%*#%##*******
*#%%%%%%%%%%%#=--=%@@@@@@@@@@@%%%@%%%#####**###*
%%%%%%%%%%%%%%%*==*@@@@@@@@%%%@%%%%@%#*****%#***
%%%%%%%%%%%%%%%**==%@@@@%#%**%%@%%@@%*****#%#***
%%%%%%%%%%%%%##***%@@@@@#***-:::=#%#%#*****####*
%%%%%%%%%%%%###*##%%@@@@@#***:::::=**#**********"""

STATIC_ROWS = [
    ("OS", "Ubuntu 22.04 LTS"),
    ("Uptime", "{{uptime}}"),
    ("Host", "AI Student @ Helwan Int'l Tech Univ"),
    ("Kernel", "Freelance Web Developer"),
    ("IDE", "VSCode"),
    (None, None),
    ("Languages.Programming", "Python, JavaScript, TypeScript, PHP"),
    ("Languages.Computer", "HTML, CSS, JSON, SQL"),
    ("Languages.Real", "Arabic, English"),
    (None, None),
    ("Hobbies.Software", "AI/ML, Web Development"),
    (None, None),
    ("__SECTION__", "Contact"),
    ("Portfolio.Link", "hazemdev.vercel.app"),
    ("Email.Work", "hazemezz988@gmail.com"),
    ("LinkedIn", "/in/hazem-ezz-424498285"),
    ("GitHub", "hazemezz123"),
    (None, None),
    ("__SECTION__", "GitHub Stats"),
    ("Repos", "{{repos}}"),
    ("Stars", "{{stars}}"),
    ("Followers", "{{followers}}"),
    ("Following", "{{following}}"),
]

ART_X, RIGHT_X = 15, 500
DOT_COL = 30
CH = 9.6
YS = 20
Y0 = 30
CW = RIGHT_X + DOT_COL * CH + 38 * CH + 10
H = 540

THEMES = {
    "dark": {
        "bg": "#161b22", "title": "#c9d1d9", "art": "#c9d1d9",
        "key": "#ffa657", "value": "#a5d6ff", "cc": "#616e7f",
        "sec": "#8b949e",
    },
    "light": {
        "bg": "#f6f8fa", "title": "#24292f", "art": "#24292f",
        "key": "#953800", "value": "#0550ae", "cc": "#57606a",
        "sec": "#6e7781",
    },
}


def get_json(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def fetch_stats():
    user = get_json(f"https://api.github.com/users/{USER_NAME}")
    repos = []
    for page in range(1, 10):
        batch = get_json(
            f"https://api.github.com/users/{USER_NAME}/repos"
            f"?type=owner&per_page=100&page={page}"
        )
        repos += batch
        if len(batch) < 100:
            break
    return {
        "repos": len(repos),
        "stars": sum(r.get("stargazers_count", 0) for r in repos),
        "followers": user["followers"],
        "following": user["following"],
    }


def format_age():
    today = datetime.datetime.today()
    years = today.year - BIRTHDAY.year
    months = today.month - BIRTHDAY.month
    days = today.day - BIRTHDAY.day
    if days < 0:
        months -= 1
        days += (today.replace(day=1) - datetime.timedelta(days=1)).day
    if months < 0:
        years -= 1
        months += 12
    parts = [
        f"{years} year{'s' if years != 1 else ''}",
        f"{months} month{'s' if months != 1 else ''}",
        f"{days} day{'s' if days != 1 else ''}",
    ]
    return ", ".join(parts)


def esc(s):
    return html.escape(s, quote=False)


def art_block(c):
    lines = [f'<text x="{ART_X}" y="{Y0}" fill="{c["art"]}" class="ascii">']
    for i, line in enumerate(ART.splitlines()):
        lines.append(f'<tspan x="{ART_X}" y="{Y0 + i * YS}">{esc(line)}</tspan>')
    lines.append("</text>")
    return "\n".join(lines)


def body_block(c, stats):
    rows = [f'<tspan x="{RIGHT_X}" y="{Y0}">{esc(USER_NAME)}@github</tspan>']
    y = Y0 + YS
    for key, value in STATIC_ROWS:
        if key is None:
            y += YS
            continue
        if key == "__SECTION__":
            rows.append(
                f'<tspan x="{RIGHT_X}" y="{y}" fill="{c["sec"]}">'
                f'- {esc(value)} {"\u2500" * (DOT_COL + 4)}</tspan>'
            )
        else:
            value = value.replace("{{uptime}}", format_age()).replace(
                "{{repos}}", str(stats["repos"])
            ).replace("{{stars}}", str(stats["stars"])).replace(
                "{{followers}}", str(stats["followers"])
            ).replace("{{following}}", str(stats["following"]))
            dots = "\u00b7" * (DOT_COL - len(key))
            rows.append(
                f'<tspan x="{RIGHT_X}" y="{y}"><tspan class="key">{esc(key)}</tspan>'
                f'<tspan class="cc">{esc(dots)}</tspan>'
                f'<tspan class="value">{esc(value)}</tspan></tspan>'
            )
        y += YS
    return "\n".join(rows)


def render(name, c, stats):
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{CW}px" height="{H}px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {c["key"]};}}
.value {{fill: {c["value"]};}}
.cc {{fill: {c["cc"]};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{CW}px" height="{H}px" fill="{c['bg']}" rx="15"/>
{art_block(c)}
<text x="{RIGHT_X}" y="{Y0}" fill="{c['title']}">
{body_block(c, stats)}
</text>
</svg>
"""


def main():
    stats = fetch_stats()
    print(f"stats: {stats}")
    for name, c in THEMES.items():
        with open(f"{name}_mode.svg", "w", encoding="utf-8") as f:
            f.write(render(name, c, stats))
        print(f"{name}_mode.svg written")


if __name__ == "__main__":
    main()
