import hashlib,json
from pathlib import Path
import torch
R=Path(__file__).resolve().parent;raw=json.loads((R/'results/raw.json').read_text());checks=[]
for row in raw['rows']:
 p=R/'results'/(row['request_id']+'.pt');x=torch.load(p,map_location='cpu',weights_only=True);opt=x['optimizer'];group=opt['param_groups'][0];assert group['lr']==.001 and group['weight_decay']==0 and group['betas']==(.9,.999)
 assert x['request_id']==row['request_id'] and x['trained_output_tokens']==row['completed_training_tokens']
 for name,i in zip(['A','B'],group['params']):
  state=opt['state'][i];assert int(state['step'])==1
  assert state['exp_avg'].shape==state['exp_avg_sq'].shape==x['adapter'][name].shape
  assert torch.isfinite(state['exp_avg']).all() and torch.isfinite(state['exp_avg_sq']).all() and (state['exp_avg_sq']>=0).all()
  torch.testing.assert_close(state['exp_avg'].norm(),torch.tensor(row['gradient_norms'][name]*.1),rtol=1e-5,atol=1e-9)
  if name=='B':
   expected=-.001*(state['exp_avg']/.1)/((state['exp_avg_sq']/.001).sqrt()+group['eps'])
   torch.testing.assert_close(x['adapter'][name],expected,rtol=1e-5,atol=1e-9)
  else:assert not torch.count_nonzero(state['exp_avg']) and not torch.count_nonzero(state['exp_avg_sq'])
 checks.append(dict(request_id=row['request_id'],optimizer_step=1,moments_verified=True,adam_update_verified=True,checkpoint_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(R/'checkpoint-verification.json').write_text(json.dumps(dict(checks=checks,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n');print('12 optimizer checkpoints independently verified')
