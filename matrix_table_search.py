
#!/usr/bin/env python3
import json,time,os
from requests import post

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    print("Install: pip install rich requests")
    raise

CFG=os.path.expanduser("~/.matrix_api_config.json")
URL="https://leakosintapi.com/"
console=Console()

def load_token():
    with open(CFG,"r") as f:
        return json.load(f)["api_token"]

def collect(obj,prefix=""):
    rows=[]
    if isinstance(obj,dict):
        for k,v in obj.items():
            rows.extend(collect(v,k))
    elif isinstance(obj,list):
        for x in obj:
            rows.extend(collect(x,prefix))
    else:
        if obj not in ("",None,[],{}):
            rows.append((prefix,str(obj)))
    return rows

console.clear()
console.print(Panel.fit("🟢 MATRIX INTELLIGENCE REPORT",style="bold green"))
query=console.input("[bold green]🎯 Search Query:[/] ")

with console.status("[green]🔍 Gathering information...[/]",spinner="dots"):
    time.sleep(1)
    payload={"token":load_token(),"request":query,"limit":100,"lang":"en"}
    data=post(URL,json=payload,timeout=60).json()

rows=collect(data)

table=Table(title="📄 Filtered Results",show_lines=True)
table.add_column("Field",style="cyan",no_wrap=True)
table.add_column("Value",style="green")

seen=set()
for k,v in rows:
    if not k or v.lower() in ("null","none","[]","{}"):
        continue
    key=(k,v)
    if key in seen:
        continue
    seen.add(key)
    table.add_row(k,v)

console.print(table)
console.print(Panel(f"Useful fields shown: {len(seen)}",style="green"))
