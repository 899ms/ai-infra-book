#!/usr/bin/env python3
"""Derive the pinned static TrueType faces from Adobe's 2.005 variable font.

Usage: python make_truetype.py /path/to/SourceHanSansCN-VF.ttf
Requires fontTools. See README.md for upstream source and SHA-256.
"""
from pathlib import Path
import argparse
import hashlib
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', type=Path)
args = parser.parse_args()
expected = '25a01e41b5cc99893eb35a6cd2cc7611841dc19eb03cbaf7f0c1de8210f2ba0b'
if hashlib.sha256(args.source.read_bytes()).hexdigest() != expected:
    raise SystemExit('Source does not match the pinned Adobe 2.005 font')
for weight, value in [('Regular', 400), ('Medium', 500), ('Bold', 700)]:
    font = instantiateVariableFont(TTFont(args.source), {'wght': value}, inplace=True)
    names = {1:'Source Han Sans CN', 2:weight, 4:'Source Han Sans CN '+weight,
             6:'SourceHanSansCN-'+weight, 16:'Source Han Sans CN', 17:weight}
    for record in font['name'].names:
        if record.nameID in names:
            record.string = names[record.nameID].encode(record.getEncoding())
    font['OS/2'].usWeightClass = value
    font.save(Path(__file__).parent / f'SourceHanSansCN-{weight}.ttf')
