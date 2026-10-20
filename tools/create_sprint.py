#!/usr/bin/env python3
"""Create a real Learning Sprint scaffold for an Agent to finish and teach."""
from argparse import ArgumentParser
from datetime import date
from pathlib import Path
import csv
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['lesson_id','title','status','practice_status','mastery_status','score','completed_at','evidence_path','next_action']
MISTAKES = ['mistake_id','lesson_id','concept','learner_response','feedback','status','next_review','evidence_path']

def safe_slug(value):
    value = re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')
    if not value:
        raise ValueError('title does not produce a safe slug')
    return value

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + '\n', encoding='utf-8')

def table(path, fields, rows):
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

parser = ArgumentParser()
parser.add_argument('--title', required=True)
parser.add_argument('--goal', required=True)
parser.add_argument('--mode', required=True, choices=['agent_generated','public_link','attached_files'])
parser.add_argument('--lessons', required=True, type=int)
parser.add_argument('--minutes', type=int, default=30)
parser.add_argument('--level', default='Not recorded')
parser.add_argument('--source', default='No external source supplied.')
parser.add_argument('--slug')
args = parser.parse_args()
if not 1 <= args.lessons <= 120:
    parser.error('--lessons must be between 1 and 120')

slug = safe_slug(args.slug or args.title)
target = ROOT / 'workspace' / 'sprints' / slug
if target.exists():
    raise SystemExit(f'Sprint already exists: {target.relative_to(ROOT)}')
today = date.today().isoformat()
sid = 'SPRINT-' + today.replace('-', '') + '-' + re.sub('[^A-Z0-9]', '', slug.upper())[:12]

write(target/'learning-plan.md', f'''# {args.title}

- Sprint ID: {sid}
- Goal: {args.goal}
- Source mode: {args.mode}
- Planned lessons: {args.lessons}
- Status: planned
- Current lesson: L01
- Session length: {args.minutes} minutes
- Starting level: {args.level}
- Started: {today}
- Last updated: {today}

## Success evidence

Define an observable outcome before teaching.

## Planned sequence

The Agent should replace generic titles in `progress.csv` with a goal-specific sequence and adapt later lessons after feedback.''')
write(target/'sources.md', f'''# Sources

## Source mode

`{args.mode}`

## Access record

{args.source}

The teaching Agent must record what was actually accessible and any limits before using this source.''')
rows=[]
for number in range(1,args.lessons+1):
    lid=f'L{number:02}'
    rows.append({'lesson_id':lid,'title':f'Lesson {number}','status':'ready' if number==1 else 'not_started','practice_status':'not_started','mastery_status':'unassessed','score':'','completed_at':'','evidence_path':f'lessons/day-{number:02}.md','next_action':'Prepare this lesson from the agreed goal' if number==1 else 'Wait for prior lesson review'})
    write(target/'lessons'/f'day-{number:02}.md', f'''# {lid} · Lesson {number}

- Status: {'ready' if number==1 else 'not_started'}

## Learning objectives

- Replace with an observable objective.

## Learning content

{'The Agent must replace this scaffold with a complete first lesson before teaching.' if number==1 else 'Planned outline; adapt after prior feedback.'}

## Practice

{'Prepare an observable task aligned to the objective.' if number==1 else 'Prepare after the previous lesson is reviewed.'}

## Learner submission

Not submitted.

## Feedback

Not reviewed.

## Adaptation

Continue from the earliest unfinished step.''')
table(target/'progress.csv', FIELDS, rows)
table(target/'mistakes.csv', MISTAKES, [])
write(target/'knowledge.md', '# My Knowledge\n\n## Demonstrated\n\n- None yet.\n\n## Developing\n\n- None yet.\n\n## Needs review\n\n- None yet.')
write(target/'handoff.md', f'''# Sprint Handoff

| Recorded at | Agent role | Learner evidence | Files updated | Next step |
|---|---|---|---|---|
| {today} | Planner | No practice yet. | Initial Sprint files | Replace the L01 scaffold with a complete lesson, then teach it. |''')
(ROOT/'workspace'/'active-sprint.txt').write_text(slug+'\n', encoding='utf-8')
subprocess.run([sys.executable, str(ROOT/'tools'/'build_reports.py')], check=True)
print(f'Created workspace/sprints/{slug} and set it as active.')
