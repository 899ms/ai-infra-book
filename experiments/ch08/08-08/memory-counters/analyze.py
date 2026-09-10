import csv,hashlib,json
from pathlib import Path
r=Path(__file__).absolute().parent;reports=[]
for x in json.loads((r/'reference/index.json').read_text()):assert hashlib.sha256((r/x['file']).read_bytes()).hexdigest()==x['sha256']
for name in ['bf16','fp8']:
 run=json.loads((r/'results'/name/'run.json').read_text());ref=json.loads((r/'reference'/name/'kv-snapshots.json').read_text());env=json.loads((r/'reference'/name/'environment.json').read_text())
 for n,h in run['sources'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
 assert run['input_sha256']==hashlib.sha256((r/'reference'/name/'inputs.json').read_bytes()).hexdigest()
 expected=dict(env['config']);expected['worker_extension_cls']='trace_probe.TraceProbe';assert expected==run['config']
 assert run['weights']==ref['weights']
 assert run['kv_before'][0]['scales']==run['kv_after'][0]['scales']==ref['after_calibration'][0]['scales']
 assert run['request']['prompt_tokens']==7239 and len(run['request']['output_ids'])==2
 if name=='bf16':reference_weights=run['weights']
 else:assert run['weights']==reference_weights
 rows=list(csv.DictReader((r/f'{name}.csv').open()));assert len(rows)==2
 units,data=rows;assert data['Kernel Name']=='kernel_unified_attention'
 assert data['Grid Size']=='(1, 8, 16)' and data['Block Size']=='(128, 1, 1)'
 metrics={}
 for key,unit in [('dram__bytes_op_read.sum','byte'),('dram__bytes_op_write.sum','byte'),('lts__t_bytes.sum','byte'),('gpu__time_duration.sum','ns')]:
  assert units[key]==unit,(key,units[key]);metrics[key]=float(data[key].replace(',',''));assert metrics[key]>=0
 report=dict(format=name,kernel=data['Kernel Name'],grid=data['Grid Size'],block=data['Block Size'],metrics=metrics,
  replay_passes=int(data['profiler__replayer_passes']),warmup_passes=int(data['profiler__replayer_passes_type_warmup']),
  request_output_ids=run['request']['output_ids'],scope='First decode-layer unified-attention body only; 16 segments; subsequent reduction excluded.')
 reports.append(report);print(json.dumps(report))
(r/'summary.json').write_text(json.dumps(dict(reports=reports,scope='Actual hardware counters; shared GPU, cache-control none, clock-control none. Do not multiply by layers or equate to end-to-end bytes/time.'),indent=2)+'\n')
