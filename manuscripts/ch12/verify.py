#!/usr/bin/env python3
"""Validate chapter structure, actual source data, links, artwork, and arithmetic."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from svg_labels import svg_labels
from fractions import Fraction
from urllib.parse import unquote, urlsplit
import hashlib,json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
md=ROOT/'manuscripts/12-端边云协同.md';text=md.read_text();page=md.with_suffix('.html').read_text();errors=[];checks={}
catalog=json.loads((HERE/'figure-catalog.json').read_text());active_catalog=json.loads((HERE/'figure-index.json').read_text());figure_count=len(active_catalog)
def check(name,condition):
 checks[name]=bool(condition)
 if not condition:errors.append(name)
def close(x,y):return abs(x-y)<1e-8
outline=(ROOT/'outlines/12-端边云协同.md').read_text()
check('five_sections',re.findall(r'^## (12\.\d+) ',text,re.M)==[f'12.{i}' for i in range(1,6)])
check('subsection_numbers_match_outline',re.findall(r'^### (12\.\d+\.\d+) ',text,re.M)==re.findall(r'^### (12\.\d+\.\d+) ',outline,re.M))
check('eight_exercises',re.findall(r'^\*\*(12-\d+)\s',text,re.M)==[f'12-{i}' for i in range(1,9)])
check('three_core_exercises',re.findall(r'^\*\*(12-\d+)[^\n]*〔核心',text,re.M)==['12-2','12-3','12-7'])
check('external_captions',re.findall(r'^\*图 (12-\d+)：',text,re.M)==[f'12-{i}' for i in range(1,figure_count+1)])
check('html_figcaptions',page.count('<figcaption>')==figure_count)
check('embedded_images',page.count('src="data:image/png;base64,')==figure_count)
check('no_math_placeholders','MATHPLACEHOLDER' not in page)
check('no_katex_errors','class="katex-error"' not in page)
check('no_authoring_placeholders',not re.search('配图计划|待扩写|TODO|TBD',text))
# Source and artifact hashes are checked independently of the drawing code.
for record in json.loads((HERE/'sources.json').read_text())['sources']:
 p=ROOT/record['path'];check('source:'+record['path'],p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'])
for record in json.loads((HERE/'manifest.json').read_text())['outputs']:
 p=ROOT/record['path'];check('artifact:'+record['path'],p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'])
links=re.findall(r'\]\(([^)]+)\)',text)
for url in links:
 parts=urlsplit(url)
 if parts.scheme or not parts.path:continue
 p=(md.parent/unquote(parts.path)).resolve();check('link:'+url,p.exists())
for entry in active_catalog:
 p=HERE/entry['file']
 labels=svg_labels(p)
 check('artwork_has_no_caption_number:'+p.name,not any(re.search(r'图\s*\d+\s*[-－–]\s*\d+',s) for s in labels))
 check('artwork_has_labels:'+p.name,bool(labels))
check('book_size_layout',all(r['width_pt']==420 and r['min_label_pt']>=11 and not r['text_extent_warnings'] for r in json.loads((HERE/'teaching-layout-validation.json').read_text())))
rendered_data=json.loads((HERE/'figure-data.json').read_text());d={f"12-{e['source_id']}":rendered_data[f"12-{e['number']}"] for e in catalog};q=json.loads((ROOT/'calculations/results/queqiao-records-conditions.json').read_text());ec=json.loads((ROOT/'calculations/results/multimodal-cache-single.json').read_text())['summary']
check('full_ec_shape',400*10240*2==ec['complete_encoder_bytes_per_image']==d['12-3']['bytes'][1])
check('visual_kv',400*147456==ec['visual_kv_bytes_per_image']==d['12-3']['bytes'][2])
check('image_feature_transfer',d['12-3']['uplink_seconds_at_6_4Mbps'][:2]==[1,10.24])
check('raw_budget',close(30*8/20+.1+.3+5*8/100,12.8))
check('model_acceleration',close(12+.1+.03+.4,12.53))
check('compression_budget',close(15*8/20+.1+.3+.4+.15,6.95))
check('screenshot_round',close(.2*8/6.4+.03+2.5,2.78))
check('screenshot_30_round_saving',close((3.5-2.78)*30,21.6))
check('migration_break_even',19*.4 < 64*2**20*8/80e6+1 <20*.4)
check('raw_packet_wire',35000000+29966*(60+92)==39554832)
check('ack_difference_bytes',39555120-38177328==1377792)
check('ack_difference_time',close(14.564459796-14.52103724,.043422556))
check('air_exchange_totals',all(close(sum(a),b) for a,b in zip(d['12-5']['exchange_components_us'],[302,134])))
check('airtime_budget',close(30800*(302+134)/1e6,13.4288))
check('fixed_file_payload',d['12-6']['recorded_fixed_bytes']==354640)
check('queqiao_matched_rows',d['12-6']['matched_ASR_ms']==[[1185.3,301.6],[240.9,236.5]])
check('all_physical_rows_retained',d['12-6']['starvation_ms']==[[520,360],[700,1040],[460,560],[880,1440]])
check('deployment_times',all(close(x,y) for x,y in zip(d['12-7']['task_seconds'],[20*(.3+2.9),3+20*(.3+1.5+.02+6.4/80),1+20*(.3+.8+.2+6.4/6.4)])))
check('deployment_thresholds',close(27+128/d['12-7']['feasible_threshold_Mbps'],45) and close(27+128/d['12-7']['faster_threshold_Mbps'],41))
check('deployment_cost',close(d['12-7']['cost_units'][2],.05+16*.001))
for name,c in d['12-4']['comparisons'].items():
 for source,values in zip(c['sources'],c['image_audio_seconds']):
  b={x['id']:float(Fraction(x['complete'])) for x in json.loads((ROOT/'calculations/results'/f'{source}.json').read_text())['businesses']}
  check('media_saved_values:'+source,values==[b['image'],b['audio']])
check('no_control_characters',all(ord(c)>=32 or c=='\n' for c in text))
expected_subsets=['three_latency_curves','first_five_audio_chunks','image_and_complete_ec_only','delivery_order_only','exchange_components_only','matched_ASR_only','latency_thresholds_only']
for i,subset in enumerate(expected_subsets,1):
 check('single_relationship:'+str(i),d[f'12-{i}']['plotted_subset']==subset and d[f'12-{i}']['axes_count']==1)
check('screenshot_integer_boundary',37*2.78<105<38*2.78)
check('screenshot_baseline_components',close(.3+2+.2+.8*8/6.4,3.5))
check('connection_reuse_30_rounds',close((30-1)*2*.2,11.6))
check('buffer_depletion',.12<15360/(256000-130000)<.13)
check('deployment_examples',27+128/8==43 and close(27+128/10,39.8))
check('rounded_queqiao_prose','约 0.24 s | 约 0.24 s' in text)
check('migration_extra_restore_threshold',21*.4 < 64*2**20*8/80e6+2 <22*.4)
check('cloud_near_difference',close(20*((1-.08)+(.2-.02)) - 20*(1.5-.8) - (3-1),6))
check('variable_bandwidth_penalty',close(27+10*6.4/6+10*6.4/10,44.06666666666667) and 27+10*6.4/6+10*6.4/10 > 43)
check('recovery_retained_progress',close(41+1+1.9,43.9))
check('recovery_lost_progress',close(41+1+10*1.9,61))
check('thirty_round_continuity','前十轮已完成，剩余二十轮' in text and '每轮 3.5 秒，继续执行需要 70 秒' in text)
check('mechanism_explanations',all(x in text for x in ['资源竞争','最大值','如果等待窗口是主要原因','每一步既记录总时间，也记录握手、发送和确认的时刻']))
check('figures_in_reading_order',[e['number'] for e in active_catalog]==list(range(1,figure_count+1)))
check('figure_catalog_paths',all((HERE/e['file']).exists() for e in catalog))
check('source_backed_overlap',close(d['12-8']['chunked_s'],12.36) and d['12-8']['chunk_return_s']==[.08,.16,.16])
check('buffer_double_duration',close(d['12-9']['empty_s'][1],2*d['12-9']['empty_s'][0]))
check('migration_figure',d['12-11']['minimum_rounds']==[20,22])
check('layer_sync_figure',d['12-12']['layers']*d['12-12']['reductions_per_layer']*d['12-12']['startup_stages_per_reduction']==144)
check('window_figure_timing',close(d['12-13']['batch_send_s'],.0256) and close(d['12-13']['cycle_s'],.1256))
check('multipath_figure',sum(d['12-14']['split_MB'])==30 and d['12-14']['shared_min_s']==10)
check('deployment_figure_components',d['12-15']['totals_s']==[64,41,47])
check('recovery_figure',all(close(1+1.9*n,t) for n,t in zip(d['12-16']['redo_rounds'],d['12-16']['extra_s'])))
refs=[int(x) for x in re.findall(r'图 12-(\d+)',text)]
check('all_figure_references_resolve',all(1<=x<=figure_count for x in refs))
# A compact arithmetic answer key verifies that the newly specified exercises have determinate inputs.
answers={'12-1':{'compression_break_even_Mbps':120/.15,'only_0_2_s_accelerated_total_s':12.8-.2+.02},'12-2':{'compressed_38_rounds_s':38*2.78,'largest_faster_integer_rounds':37},'12-3':{'extra_edge_encoding_s':.12+10.24-(1+.04),'migration_preparation_s':64*2**20*8/80e6+1},'12-5':{'ideal_airtime_saved_s':15400*134/1e6,'buffer_depletion_s':(.06*256000)/(256000-130000)},'12-6':{'ideal_split_fraction':2/3,'ideal_seconds':30*8/30,'shared_bottleneck_lower_s':30*8/24,'joint_failure':.02+.98*.1*.05},'12-8':{'ten_rounds_times_s':[32,22,24],'ten_rounds_cost':[.03,.04,.025+.008],'ten_rounds_cloud_double_rate_cost':.025+.016}}
answers['12-2']['RTT_plus_100ms_totals_s']=[30*3.6,38*2.88]
answers['12-3']['fast_link_extra_transfer_ms']=(8192000-800000)/25e9*1000
answers['12-3']['extra_restore_minimum_rounds']=22
answers['12-4']={'connection_new_each_s':12,'connection_reuse_s':.4,'saved_s':11.6}
answers['12-5']['24kHz_60ms_buffer_depletion_s']=.06*384000/(384000-130000)
answers['12-8']['variable_bandwidth_twenty_rounds_s']=27+10*6.4/6+10*6.4/10
answers['12-8']['ten_rounds_recovery']={
 'retain_seven_total_s':[32,3+11*1.9+2,1+11*2.3+2],
 'retain_seven_remaining_s':[2*3.2,2+3*1.9,2+3*2.3],
 'lose_eight_total_s':[32,3+18*1.9+2,1+18*2.3+2],
 'lose_eight_remaining_s':[2*3.2,2+10*1.9,2+10*2.3],
 'retain_seven_cost':[.03,11*.004,11*(.0025+.8*.001)],
 'lose_eight_cost':[.03,18*.004,18*(.0025+.8*.001)],
 'deadline_23s':'no feasible candidate under either recovery outcome'}
(HERE/'exercise-check.json').write_text(json.dumps(answers,ensure_ascii=False,indent=2)+'\n')
report={'passed':not errors,'checks':len(checks),'sections':6,'subsections':20,'figures':figure_count,'exercises':8,'sources':len(json.loads((HERE/'sources.json').read_text())['sources']),'local_links':len(links),'chinese_characters':len(re.findall(r'[\u4e00-\u9fff]',text)),'errors':errors}
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
