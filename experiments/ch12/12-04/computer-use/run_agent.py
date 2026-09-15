import base64,hashlib,json,time,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent;O=R/'agent-results'
TASK='Save an order for 12 USB-C Adapters, warehouse East, project Vision Lab, Express delivery.'
CONTRACT='You control the browser using only the current screenshot. Complete this task: '+TASK+' Return exactly one JSON object, no markdown or explanation. Allowed actions: {"action":"click","x":number,"y":number}, {"action":"type","text":"value"}, {"action":"key","key":"Tab|Enter|Backspace|Escape"}, {"action":"done"}. Click coordinates are normalized 0 to 1000 across the screenshot width and height. Type replaces the contents of the currently focused input field. Click an input before typing. Take one action per response. Use done only after the order has been saved correctly.'
TARGET=dict(warehouse='East',product='USB-C Adapter',quantity=12,project='Vision Lab',delivery='Express',saved=True)
def infer(png,instruction,rid,cap=160):
 req=dict(id=rid,image=base64.b64encode(png).decode(),instruction=instruction,max_tokens=cap);start=time.monotonic()
 with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:19308/generate',data=json.dumps(req).encode(),headers={'Content-Type':'application/json'}),timeout=300) as f:response=json.load(f)
 return dict(request_start_s=start,response_end_s=time.monotonic(),request_instruction=instruction,response=response)
def main():
 O.mkdir(exist_ok=False)
 with sync_playwright() as p:
  for trial in range(3):
   D=O/f'trial{trial}';D.mkdir();browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--no-first-run','--disable-background-networking']);page=browser.new_page(viewport=dict(width=1280,height=960),device_scale_factor=1);page.goto((R/'task.html').as_uri());history=[];start=time.monotonic();reason='action_limit'
   try:
    if trial==0:
     png=page.screenshot();(O/'warmup.json').write_text(json.dumps(infer(png,CONTRACT,'warmup',1),indent=2)+'\n')
     start=time.monotonic()
    for step in range(16):
     t=time.monotonic();png=page.screenshot();shot=D/f'step{step:02d}.png';shot.write_bytes(png);shot_end=time.monotonic();instruction=CONTRACT+'\nPrevious actions: '+json.dumps(history)
     record=dict(trial=trial,step=step,screenshot_start_s=t,screenshot_end_s=shot_end,screenshot_sha256=hashlib.sha256(png).hexdigest(),**infer(png,instruction,f't{trial}-s{step}'))
     try:
      action=json.loads(record['response']['text']);kind=action['action'];record['action_start_s']=time.monotonic()
      if kind=='click':
       assert set(action)=={'action','x','y'} and 0<=action['x']<=1000 and 0<=action['y']<=1000
       page.mouse.click(action['x']*1280/1000,action['y']*960/1000)
      elif kind=='type':
       assert set(action)=={'action','text'} and isinstance(action['text'],str) and len(action['text'])<=100
       page.keyboard.press('Meta+A');page.keyboard.insert_text(action['text'])
      elif kind=='key':
       assert set(action)=={'action','key'} and action['key'] in ['Tab','Enter','Backspace','Escape'];page.keyboard.press(action['key'])
      elif kind=='done':assert set(action)=={'action'}
      else:raise ValueError('unsupported action')
      record['action']=action;history.append(action);record['action_end_s']=time.monotonic()
     except Exception as e:record['action_error']=repr(e);reason='invalid_action'
     (D/f'step{step:02d}.json').write_text(json.dumps(record,indent=2)+'\n');print(trial,step,record.get('action',record.get('action_error')),flush=True)
     if 'action_error' in record:break
     # Oracle is used to terminate/evaluate only. It is never included in model input.
     if page.evaluate('window.orderState')==TARGET:reason='target_reached';break
     if kind=='done':reason='model_done';break
    state=page.evaluate('window.orderState');page.screenshot(path=str(D/'final.png'));result=dict(trial=trial,reason=reason,passed=state==TARGET,final_state=state,target=TARGET,elapsed_s=time.monotonic()-start,actions=history,browser_version=browser.version,oracle_log=page.evaluate('window.actionLog'))
    (D/'result.json').write_text(json.dumps(result,indent=2)+'\n')
   finally:browser.close()
if __name__=='__main__':main()
