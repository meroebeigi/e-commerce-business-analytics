"""Check repository packaging and the pinned public-data/report snapshot.

Run after installing requirements. Does not fit models, execute notebooks or call Power BI.
"""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
from urllib.parse import unquote, urlsplit
import ast
import csv
import hashlib
import json
import re
import subprocess
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def validate():
    checks = {}
    tracked = subprocess.check_output(
        ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
        cwd=ROOT).decode('utf-8').split('\0')
    paths = sorted({ROOT / p for p in tracked if p and (ROOT / p).is_file()})
    python = [p for p in paths if p.suffix == '.py']
    for p in python:
        ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    checks['python_sources_parsed'] = len(python)
    for p in paths:
        if p.suffix == '.json':
            json.loads(p.read_text(encoding='utf-8'))

    markdown = [(p, p.read_text(encoding='utf-8')) for p in paths if p.suffix == '.md']
    notebooks = []
    legacy = [ROOT / 'Ecommence.ipynb', ROOT / 'docs/original_notebook.ipynb']
    assert legacy[0].read_bytes() == legacy[1].read_bytes(), 'Legacy notebook copies differ'
    for p in sorted((ROOT / 'notebooks').glob('*.ipynb')):
        nb = json.loads(p.read_text(encoding='utf-8'))
        assert nb['nbformat'] == 4
        code = [c for c in nb['cells'] if c['cell_type'] == 'code']
        assert all(c['execution_count'] is not None for c in code), p
        assert not any(o['output_type'] == 'error' for c in code for o in c['outputs']), p
        for c in code:
            ast.parse(''.join(c['source']))
        narrative = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'markdown')
        assert '../docs/project_status.md' in narrative, p
        markdown.append((p, narrative))
        notebooks.append({'notebook': p.name, 'executed_code_cells': len(code), 'stored_errors': 0})
    assert len(notebooks) == 4
    checks['notebooks'] = notebooks
    checks['legacy_notebook_copies_identical'] = True

    links = 0
    for p, text in markdown:
        for link in re.findall(r'!?\[[^\]]*\]\(([^\n]+?)\)', text):
            target = link.strip().strip('<>')
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            local = unquote(target.split('#')[0])
            assert (p.parent / local).exists(), f'Broken local link in {p}: {target}'
            links += 1
    checks['local_links_checked'] = links

    manifest = json.loads((ROOT / 'data/source_manifest.json').read_text())
    normalized_sources = []
    def verify_source(file, entry):
        content = file.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if digest != entry['sha256']:
            # Windows Git checkout can convert LF source blobs to CRLF.
            canonical = content.replace(b'\r\n', b'\n')
            assert len(canonical) == entry['bytes'], file
            assert hashlib.sha256(canonical).hexdigest() == entry['sha256'], file
            normalized_sources.append(file.relative_to(ROOT).as_posix())
        else:
            assert len(content) == entry['bytes'], file
        return digest
    for entry in manifest:
        raw = ROOT / 'archive' / entry['file']
        verify_source(raw, entry)
    checks['source_files_hash_verified'] = len(manifest)

    with (ROOT / 'powerbi/dashboard_data.csv').open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        expected = ['Purchase_month', 'Customer_state', 'GMV_BRL', 'Orders', 'Units',
                    'Eligible_deliveries', 'Late_deliveries', 'Reviewed_orders',
                    'Low_reviews', 'Returning_orders']
        assert reader.fieldnames == expected
        rows = list(reader)
    assert len(rows) == 556
    assert len({(r['Purchase_month'], r['Customer_state']) for r in rows}) == len(rows)
    def total(field, subset=rows):
        return sum((Decimal(r[field]) for r in subset), Decimal(0))
    assert total('GMV_BRL') == Decimal('13221498.11')
    assert total('Orders') == 96478 and total('Units') == 110197
    acre = [r for r in rows if r['Customer_state'] == 'AC']
    assert total('GMV_BRL', acre) == Decimal('15930.97')
    assert total('Orders', acre) == 80 and total('Units', acre) == 91
    for r in rows:
        assert 0 <= int(r['Late_deliveries']) <= int(r['Eligible_deliveries']) <= int(r['Orders'])
        assert 0 <= int(r['Low_reviews']) <= int(r['Reviewed_orders']) <= int(r['Orders'])
    checks['dashboard_snapshot'] = {'rows': len(rows), 'gmv_brl': str(total('GMV_BRL')),
                                  'orders': int(total('Orders')), 'units': int(total('Units')),
                                  'acre_filter_matches': True}

    with zipfile.ZipFile(ROOT / 'powerbi/Olist E-Commerce Performance.pbix') as z:
        assert z.testzip() is None
        names = z.namelist()
        assert 'DataModel' in names
        pages = [n for n in names if re.fullmatch(r'Report/definition/pages/[^/]+/page.json', n)]
        visuals = [n for n in names if n.endswith('/visual.json')]
        assert len(pages) == 1 and len(visuals) == 5
        definitions = [json.loads(z.read(n)) for n in visuals]
        types = sorted(v.get('visual', {}).get('visualType', 'textbox') for v in definitions)
        assert types == ['cardVisual', 'clusteredBarChart', 'lineChart', 'slicer', 'textbox'], types
        assert b'dashboard_data' in b''.join(z.read(n) for n in visuals)
    checks['pbix_package'] = {'pages': len(pages), 'visuals': len(visuals), 'visual_types': types,
                              'scope': 'ZIP and report definitions; no new Desktop/DAX execution'}

    metrics = json.loads((ROOT / 'output/model_metrics.json').read_text())
    tn, fp, fn, tp = [metrics[n] for n in ['true_negatives', 'false_positives', 'false_negatives', 'true_positives']]
    assert tn + fp + fn + tp == metrics['test_orders']
    assert abs(tp / (tp + fp) - metrics['test_precision']) < 1e-12
    assert abs(tp / (tp + fn) - metrics['test_recall']) < 1e-12
    checks['historical_model_metric_arithmetic'] = 'passed; model not refitted'

    tests = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    result = unittest.TextTestRunner(verbosity=1).run(tests)
    assert result.wasSuccessful(), 'Regression tests failed'
    checks['regression_tests_passed'] = result.testsRun

    # Optional generated evidence must not masquerade as checks run on a fresh clone.
    checks['generated_evidence'] = {}
    for name, count in [('reconciliation', 7), ('sql_reconciliation', 18)]:
        file = ROOT / 'output' / (name + '.csv')
        if file.exists():
            with file.open(encoding='utf-8', newline='') as f:
                records = list(csv.DictReader(f))
            assert len(records) == count and all(r['passed'] == 'True' for r in records)
            checks['generated_evidence'][name] = f'{count} recorded rows passed'
        else:
            checks['generated_evidence'][name] = 'not checked: generated table absent'
    if (ROOT / 'output/FactOrders.csv').exists():
        import pandas as pd
        from src.dashboard import build_dashboard_data
        f = pd.read_csv(ROOT / 'output/FactOrders.csv', dtype={
            c: 'boolean' for c in ['commercial_eligible', 'delivery_eligible',
                'review_eligible', 'is_late', 'low_review', 'is_returning']})
        actual = build_dashboard_data(f)
        pd.testing.assert_frame_equal(actual, pd.read_csv(ROOT / 'powerbi/dashboard_data.csv'),
                                      check_dtype=False, rtol=0, atol=0)
        checks['generated_evidence']['dashboard_rebuilt_from_orders'] = 'all rows matched'
    else:
        checks['generated_evidence']['dashboard_rebuilt_from_orders'] = 'not checked: FactOrders absent'
    file = ROOT / 'output/source_checksums.csv'
    if file.exists():
        with file.open(encoding='utf-8', newline='') as f:
            current = {r['file']: r for r in csv.DictReader(f)}
        for entry in manifest:
            digest = verify_source(ROOT / 'data/raw' / entry['file'], entry)
            assert current[entry['file']]['sha256'] == digest
        checks['generated_evidence']['working_input_hashes'] = '8 matched source content and recorded checksums'
    else:
        checks['generated_evidence']['working_input_hashes'] = 'not checked: checksum table absent'
    checks['crlf_normalized_source_files'] = normalized_sources
    return checks


if __name__ == '__main__':
    report = {'reviewed_at_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Repository/package checks; historical notebook outputs inspected, not re-executed',
              'checks': validate()}
    target = ROOT / 'docs/repository_validation.json'
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
