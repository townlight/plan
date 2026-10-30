# SPDX-License-Identifier: AGPL-3.0-only
"""Planning public exploration acceptance on real PostgreSQL + real browser.

Synthetic fictional plan sources only. Bounded: one disposable PostgreSQL
cluster, Planning's own migrations, a real Planning HTTP process, real HTTP
exploration, and a real Chromium browsing the public page.

    <venv>\\python.exe -B accept_plan_public.py <run-root>
"""
from pathlib import Path
import json
import os
import socket
import secrets as _secrets
import subprocess
import sys
import time

import httpx
import psycopg2

TASK = Path(__file__).resolve().parents[3]
PLAN = TASK / 'work/beta-products/plan'
CORE = TASK / 'work/beta-foundations/core'
PG = TASK / 'work/station-boundary/postgres/bin'
PYTHON = Path(sys.executable)
NODE = r'C:/Users/scott/scoop/apps/nodejs-lts/current/node.EXE'
ROOT = Path(sys.argv[1]).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
BROWSER = TASK / 'work/beta-products/plan/browser-plan-explore.cjs'
_pw = _secrets.token_hex(16)
PASSWORD = _pw
checks = []
children = []
env = {k: v for k, v in os.environ.items()
       if not k.startswith(('CIVIC', 'TOWNLIGHT', 'DATABASE', 'PG', 'OLLAMA', 'PLANNING'))}
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['PYTHONPATH'] = os.pathsep.join(map(str, [PLAN, CORE, PLAN / 'tests']))


def save(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2, default=str), encoding='utf-8')


def passed(name):
    checks.append(name)
    save('checks.json', checks)
    print('PASS:', name, flush=True)


def port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def start(name, args, custom_env=None):
    log = (ROOT / (name + '.log')).open('a', encoding='utf-8')
    process = subprocess.Popen(list(map(str, args)), env=custom_env or env, stdout=log,
        stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
    children.append((name, process, log))
    save('owned-jobs.json', [{'name': n, 'pid': p.pid, 'terminal': p.poll()}
                             for n, p, _ in children])
    return process


def command(name, args, custom_env=None, timeout=110):
    with (ROOT / (name + '.log')).open('w', encoding='utf-8') as log:
        result = subprocess.run(list(map(str, args)), env=custom_env or env, stdout=log,
            stderr=subprocess.STDOUT, timeout=timeout, creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode:
        raise RuntimeError(f'{name} exited {result.returncode}; see retained log')


def stop(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)


def ready(url, process, expected=200):
    for _ in range(150):
        if process.poll() is not None:
            raise RuntimeError('process exited before readiness; inspect log')
        try:
            if httpx.get(url, timeout=1, trust_env=False).status_code == expected:
                return
        except httpx.HTTPError:
            pass
        time.sleep(.2)
    raise RuntimeError('readiness timed out')


def main():
    pgport, planport = port(), port()
    PGDATA = ROOT / 'pgdata'
    save('endpoints.json', {'postgres': pgport, 'planning': planport})
    if not PGDATA.exists():
        pw = ROOT / 'pg-password.txt'
        pw.write_text(PASSWORD, encoding='ascii')
        command('initdb', [PG / 'initdb.exe', '-D', PGDATA, '-U', 'plan_admin',
            '-A', 'scram-sha-256', '--pwfile', pw, '--encoding=UTF8', '--locale=C'])
        pw.unlink()
    pg = start('postgres', [PG / 'postgres.exe', '-D', PGDATA, '-h', '127.0.0.1',
        '-p', pgport, '-c', 'shared_buffers=64MB', '-c', 'max_connections=40'])
    admin = None
    try:
        for _ in range(120):
            try:
                admin = psycopg2.connect(host='127.0.0.1', port=pgport, user='plan_admin',
                    password=PASSWORD, dbname='postgres')
                break
            except psycopg2.OperationalError:
                if pg.poll() is not None:
                    raise
                time.sleep(.25)
        else:
            raise RuntimeError('disposable PostgreSQL did not start')
        admin.autocommit = True
        with admin.cursor() as cursor:
            cursor.execute('CREATE DATABASE planning_public OWNER plan_admin')
        admin.close()
        url = f'postgresql+psycopg2://plan_admin:{PASSWORD}@127.0.0.1:{pgport}/planning_public'
        penv = {**env, 'CIVICPLAN_POLICY_DB_URL': url, 'CIVICPLAN_STAFF_API_KEY': 'plan-fixture-key'}

        command('planning-migrate', [PYTHON, '-B', '-m', 'civicplan.migrations'], custom_env=penv)
        passed('Planning source schema migrated in disposable PostgreSQL')

        command('planning-seed', [PYTHON, '-B', PLAN / 'accept_plan_public_seed.py', str(ROOT)],
                custom_env=penv)
        passed('two adopted public plans and one staff-only plan imported as persisted sources')

        planning = start('planning-http', [PYTHON, '-B', '-c',
            'import uvicorn;from civicplan.main import app;'
            f'uvicorn.run(app,host="127.0.0.1",port={planport},log_level="warning")'],
            custom_env=penv)
        base = f'http://127.0.0.1:{planport}'
        ready(base + '/health', planning)
        with httpx.Client(base_url=base, timeout=30, trust_env=False) as client:
            explore = client.get('/api/v1/civicplan/public/plan-explore')
            if explore.status_code != 200:
                raise RuntimeError('explore API failed: ' + explore.text[:400])
            payload = explore.json()
            if payload['total'] < 2:
                raise RuntimeError('persisted public policies not explored: ' + json.dumps(payload)[:400])
            plan_ids = sorted({plan['plan_id'] for plan in payload['plans']})
            if 'redstone-internal' in plan_ids:
                raise RuntimeError('a staff-only plan leaked into public exploration')
            passed('real HTTP public exploration returns persisted adopted public policies only')

            query = client.get('/api/v1/civicplan/public/plan-explore',
                               params={'q': 'transit'})
            matched = query.json()
            if matched['total'] < 1 or 'transit' not in json.dumps(matched).casefold():
                raise RuntimeError('keyword exploration did not match persisted text')
            passed('keyword exploration matches persisted plan text and cites it')

            goal = client.get('/api/v1/civicplan/public/plan-explore',
                              params={'goal': 'Housing choice'})
            if goal.json()['total'] < 1:
                raise RuntimeError('goal filter did not use persisted goals')
            passed('goal filter resolves through persisted plan goals')

            empty = client.get('/api/v1/civicplan/public/plan-explore',
                               params={'q': 'heliport'}).json()
            if empty['total'] != 0 or not empty['empty_reason']:
                raise RuntimeError('unsupported exploration did not fail explicitly')
            passed('an unsupported exploration returns an explicit empty state, not a guess')

            # Non-public denial: a staff-only revision id cannot be reached.
            denied = client.get('/api/v1/civicplan/public/policy/'
                                f'{payload["plans"][0]["revision_id"]}/INTERNAL-1')
            if denied.status_code != 404:
                raise RuntimeError('nonpublic policy was reachable: ' + denied.text[:200])
            passed('a non-public policy/revision is denied to the public surface (404)')

            page = client.get('/civicplan')
            if page.status_code != 200 or 'Fictional' not in page.text:
                raise RuntimeError('public page did not render persisted sources')
            if 'Housing proposal context' in page.text:
                raise RuntimeError('static sample text survived on the page')
            passed('the public page is rendered from persisted sources, with no static sample')

        result = subprocess.run([NODE, str(BROWSER), base, str(ROOT / 'browser')],
            capture_output=True, text=True, timeout=110)
        (ROOT / 'browser-plan.log').write_text((result.stdout or '') + (result.stderr or ''),
                                              encoding='utf-8')
        print(result.stdout or '', flush=True)
        if result.returncode:
            raise RuntimeError(f'planning browser acceptance exited {result.returncode}')
        passed('a real browser explores the persisted plan, filters, and sees the empty state')
        save('result.json', {'checks': checks, 'explore_total': payload['total'],
                             'plan_ids': plan_ids})
        print(json.dumps({'checks': len(checks)}))
    finally:
        if admin is not None:
            try:
                admin.close()
            except Exception:
                pass
        for name, process, log in reversed(children):
            stop(process)
            log.close()
        save('owned-jobs.json', [{'name': n, 'pid': p.pid, 'returncode': p.poll()}
                                 for n, p, _ in children])
        survivors = [n for n, p, _ in children if p.poll() is None]
        if survivors:
            raise RuntimeError('owned child processes still running: ' + ', '.join(survivors))


if __name__ == '__main__':
    main()
