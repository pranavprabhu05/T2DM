"""Export a deterministic, standalone HTML fallback; no server or CDN required."""
from __future__ import annotations

import argparse
import hashlib
from html import escape
import json
from pathlib import Path

from demo.core import (COHORTS, FROZEN_COMMIT, TABLES, contracts, example_sample,
                       load_table, verify_sources)


def build_report() -> str:
    manifest = verify_sources()
    configs, panels = contracts()
    payload = {
        "configs": configs,
        "panels": panels,
        "samples": {cohort: example_sample(cohort, "full") for cohort in COHORTS},
        "tables": {key: {"title": title, "source": path, "meaning": meaning,
                         "rows": {c: load_table(key, c) for c in COHORTS}}
                   for key, (title, path, meaning) in TABLES.items()},
    }
    data = json.dumps(payload, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    return """<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'">
<title>T2DM · Offline research demo</title>
<style>
body{font:16px system-ui,sans-serif;color:#15314c;background:#f5f8fc;margin:0}
main{max-width:1180px;margin:auto;padding:36px 24px}h1{font-size:2.4rem;letter-spacing:-.04em}
.kicker{font-size:.8rem;letter-spacing:.15em;color:#17695d;font-weight:700}
.notice{background:#e6f2ee;border-left:4px solid #22776a;padding:16px;line-height:1.6}
section{background:white;border:1px solid #dce4ef;border-radius:12px;padding:24px;margin:20px 0}
select,button{font:inherit;padding:8px;border:1px solid #9eafc3;border-radius:6px;margin:6px}
button:disabled{color:#697b8e}label{display:inline-block;margin:5px 16px 5px 0}
#fields{display:flex;flex-wrap:wrap;gap:4px;margin-top:16px}#fields label{font-size:.85rem;background:#edf3f8;padding:7px;border-radius:5px}
table{border-collapse:collapse;font-size:.8rem;width:100%}td,th{border:1px solid #dce4ef;padding:8px;text-align:left;white-space:nowrap}
th{background:#eaf0f7;position:sticky;top:0}.scroll{overflow:auto;max-height:540px}.source,small{color:#536780;font-size:.8rem}
#decision{font-weight:650;line-height:1.7}code{overflow-wrap:anywhere}footer{font-size:.8rem;color:#536780}
@media print{.scroll{overflow:visible;max-height:none}#fields{display:none}section{break-inside:avoid}}
</style><main>
<div class="kicker">T2DM / SELF-CONTAINED OFFLINE FALLBACK</div>
<h1>Feature availability in practice</h1>
<p class="notice">Saved internal-validation evidence and synthetic schema examples. Fitted models/calibrators are absent; live probabilities and individual predictions are unavailable. Four distinct endpoints; no clinical interpretation or cross-cohort pooling.</p>
<label>Cohort <select id="cohort"></select></label><p id="endpoint"></p>
<section><h2>Feature availability explorer</h2>
<p>Synthetic, already encoded fields; no patient record or outcome. Check which fields are observed.</p>
<label>Example <select id="example"><option value="full">All fields observed</option><option value="minimal">Smallest panel</option><option value="unsupported">Insufficient fields</option></select></label>
<label>Request <select id="scenario"></select></label>
<div id="fields"></div><p id="decision" role="status" aria-live="polite"></p>
<button disabled>Predict · validated artifacts unavailable</button>
<p>Availability abstention is distinct from retrospective confidence rejection. Supported eligibility does not establish a fitted family, calibration map or probability.</p></section>
<section><h2>Saved experiments &amp; results</h2><label>Experiment <select id="experiment"></select></label>
<p id="meaning"></p><p class="source" id="source"></p><p id="count"></p><div class="scroll"><table id="results"></table></div>
<p>Blank saved cells remain blank. Dynamic switching did not establish consistent Holm-corrected superiority over the robust fixed family. Selective metrics must be read with observation/event coverage and excluded prevalence.</p></section>
<section><h2>Evidence boundary</h2>
<p>Original routing chooses the largest fully supported native panel, then its development-selected fitted model/map. Original classification threshold: fixed 0.5. No model is trained or loaded by this report.</p>
<p>Confidence rejection ranks evaluation cases by 2 × |calibrated probability − 0.5|, retaining groups together when present. It does not provide a validated single-sample confidence cutoff.</p>
<p>Masked-input stress, reduced-schema refits, natural runtime policies and repeat summaries are different experiments. Better accepted-case scores do not establish improved whole-population performance. Repeat SD is descriptive, not a confidence interval.</p>
<p>Release: v1.0.0-paper · commit <code>""" + escape(FROZEN_COMMIT) + """</code><br>Version DOI: 10.5281/zenodo.23537932<br>Verified source hashes at export: """ + str(len(manifest["sha256"])) + """</p>
</section><footer>This HTML contains its own data and scripts. It needs no network, Python environment or running server to open.</footer>
<script type="application/json" id="evidence">""" + data + """</script>
<script>
'use strict';
const D=JSON.parse(document.getElementById('evidence').textContent);
const el=id=>document.getElementById(id);
function option(select,value,label){const o=document.createElement('option');o.value=value;o.textContent=label;select.append(o);}
Object.keys(D.samples).forEach(c=>option(el('cohort'),c,c==='brfss'?'BRFSS 2015':c==='hospital130'?'Hospital130':c==='pidd'?'PIDD':'Sylhet'));
Object.entries(D.tables).forEach(([k,t])=>option(el('experiment'),k,t.title));
function setup(){
 const c=el('cohort').value,cfg=D.configs[c];
 el('endpoint').textContent=cfg.display_name+' · '+cfg.endpoint;
 el('scenario').replaceChildren();option(el('scenario'),'auto','Automatic · largest supported panel');
 Object.keys(D.panels[c].scenarios).forEach(s=>option(el('scenario'),s,s));
 examples();results();
}
function examples(){
 const c=el('cohort').value,cfg=D.configs[c],sc=D.panels[c].scenarios;
 const ordered=Object.keys(sc).sort((a,b)=>sc[a].available_features.length-sc[b].available_features.length||(a<b?-1:a>b?1:0));
 const kind=el('example').value;
 const observed=kind==='full'?Object.keys(D.samples[c]):kind==='minimal'?sc[ordered[0]].available_features:[cfg.numeric_features[0]];
 el('fields').replaceChildren();
 Object.entries(D.samples[c]).forEach(([f,v])=>{const label=document.createElement('label'),box=document.createElement('input');
 box.type='checkbox';box.value=f;box.checked=observed.includes(f);box.onchange=decision;
 label.append(box,document.createTextNode(' '+f+' = '+v));el('fields').append(label);});decision();
}
function decision(){
 const c=el('cohort').value,sc=D.panels[c].scenarios,req=el('scenario').value;
 const avail=new Set(Array.from(el('fields').querySelectorAll('input:checked')).map(b=>b.value));
 const supported=Object.keys(sc).filter(s=>sc[s].available_features.every(f=>avail.has(f)));
 // Ascending tuple order matches the original router's max(len, is_full, name).
 supported.sort((a,b)=>sc[a].available_features.length-sc[b].available_features.length||Number(a==='full')-Number(b==='full')||(a<b?-1:a>b?1:0));
 if(req!=='auto'&&!supported.includes(req))el('decision').textContent='ABSTAIN · required_scenario_features_missing: '+sc[req].available_features.filter(f=>!avail.has(f)).join(', ');
 else if(!supported.length)el('decision').textContent='ABSTAIN · no_supported_feature_panel';
 else el('decision').textContent='Supported panel · '+(req==='auto'?supported[supported.length-1]:req)+' · eligibility only; no model prediction';
}
function results(){
 const c=el('cohort').value,t=D.tables[el('experiment').value],rows=t.rows[c];
 el('meaning').textContent=t.meaning;el('source').textContent='Frozen source: '+t.source;
 el('count').textContent=rows.length+' saved rows · '+D.configs[c].endpoint;
 const table=el('results');table.replaceChildren();
 if(!rows.length){el('count').textContent='No saved rows for this cohort/experiment.';return;}
 const fields=Object.keys(rows[0]),head=document.createElement('thead'),hr=document.createElement('tr');
 fields.forEach(f=>{const th=document.createElement('th');th.scope='col';th.textContent=f;hr.append(th);});head.append(hr);table.append(head);
 const body=document.createElement('tbody');rows.forEach(r=>{const tr=document.createElement('tr');fields.forEach(f=>{const td=document.createElement('td');td.textContent=r[f];tr.append(td);});body.append(tr);});table.append(body);
}
el('cohort').onchange=setup;el('example').onchange=examples;el('scenario').onchange=decision;el('experiment').onchange=results;setup();
</script></main></html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("outputs/panel-demo.html"))
    args = parser.parse_args()
    report = build_report().encode("utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as handle:
        handle.write(report)
    print(f"Offline report: {args.output.resolve()}\nSHA-256: {hashlib.sha256(report).hexdigest()}")


if __name__ == "__main__":
    main()
