import argparse,asyncio,hashlib,json,os,random,time
from dataclasses import asdict
from pathlib import Path

def fixture(tok,rows,seed,index):
    rng=random.Random(seed)
    values=[str(rng.randrange(100000,1000000)) for _ in range(rows)]
    document='\n'.join(f'k{i:04d} = {v}' for i,v in enumerate(values))
    targets=[rows//8,rows//2,rows-rows//8-1]
    expected={f'k{i:04d}':values[i] for i in targets}
    messages=[dict(role='system',content='Read the supplied records. Return only a JSON object mapping each requested key to its exact six-digit value as a string. Do not add explanation.'),
        dict(role='user',content=f'Records:\n{document}\n\nReturn values for these keys: '+', '.join(expected))]
    ids=tok.apply_chat_template(messages,tokenize=True,return_dict=False,add_generation_prompt=True,enable_thinking=False)
    return dict(id=index,rows=rows,seed=seed,messages=messages,prompt_token_ids=ids,expected=expected)

