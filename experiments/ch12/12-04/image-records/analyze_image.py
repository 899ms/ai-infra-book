import hashlib,json,shutil,statistics
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent
platforms={};pixels={}
for label,folder in [('mac',R/'mac-results'),('rtx',R/'rtx-results/run')]:
    env=json.loads((folder/'environment.json').read_text())
    assert env['source_sha256']==hashlib.sha256((R/'run_image.py').read_bytes()).hexdigest()
    assert env['input_sha256']==hashlib.sha256((R/'iss030e122639.NEF').read_bytes()).hexdigest()
    rows=json.loads((folder/'requests.json').read_text())
    assert len(rows)==4 and [r['warmup'] for r in rows]==[True,False,False,False]
    assert json.loads((folder/'completion.json').read_text())['requests']==4
    with Image.open(folder/'developed.png') as im:pixels[label]=np.array(im.convert('RGB'))
    for row in rows:
        assert row['start_ns']<=row['loaded_ns']<=row['developed_ns']<=row['encoded_ns']<=row['written_ns']
        data=(folder/f"trial{row['trial']}.jpg").read_bytes()
        assert len(data)==row['output_bytes'] and hashlib.sha256(data).hexdigest()==row['jpeg_sha256']
        with Image.open(folder/f"trial{row['trial']}.jpg") as im:
            im.load();decoded=np.array(im.convert('RGB'))
        assert list(decoded.shape)==row['shape']==list(pixels[label].shape)
        assert hashlib.sha256(decoded.tobytes()).hexdigest()==row['decoded_sha256']
        assert hashlib.sha256(pixels[label].tobytes()).hexdigest()==row['rgb_sha256']
        mse=float(np.mean((pixels[label].astype(np.float32)-decoded.astype(np.float32))**2))
        assert abs(mse-row['jpeg_mse'])<1e-6
    assert len({row['jpeg_sha256'] for row in rows})==len({row['rgb_sha256'] for row in rows})==1
    formal=rows[1:]
    platforms[label]=dict(environment=env,libraw_flags=json.loads((R/(label+'-libraw-flags.json')).read_text()),
        processing_s=[(r['written_ns']-r['start_ns'])/1e9 for r in formal],
        median_processing_s=statistics.median((r['written_ns']-r['start_ns'])/1e9 for r in formal),
        jpeg_bytes=formal[0]['output_bytes'],jpeg_psnr_db=formal[0]['jpeg_psnr_db'],shape=formal[0]['shape'],jpeg_sha256=formal[0]['jpeg_sha256'])
assert pixels['mac'].shape==pixels['rtx'].shape
diff=np.abs(pixels['mac'].astype(np.int16)-pixels['rtx'].astype(np.int16))
comparison=dict(rgb_equal=bool(np.array_equal(pixels['mac'],pixels['rtx'])),
    differing_channel_values=int(np.count_nonzero(diff)),max_abs_channel_difference=int(diff.max()),
    jpeg_equal=platforms['mac']['jpeg_sha256']==platforms['rtx']['jpeg_sha256'])
assert (R/'process-container-after.txt').read_text()==''
shutil.copyfile(R/'rtx-results/run/trial1.jpg',R/'final.jpg')
fixture=dict(upload_file='iss030e122639.NEF',response_file='final.jpg',
    upload_sha256=hashlib.sha256((R/'iss030e122639.NEF').read_bytes()).hexdigest(),response_sha256=hashlib.sha256((R/'final.jpg').read_bytes()).hexdigest(),
    service_s=platforms['rtx']['median_processing_s'],shape=platforms['rtx']['shape'],
    decoded_sha256=json.loads((R/'rtx-results/run/requests.json').read_text())[1]['decoded_sha256'],
    source_sha256={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['run_image.py','source.json','rtx-results/run/environment.json','rtx-results/run/requests.json']},
    scope='Real full-resolution RAW/final-JPEG and measured warm RTX CPU service replay; not neural inference')
(R/'image-fixture.json').write_text(json.dumps(fixture,indent=2)+'\n')
(R/'image-summary.json').write_text(json.dumps(dict(status='Eight complete CPU RAW-development executions verified',platforms=platforms,cross_platform=comparison,fixture=fixture),indent=2)+'\n')
print(json.dumps(dict(platforms={k:{x:v[x] for x in ['processing_s','jpeg_bytes','jpeg_psnr_db','libraw_flags']} for k,v in platforms.items()},cross_platform=comparison),indent=2))
