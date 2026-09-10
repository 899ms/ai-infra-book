"""Compare manifested full workloads; this is reporting, not independent acceptance."""
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F

ROOT=Path(__file__).resolve().parent

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        while chunk:=stream.read(1048576):h.update(chunk)
    return h.hexdigest()


def main():
    inputs=json.loads((ROOT/'book-inputs.json').read_text())
    common=None
    for value in inputs.values():
        normalized=copy.deepcopy(value)
        normalized['application']['scheduling']['send']='CONTROLLED'
        normalized['network']['ack_policy']='CONTROLLED'
        if common is None:common=normalized
        assert common==normalized,'undeclared difference between comparison inputs'
    rows=[]
    fingerprints=[]
    for name in ['image-baseline',*inputs]:
        stem='book-'+name
        manifest=json.loads((ROOT/'runs'/f'{stem}-manifest.json').read_text())
        assert manifest['status']=='COMPLETE_STABLE_IDENTITY_NOT_INDEPENDENT_ACCEPTANCE'
        assert manifest['pilot'] is False
        assert manifest['source_hashes_before']==manifest['source_hashes_after']
        fingerprints.append(manifest['source_hashes_before'])
        for path_key,hash_key in [('result_file','result_sha256'),('summary_file','summary_sha256'),('effective_input_file','effective_input_sha256')]:
            assert digest(ROOT/manifest[path_key])==manifest[hash_key]
        summary=json.loads((ROOT/manifest['summary_file']).read_text())
        by_kind={b['kind']:b for b in summary['businesses']}
        image=by_kind['image']
        tts=by_kind.get('tts',{})
        screenshot=by_kind.get('screenshot',{})
        rows.append(dict(case=name,wire_bytes=summary['summary']['wire_bytes'],packets=summary['transmission_count'],received_bytes=summary['summary']['unique_received_application_bytes'],delivered_bytes=summary['summary']['delivered_application_bytes'],image_complete_at=image['complete_at'],image_complete_seconds=float(F(image['complete_at'])) if image['complete_at'] is not None else None,first_play=tts.get('first_play'),missing_audio_seconds=tts.get('missing_audio_seconds'),screenshot_usable=screenshot.get('usable'),all_messages_delivered=summary['summary']['all_messages_delivered'],businesses=summary['businesses'],result_sha256=manifest['result_sha256']))
    assert all(f==fingerprints[0] for f in fingerprints),'runs used different source identities'
    report=dict(status='manifested_results_compared_not_independent_acceptance',controlled_differences=['application.scheduling.send','network.ack_policy'],source_hashes=fingerprints[0],rows=rows)
    (ROOT/'book-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    lines=['# 完整媒体业务条件比较','', '固定同一业务 DAG；四格只改变发送调度与 ACK 策略。这里汇总实际运行的完整轨迹，不替代独立验收。取消、过期与版本失效须同时查看业务质量记录。','', '| 场景 | 包数 | 线上 B | 完整图片 s | 首次播放 s | 缺音 s | 截图可用 |','| --- | ---: | ---: | ---: | ---: | ---: | --- |']
    for r in rows:
        play='—' if r['first_play'] is None else str(float(F(r['first_play'])))
        missing='—' if r['missing_audio_seconds'] is None else str(float(F(r['missing_audio_seconds'])))
        usable='—' if r['screenshot_usable'] is None else ('是' if r['screenshot_usable'] else '否')
        lines.append(f"| {r['case']} | {r['packets']} | {r['wire_bytes']} | {r['image_complete_seconds']} | {play} | {missing} | {usable} |")
    lines+=['','单图片保留原 25 KB 业务块边界，分片及封装成本与合并成一个连续字节数组的旧基线不同。不能把该差异解释成拥塞控制收益。','']
    (ROOT/'BOOK-COMPARISON.md').write_text('\n'.join(lines))
    print(json.dumps({r['case']:{k:r[k] for k in ('packets','wire_bytes','image_complete_seconds','first_play','screenshot_usable')} for r in rows},indent=2))

if __name__=='__main__':main()
