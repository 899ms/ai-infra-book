import argparse,hashlib,io,json,os,platform,time
from pathlib import Path
import numpy as np
import rawpy
from PIL import Image
import PIL

R=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
out=a.output;out.mkdir(exist_ok=False)
source=json.loads((R/'source.json').read_text())
raw_file=R/source['file']
assert hashlib.sha256(raw_file.read_bytes()).hexdigest()==source['sha256']
params=dict(use_camera_wb=True,no_auto_bright=True,exp_shift=1.25,output_bps=8,user_flip=0,gamma=(2.222,4.5))
environment=dict(platform=platform.platform(),machine=platform.machine(),python=platform.python_version(),
    omp_num_threads=os.environ.get('OMP_NUM_THREADS'),
    rawpy=rawpy.__version__,libraw=list(rawpy.libraw_version),numpy=np.__version__,pillow=PIL.__version__,
    source_sha256=hashlib.sha256((R/'run_image.py').read_bytes()).hexdigest(),input_sha256=source['sha256'],
    params=params,demosaic='AHD',color_space='sRGB',jpeg=dict(quality=95,subsampling=0,optimize=False,progressive=False),scope='CPU RAW development, not neural inference')
(out/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
records=[]
for trial in range(4):
    start=time.perf_counter_ns()
    with rawpy.imread(str(raw_file)) as raw:
        loaded=time.perf_counter_ns()
        rgb=raw.postprocess(demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD,output_color=rawpy.ColorSpace.sRGB,**params)
        developed=time.perf_counter_ns()
        sizes=raw.sizes._asdict()
    buffer=io.BytesIO();Image.fromarray(rgb).save(buffer,format='JPEG',quality=95,subsampling=0,optimize=False,progressive=False)
    data=buffer.getvalue();encoded=time.perf_counter_ns()
    target=out/f'trial{trial}.jpg';target.write_bytes(data);written=time.perf_counter_ns()
    with Image.open(io.BytesIO(data)) as image:
        image.load();decoded=np.array(image.convert('RGB'))
    assert rgb.dtype==np.uint8 and rgb.ndim==3 and rgb.shape[2]==3 and decoded.shape==rgb.shape
    mse=float(np.mean((rgb.astype(np.float32)-decoded.astype(np.float32))**2))
    record=dict(trial=trial,warmup=trial==0,start_ns=start,loaded_ns=loaded,developed_ns=developed,encoded_ns=encoded,written_ns=written,
        shape=list(rgb.shape),raw_sizes=sizes,input_bytes=raw_file.stat().st_size,output_bytes=len(data),
        jpeg_sha256=hashlib.sha256(data).hexdigest(),rgb_sha256=hashlib.sha256(rgb.tobytes()).hexdigest(),decoded_sha256=hashlib.sha256(decoded.tobytes()).hexdigest(),
        jpeg_mse=mse,jpeg_psnr_db=None if mse==0 else float(10*np.log10(255**2/mse)),
        channel_min=rgb.min(axis=(0,1)).tolist(),channel_max=rgb.max(axis=(0,1)).tolist())
    records.append(record)
    (out/'requests.json').write_text(json.dumps(records,indent=2)+'\n')
    if trial==0:
        Image.fromarray(rgb).save(out/'developed.png')
        preview=Image.fromarray(rgb);preview.thumbnail((1400,1000));preview.save(out/'preview.png')
    print(trial,record['shape'],len(data),(written-start)/1e9,record['jpeg_psnr_db'],flush=True)
(out/'completion.json').write_text(json.dumps(dict(requests=4))+'\n')
