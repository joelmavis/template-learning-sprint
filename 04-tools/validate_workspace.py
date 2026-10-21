#!/usr/bin/env python3
"""Validate Learning Sprint structure, evidence relationships, reports, and links."""
from pathlib import Path
from html import escape
import csv
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
ERRORS=[]
for name in ('01-workspace','02-examples','03-templates','04-tools'):
    if not (ROOT/name).is_dir(): ERRORS.append(f'missing ordered directory: {name}')
for name in ('workspace','example','templates','tools'):
    if (ROOT/name).exists(): ERRORS.append(f'legacy unnumbered directory remains: {name}')
PROGRESS=['lesson_id','title','status','practice_status','mastery_status','score','completed_at','evidence_path','next_action']
MISTAKES=['mistake_id','lesson_id','concept','learner_response','feedback','status','next_review','evidence_path']
EXPECTED={'01-photography-basics':(7,7),'02-everyday-english':(14,6),'03-data-analysis-fundamentals':(30,5)}

def rows(path,fields):
    try:
        with path.open(newline='',encoding='utf-8') as handle:
            reader=csv.DictReader(handle); data=list(reader)
            if reader.fieldnames!=fields: ERRORS.append(f'{path.relative_to(ROOT)}: unexpected columns')
            return data
    except OSError:
        ERRORS.append(f'missing {path.relative_to(ROOT)}'); return []

def check_sprint(sprint,sample):
    required=['learning-plan.md','sources.md','progress.csv','mistakes.csv','knowledge.md','handoff.md','learning-report.html']
    for rel in required:
        if not (sprint/rel).is_file(): ERRORS.append(f'{sprint.relative_to(ROOT)}: missing {rel}')
    progress=rows(sprint/'progress.csv',PROGRESS); mistakes=rows(sprint/'mistakes.csv',MISTAKES)
    ids=[r['lesson_id'] for r in progress]
    if len(ids)!=len(set(ids)): ERRORS.append(f'{sprint.name}: duplicate lesson IDs')
    done=[r for r in progress if r['status']=='completed']
    for row in progress:
        path=sprint/row['evidence_path']
        if not path.is_file(): ERRORS.append(f'{sprint.name}: missing lesson {row["evidence_path"]}'); continue
        text=path.read_text(encoding='utf-8')
        if row['status']=='completed':
            for heading in ('Learning content','Practice','Learner submission','Feedback','Adaptation'):
                match=re.search(rf'^## {heading}\s*$\n(.*?)(?=^## |\Z)',text,re.M|re.S)
                if not match or not match.group(1).strip() or match.group(1).strip() in ('Not submitted.','Not reviewed.'):
                    ERRORS.append(f'{sprint.name}/{row["lesson_id"]}: incomplete {heading}')
            if row['practice_status']!='reviewed' or row['mastery_status']=='unassessed' or not row['completed_at']:
                ERRORS.append(f'{sprint.name}/{row["lesson_id"]}: completed status lacks review evidence')
    for item in mistakes:
        if item['lesson_id'] not in ids: ERRORS.append(f'{sprint.name}: {item["mistake_id"]} has unknown lesson')
        if not (sprint/item['evidence_path']).is_file(): ERRORS.append(f'{sprint.name}: {item["mistake_id"]} has missing evidence')
    report=(sprint/'learning-report.html').read_text(encoding='utf-8') if (sprint/'learning-report.html').is_file() else ''
    for phrase in ('Progress','Knowledge I Can Use','Focus Next','Next Step','Session Records','Review History','Day and Session'):
        if phrase not in report: ERRORS.append(f'{sprint.name}: report missing {phrase}')
    for row in done:
        if escape(row['title']) not in report: ERRORS.append(f'{sprint.name}: report missing completed lesson {row["lesson_id"]}')
    sample_note='Sample report · Illustrative learning record'
    if sample and report.count(sample_note)!=1: ERRORS.append(f'{sprint.name}: sample report disclosure missing')
    if not sample and sample_note in report: ERRORS.append(f'{sprint.name}: real report contains sample disclosure')
    return len(progress),len(done)

examples=ROOT/'02-examples'
if not examples.is_dir(): ERRORS.append('missing example directory')
found={p.name for p in examples.iterdir() if p.is_dir()} if examples.is_dir() else set()
if found!=set(EXPECTED): ERRORS.append(f'example inventory differs: {sorted(found)}')
for name,counts in EXPECTED.items():
    sprint=examples/name
    if sprint.is_dir():
        actual=check_sprint(sprint,True)
        if actual!=counts: ERRORS.append(f'{name}: expected {counts[1]}/{counts[0]} completed, found {actual[1]}/{actual[0]}')
for sprint in (ROOT/'01-workspace'/'sprints').iterdir():
    if sprint.is_dir(): check_sprint(sprint,False)

english=(examples/'02-everyday-english'/'sources.md')
if english.is_file():
    text=english.read_text(encoding='utf-8')
    if text.count('https://learnenglish.britishcouncil.org/')<3 or 'Accessed 2026-10-20' not in text or 'does not claim access' not in text:
        ERRORS.append('English example lacks public-source access boundary')
for rel in ('materials/course-notes.md','materials/practice-data.csv'):
    if not (examples/'03-data-analysis-fundamentals'/rel).is_file(): ERRORS.append(f'Data example missing {rel}')

for document in ROOT.rglob('*.html'):
    text=document.read_text(encoding='utf-8')
    for href in re.findall(r'href="([^"]+)"',text):
        if href.startswith(('http:','https:','#')): continue
        if not (document.parent/href.split('#')[0]).resolve().exists(): ERRORS.append(f'broken link: {document.relative_to(ROOT)} -> {href}')
for document in ROOT.rglob('*'):
    if document.is_file() and '.git' not in document.parts:
        try: text=document.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        forbidden=('PuppyOne Best '+'Practice','Best Practice '+'Template','最佳实践'+'模板')
        if any(term.lower() in text.lower() for term in forbidden): ERRORS.append(f'brand marketing phrase in {document.relative_to(ROOT)}')
        if re.search('/'+'Users'+r'/[^/]+/',text): ERRORS.append(f'absolute developer path in {document.relative_to(ROOT)}')

if ERRORS:
    print('FAILED'); print('\n'.join(ERRORS)); sys.exit(1)
print('PASSED: 3 examples; Photography 7/7, English 6/14, Data Analysis 5/30; lesson evidence, sources, reports, and links checked.')
