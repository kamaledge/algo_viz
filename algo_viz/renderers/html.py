# algo_viz/renderers/html.py

from html import escape

HTML_TEMPLATE = """
<html>
<head>
<style>
body {{ font-family: monospace; }}
.step {{ margin: 4px 0; }}
.call {{ color: blue; }}
.return {{ color: green; }}
.var {{ color: black; }}
</style>
</head>
<body>
<h2>Algorithm Execution Timeline</h2>
{content}
</body>
</html>
"""

def render_html(events, output="algo_viz.html"):
    rows = []

    for e in events:
        indent = "&nbsp;" * 4 * (e.depth or 0)

        if e.event_type == "call":
            args = ", ".join(f"{k}={v}" for k, v in e.new_value.items()) if isinstance(e.new_value, dict) else ""
            rows.append(
                f"<div class='step call'>{indent}[+] {e.func_name}({args})</div>"
            )
        elif e.event_type == "return":
            rows.append(
                f"<div class='step return'>{indent}[-] return {escape(str(e.new_value))}</div>"
            )
        elif e.event_type == "var_change":
            rows.append(
                f"<div class='step var'>{indent}"
                f"{e.var_name}: {escape(str(e.old_value))} -> {escape(str(e.new_value))}"
                "</div>"
            )

    html = HTML_TEMPLATE.format(content="\n".join(rows))
    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    print("[*] HTML visualization written to " + output)
