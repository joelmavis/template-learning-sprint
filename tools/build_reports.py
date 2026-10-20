#!/usr/bin/env python3
"""Build readable Learning Sprint reports and the workspace dashboard."""
from pathlib import Path
from html import escape
import csv
import os
import re

ROOT = Path(__file__).resolve().parents[1]
CSS = '''<style>:root{--ink:#26342f;--heading:#183f36;--muted:#6f746b;--line:#d9d3c5;--bg:#f3efe5;--card:#fffdf8;--accent:#a84f35;--green:#356a57;--amber:#8a5a16}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.66 "Avenir Next",Avenir,"Helvetica Neue",Arial,sans-serif}main{max-width:1020px;margin:auto;padding:38px 22px 76px}h1,h2,h3{color:var(--heading);font-family:Georgia,"Times New Roman",serif;font-weight:600}h1{font-size:clamp(32px,5vw,46px);line-height:1.12;letter-spacing:-.02em;margin:6px 0 12px}h2{margin:0 0 16px;font-size:24px}h3{margin:0 0 8px;font-size:19px}p{margin:0 0 13px}a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}code{background:#eee8dc;color:#70402f;border-radius:4px;padding:1px 4px}.eyebrow{color:var(--accent);font-size:12px;font-weight:750;letter-spacing:.13em;text-transform:uppercase}.lead{color:#4d5d56;font-size:18px;max-width:760px}.nav{display:flex;flex-wrap:wrap;gap:15px;margin:20px 0 28px}.nav a{font-weight:650}section{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:24px;margin:18px 0;box-shadow:0 5px 18px rgba(62,49,34,.045)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}.card{border:1px solid #d8d0bf;border-top:4px solid #789486;border-radius:7px;padding:17px;margin:13px 0;background:#fbf7ed}.grid .card:nth-child(2n){border-top-color:#c68162;background:#f8eee8}.grid .card:nth-child(3n){border-top-color:#8a89a8;background:#f1f0f6}.fact{background:#edf1e8;padding:13px;border-radius:6px}.fact:nth-child(2n){background:#f4e8de}.fact:nth-child(3n){background:#e8eef0}.fact:nth-child(4n){background:#f0e9f0}.label{display:block;color:#6c6258;font-size:12px;font-weight:720;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}.pill{display:inline-block;background:#ead8cf;color:#7c3d2d;border-radius:4px;padding:3px 9px;font-size:13px;font-weight:700}.good{background:#dce9df;color:var(--green)}.wait{background:#f3e3c8;color:var(--amber)}.muted{color:var(--muted)}ul{padding-left:22px}li{margin:6px 0}table{width:100%;border-collapse:collapse}th,td{padding:11px 10px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{color:#29463d;font-size:13px;background:#e7ebe3}footer{margin-top:34px;color:var(--muted);font-size:13px}@media(max-width:620px){main{padding:24px 13px 56px}section{padding:18px}.lead{font-size:17px}}</style>'''

def read_rows(path):
    with path.open(newline='',encoding='utf-8') as handle:
        return list(csv.DictReader(handle))

def meta(path):
    text=path.read_text(encoding='utf-8'); out={'title':text.splitlines()[0].lstrip('# ').strip()}
    for line in text.splitlines():
        match=re.match(r'- ([^:]+):\s*(.*)',line)
        if match: out[match.group(1).strip().lower()]=match.group(2).strip()
    return out

def section(text, name):
    match=re.search(rf'^## {re.escape(name)}\s*$\n(.*?)(?=^## |\Z)',text,re.M|re.S)
    return match.group(1).strip() if match else ''

def blocks(value):
    parts=[]; bullets=[]
    def inline(text):
        return re.sub(r'`([^`]+)`',r'<code>\1</code>',escape(text))
    def flush():
        nonlocal bullets
        if bullets:
            parts.append('<ul>'+''.join(f'<li>{inline(x)}</li>' for x in bullets)+'</ul>'); bullets=[]
    for raw in value.splitlines():
        line=raw.strip()
        if line.startswith('- '): bullets.append(line[2:])
        elif not line: flush()
        else: flush(); parts.append(f'<p>{inline(line)}</p>')
    flush()
    return ''.join(parts) or '<p class="muted">Nothing recorded.</p>'

def report(sprint, sample):
    info=meta(sprint/'learning-plan.md'); rows=read_rows(sprint/'progress.csv'); mistakes=read_rows(sprint/'mistakes.csv')
    done=[row for row in rows if row['status']=='completed']; upcoming=next((row for row in rows if row['status']!='completed'),None)
    lessons=[]
    for row in done:
        text=(sprint/row['evidence_path']).read_text(encoding='utf-8')
        lessons.append(f'''<article class="card"><h3>{escape(row['lesson_id'])} · {escape(row['title'])}</h3><p><strong>What was learned.</strong></p>{blocks(section(text,'Learning content'))}<p><strong>Practice.</strong></p>{blocks(section(text,'Practice'))}<p><strong>Learner submission.</strong></p>{blocks(section(text,'Learner submission'))}<p><strong>Feedback.</strong></p>{blocks(section(text,'Feedback'))}<p><span class="pill">{escape(row['mastery_status'].replace('_',' '))}</span> <a href="{escape(row['evidence_path'])}">Lesson record</a></p></article>''')
    mistake_html=''.join(f'''<tr><td>{escape(x['mistake_id'])}</td><td>{escape(x['concept'])}</td><td>{escape(x['learner_response'])}</td><td>{escape(x['feedback'])}</td><td>{escape(x['status'].replace('_',' '))}<br><span class="muted">{escape(x['next_review'])}</span></td></tr>''' for x in mistakes) or '<tr><td colspan="5">No mistake or review record yet.</td></tr>'
    if upcoming:
        text=(sprint/upcoming['evidence_path']).read_text(encoding='utf-8')
        next_html=f'''<h3>{escape(upcoming['lesson_id'])} · {escape(upcoming['title'])}</h3>{blocks(section(text,'Learning content'))}<p><strong>Next action.</strong> {escape(upcoming['next_action'])}</p>'''
    else:
        next_html='<h3>Sprint complete</h3><p>Review the remaining weak points, then choose a follow-on goal that uses the demonstrated skills.</p>'
    knowledge=(sprint/'knowledge.md').read_text(encoding='utf-8')
    dashboard=os.path.relpath(ROOT/'dashboard.html',sprint).replace(os.sep,'/')
    footer='Sample report · Illustrative learning record' if sample else 'Learning Sprint · Personal learning record'
    body=f'''<p class="eyebrow">Learning Report</p><h1>{escape(info['title'])}</h1><p class="lead">{escape(info.get('goal',''))}</p><nav class="nav"><a href="{dashboard}">Dashboard</a><a href="learning-plan.md">Learning plan</a><a href="sources.md">Sources</a></nav>
    <section><h2>Learning Overview</h2><div class="grid"><div class="fact"><span class="label">Source mode</span>{escape(info.get('source mode','').replace('_',' '))}</div><div class="fact"><span class="label">Progress</span>{len(done)} of {len(rows)} lessons completed</div><div class="fact"><span class="label">Starting level</span>{escape(info.get('starting level',''))}</div><div class="fact"><span class="label">Session length</span>{escape(info.get('session length',''))}</div></div><p><strong>Evidence boundary.</strong> Completed means practice was submitted and reviewed. Mastery labels reflect the recorded evidence and may still require review.</p></section>
    <section><h2>What I Learned</h2>{blocks(section(knowledge,'Demonstrated'))}<h3>Developing</h3>{blocks(section(knowledge,'Developing'))}</section>
    <section><h2>Practice &amp; Feedback</h2>{''.join(lessons) if lessons else '<p>No reviewed practice yet.</p>'}</section>
    <section><h2>Needs Review</h2>{blocks(section(knowledge,'Needs review'))}<table><tr><th>ID</th><th>Concept</th><th>Submission</th><th>Feedback</th><th>Status / next review</th></tr>{mistake_html}</table></section>
    <section><h2>Next Lesson / Next Sprint</h2>{next_html}</section>'''
    return f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(info["title"])} | Learning Report</title>{CSS}<main>{body}<footer>{footer}</footer></main></html>\n'

def dashboard(sprints):
    examples=[]
    for sprint in sorted((ROOT/'example').iterdir()):
        info=meta(sprint/'learning-plan.md'); rows=read_rows(sprint/'progress.csv'); done=sum(r['status']=='completed' for r in rows)
        examples.append(f'''<div class="card"><h3>{escape(info['title'])}</h3><p>{escape(info['goal'])}</p><p><span class="pill">{escape(info['source mode'].replace('_',' '))}</span> · {done}/{len(rows)} complete</p><p><a href="example/{escape(sprint.name)}/learning-report.html">Open learning report</a></p><p class="muted">Path: example/{escape(sprint.name)}/learning-report.html</p></div>''')
    pointer=ROOT/'workspace'/'active-sprint.txt'
    if pointer.is_file() and (ROOT/'workspace'/'sprints'/pointer.read_text(encoding='utf-8').strip()).is_dir():
        sprint=ROOT/'workspace'/'sprints'/pointer.read_text(encoding='utf-8').strip(); info=meta(sprint/'learning-plan.md'); rows=read_rows(sprint/'progress.csv'); done=sum(r['status']=='completed' for r in rows); nxt=next((r for r in rows if r['status']!='completed'),None)
        current=f'''<div class="card"><h3>{escape(info['title'])}</h3><p>{escape(info['goal'])}</p><p>{done}/{len(rows)} lessons complete</p><p><a href="workspace/sprints/{escape(sprint.name)}/learning-report.html">Open report</a></p></div>'''
        next_step=escape(nxt['next_action']) if nxt else 'Review the Sprint and choose a follow-on goal.'
        knowledge=blocks(section((sprint/'knowledge.md').read_text(encoding='utf-8'),'Demonstrated'))
    else:
        current='''<div class="card"><h3>No active Sprint yet</h3><p>Choose any starting point and say it to an agent:</p><ul><li><strong>Topic:</strong> “I want to learn photography basics in seven sessions.”</li><li><strong>Public link:</strong> “Help me study this course in 14 sessions: [URL].”</li><li><strong>Attached files:</strong> “Use the files I attached to create a learning Sprint.”</li></ul></div>'''
        next_step='Choose one prompt above. The agent will ask only for missing details, create the Sprint, and prepare the first lesson.'
        knowledge='<p>No personal knowledge record yet. It will appear after reviewed practice.</p>'
    body=f'''<p class="eyebrow">Personal learning workflow</p><h1>Learning Sprint</h1><p class="lead">Turn a topic, public course link, or attached study material into a guided learning journey.</p><section><h2>Current Sprint</h2>{current}</section><section><h2>Next Step</h2><p>{next_step}</p><p class="muted">Say this to an agent; the workflow does not depend on an HTML button.</p></section><section><h2>My Knowledge</h2>{knowledge}</section><section><h2>Examples</h2><p>These records are illustrative and are not included in personal progress.</p><div class="grid">{''.join(examples)}</div></section><section><h2>How it works</h2><p><strong>Plan → Learn → Practise → Review → Adapt.</strong> Return later or switch agents by saying, “Let’s continue my Learning Sprint.”</p><p><a href="README.md">Read the quick guide</a> · <a href="QA.md">Review tested capabilities</a></p></section>'''
    return f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Learning Sprint</title>{CSS}<main>{body}<footer>Learning Sprint · Static local dashboard</footer></main></html>\n'

def main():
    sprints=[]
    for parent,sample in ((ROOT/'example',True),(ROOT/'workspace'/'sprints',False)):
        for sprint in sorted(p for p in parent.iterdir() if p.is_dir()):
            if (sprint/'learning-plan.md').is_file():
                (sprint/'learning-report.html').write_text(report(sprint,sample),encoding='utf-8'); sprints.append(sprint)
    (ROOT/'dashboard.html').write_text(dashboard(sprints),encoding='utf-8')
    print(f'Refreshed {len(sprints)} learning reports and dashboard.html.')

if __name__=='__main__': main()
