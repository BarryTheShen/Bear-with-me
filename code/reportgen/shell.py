"""Document shell: CSS, layout primitives and figure/callout helpers.

Kept separate from `charts.py` so chart geometry and page typography can change
independently. Everything inlines into one HTML file - no external requests.

Also owns `REPORTS`, the single definition of where generated HTML is written.
It lives here rather than in each `build_*.py` so that moving the project only
requires editing one line instead of nine.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

# bear-with-me/code/reportgen/shell.py -> bear-with-me/reports
REPORTS = Path(__file__).resolve().parents[2] / "reports"

CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#f4f6f8;color:#12181f;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  font-size:16.5px;line-height:1.62;font-variant-numeric:tabular-nums}
.page{max-width:1080px;margin:0 auto;background:#fff;padding:0 0 72px;
  box-shadow:0 0 0 1px #e3e8ee,0 18px 48px -32px rgba(18,24,31,.4)}
.wrap{padding:0 62px}
h1,h2,h3,h4{line-height:1.22;margin:0;letter-spacing:-.011em}
h1{font-size:2.55rem;font-weight:750}
h2{font-size:1.72rem;font-weight:700;margin:56px 0 6px;scroll-margin-top:16px}
h3{font-size:1.2rem;font-weight:680;margin:34px 0 6px}
h4{font-size:1rem;font-weight:670;margin:22px 0 4px}
p{margin:.72em 0}
a{color:#2f5d9e;text-decoration-thickness:.06em;text-underline-offset:.16em}
strong{font-weight:660}
small{font-size:.83rem}
ul,ol{margin:.6em 0;padding-left:1.35em}
li{margin:.3em 0}
li::marker{color:#7a8794}

/* ---- masthead ---- */
.masthead{background:linear-gradient(157deg,#12181f 0%,#1d2c3f 52%,#2f5d9e 160%);
  color:#fff;padding:52px 62px 44px;margin-bottom:8px}
.masthead h1{color:#fff;max-width:20ch}
.kicker{font-size:.76rem;letter-spacing:.15em;text-transform:uppercase;
  color:#8fb4e6;font-weight:670;margin-bottom:14px}
.standfirst{font-size:1.12rem;color:#c8d4e2;max-width:64ch;margin-top:16px}
.meta{margin-top:26px;padding-top:18px;border-top:1px solid rgba(255,255,255,.16);
  display:flex;flex-wrap:wrap;gap:26px;font-size:.82rem;color:#9fb3c9}
.meta b{color:#e7eef6;font-weight:620;display:block;font-size:.74rem;
  letter-spacing:.09em;text-transform:uppercase;margin-bottom:2px}

/* ---- table of contents ---- */
.toc{background:#f7f9fb;border:1px solid #e3e8ee;border-radius:10px;
  padding:20px 26px;margin:30px 0 8px}
.toc h4{margin:0 0 10px;font-size:.76rem;letter-spacing:.13em;
  text-transform:uppercase;color:#5b6673}
.toc ol{columns:2;column-gap:38px;margin:0;padding-left:1.15em;font-size:.94rem}
.toc a{text-decoration:none;color:#22303f}
.toc a:hover{text-decoration:underline}

/* ---- key-number strip ---- */
.keys{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#e3e8ee;
  border:1px solid #e3e8ee;border-radius:10px;overflow:hidden;margin:26px 0}
.key{background:#fff;padding:18px 18px 16px}
.key .n{font-size:1.92rem;font-weight:730;letter-spacing:-.02em;line-height:1.08}
.key .l{font-size:.83rem;color:#5b6673;margin-top:5px;line-height:1.42}
.key .s{font-size:.71rem;color:#8b949e;margin-top:7px}

/* ---- figures ---- */
figure{margin:30px 0;padding:22px 24px 18px;border:1px solid #e3e8ee;
  border-radius:10px;background:#fff;break-inside:avoid}
figure .fignum{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;
  color:#c8542a;font-weight:700;margin-bottom:4px}
figure .figtitle{font-size:1.02rem;font-weight:660;margin-bottom:3px;line-height:1.35}
figure .figsub{font-size:.86rem;color:#5b6673;margin-bottom:16px;max-width:80ch}
figcaption{margin-top:14px;padding-top:11px;border-top:1px solid #eef1f5;
  font-size:.78rem;color:#6a747f;line-height:1.5}
figcaption b{color:#3f4a56}

/* ---- callouts ---- */
.box{border-radius:10px;padding:17px 21px;margin:24px 0;font-size:.95rem;
  border:1px solid;break-inside:avoid}
.box p:first-child{margin-top:0}.box p:last-child{margin-bottom:0}
.box .h{font-weight:680;font-size:.74rem;letter-spacing:.11em;
  text-transform:uppercase;margin-bottom:7px}
.box.insight{background:#f2f7fd;border-color:#cbdcf1}.box.insight .h{color:#2f5d9e}
.box.warn{background:#fdf5f0;border-color:#f0d8c8}.box.warn .h{color:#c8542a}
.box.caveat{background:#f8f9fa;border-color:#e3e8ee}.box.caveat .h{color:#5b6673}
.box.win{background:#f1f8f4;border-color:#cbe4d6}.box.win .h{color:#33755a}

/* ---- tables ---- */
.tw{overflow-x:auto;margin:26px 0;border:1px solid #e3e8ee;border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:.87rem;background:#fff}
th{text-align:left;padding:11px 14px;background:#f7f9fb;font-weight:660;
  font-size:.76rem;letter-spacing:.055em;text-transform:uppercase;color:#404b58;
  border-bottom:1px solid #dde3ea;white-space:nowrap;vertical-align:bottom}
td{padding:10px 14px;border-bottom:1px solid #eef1f5;vertical-align:top}
tbody tr:last-child td{border-bottom:none}
tbody tr:nth-child(even) td{background:#fbfcfd}
td.num,th.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}

/* ---- evidence chips ---- */
.chip{display:inline-block;padding:1.5px 7px;border-radius:20px;font-size:.7rem;
  font-weight:670;letter-spacing:.03em;white-space:nowrap;line-height:1.5}
.c-strong{background:#e3f0e9;color:#2c6b50}
.c-mod{background:#e6eefa;color:#2b5490}
.c-weak{background:#fbeee6;color:#a8481f}
.c-none{background:#f0f1f3;color:#666d75}
.c-off{background:#eef1f5;color:#48525d}
.c-aca{background:#ece7f5;color:#5c4485}
.c-ven{background:#fbeaee;color:#993047}

/* ---- misc ---- */
.lede{font-size:1.06rem;color:#333c47}
.rule{height:1px;background:#e3e8ee;margin:44px 0;border:0}
.two{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.srcnote{font-size:.78rem;color:#8b949e;margin-top:-14px}
.footer{margin-top:56px;padding-top:22px;border-top:2px solid #12181f;
  font-size:.82rem;color:#5b6673}
code{background:#f2f4f7;padding:1px 5px;border-radius:4px;font-size:.88em;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}

@media (max-width:900px){
  .wrap{padding:0 26px}.masthead{padding:38px 26px 32px}
  .keys{grid-template-columns:repeat(2,1fr)}
  .toc ol{columns:1}.two{grid-template-columns:1fr}
  h1{font-size:1.95rem}h2{font-size:1.4rem}
}
@media print{
  body{background:#fff;font-size:10.4pt}
  .page{box-shadow:none;max-width:none}
  .wrap{padding:0 14mm}.masthead{padding:14mm 14mm 10mm}
  figure,.box,.tw,.keys{break-inside:avoid}
  h2{break-after:avoid;margin-top:26px}
  h3{break-after:avoid}
  a{color:#12181f;text-decoration:none}
  .toc{break-after:page}
}
"""


def esc(s: object) -> str:
    return escape(str(s), quote=False)


class Doc:
    """Accumulates HTML fragments and auto-numbers figures and tables."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.fig_n = 0
        self.tab_n = 0
        self.toc: list[tuple[str, str]] = []

    # -- raw -----------------------------------------------------------
    def raw(self, html: str) -> "Doc":
        self.parts.append(html)
        return self

    def p(self, text: str, cls: str = "") -> "Doc":
        c = f' class="{cls}"' if cls else ""
        return self.raw(f"<p{c}>{text}</p>")

    def h2(self, title: str, anchor: str) -> "Doc":
        self.toc.append((anchor, title))
        return self.raw(f'<h2 id="{anchor}">{esc(title)}</h2>')

    def h3(self, title: str) -> "Doc":
        return self.raw(f"<h3>{esc(title)}</h3>")

    def h4(self, title: str) -> "Doc":
        return self.raw(f"<h4>{esc(title)}</h4>")

    def ul(self, items: list[str]) -> "Doc":
        return self.raw("<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>")

    def ol(self, items: list[str]) -> "Doc":
        return self.raw("<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>")

    def box(self, kind: str, head: str, body: str) -> "Doc":
        return self.raw(
            f'<div class="box {kind}"><div class="h">{esc(head)}</div>{body}</div>'
        )

    def rule(self) -> "Doc":
        return self.raw('<hr class="rule">')

    # -- figures -------------------------------------------------------
    def fig(self, svg: str, title: str, sub: str = "", source: str = "") -> "Doc":
        self.fig_n += 1
        sub_h = f'<div class="figsub">{sub}</div>' if sub else ""
        cap = f"<figcaption>{source}</figcaption>" if source else ""
        return self.raw(
            f'<figure><div class="fignum">Figure {self.fig_n}</div>'
            f'<div class="figtitle">{esc(title)}</div>{sub_h}{svg}{cap}</figure>'
        )

    def table(self, headers: list[str], rows: list[list[str]], title: str = "",
              sub: str = "", source: str = "", num_cols: set[int] | None = None) -> "Doc":
        num_cols = num_cols or set()
        self.tab_n += 1
        th = "".join(
            f'<th class="num">{esc(h)}</th>' if i in num_cols else f"<th>{esc(h)}</th>"
            for i, h in enumerate(headers)
        )
        body = []
        for r in rows:
            tds = "".join(
                f'<td class="num">{c}</td>' if i in num_cols else f"<td>{c}</td>"
                for i, c in enumerate(r)
            )
            body.append(f"<tr>{tds}</tr>")
        head = ""
        if title:
            head = (f'<div class="fignum">Table {self.tab_n}</div>'
                    f'<div class="figtitle">{esc(title)}</div>')
            if sub:
                head += f'<div class="figsub">{sub}</div>'
        cap = f"<figcaption>{source}</figcaption>" if source else ""
        inner = (f'<div class="tw"><table><thead><tr>{th}</tr></thead>'
                 f"<tbody>{''.join(body)}</tbody></table></div>")
        if head or cap:
            return self.raw(f"<figure>{head}{inner.replace(chr(34)+'tw'+chr(34), chr(34)+'tw'+chr(34))}{cap}</figure>"
                            .replace('<figure><div class="tw"', '<figure style="padding-top:22px"><div class="tw" style="border:none;margin:0"'))
        return self.raw(inner)

    def keys(self, items: list[tuple[str, str, str]]) -> "Doc":
        cells = "".join(
            f'<div class="key"><div class="n">{esc(n)}</div>'
            f'<div class="l">{lab}</div><div class="s">{esc(src)}</div></div>'
            for n, lab, src in items
        )
        return self.raw(f'<div class="keys">{cells}</div>')

    def render_toc(self) -> str:
        lis = "".join(f'<li><a href="#{a}">{esc(t)}</a></li>' for a, t in self.toc)
        return ('<div class="toc"><h4>Contents</h4><ol>' + lis + "</ol></div>")

    def html(self, title: str, masthead: str) -> str:
        body = "".join(self.parts)
        return (
            "<!doctype html>\n<html lang=\"en\">\n<head>\n"
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f"<title>{esc(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
            f'<div class="page">{masthead}<div class="wrap">'
            f"{self.render_toc()}{body}</div></div>\n</body>\n</html>\n"
        )
