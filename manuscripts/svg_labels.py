"""Read labels from SVG text or Matplotlib's outlined glyph groups."""
from pathlib import Path
import xml.etree.ElementTree as ET

def svg_labels(path):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    root = ET.fromstring(Path(path).read_text(), parser=parser)
    labels = []
    for node in root.iter():
        if not isinstance(node.tag, str):
            continue
        if node.tag.endswith('}text'):
            labels.append(''.join(node.itertext()))
        elif node.tag.endswith('}g') and node.get('id', '').startswith('text_'):
            # An annotation alone is insufficient: outlined labels need glyphs.
            has_glyphs = any(isinstance(x.tag, str) and x.tag.rsplit('}', 1)[-1] in {'use', 'path'} for x in node.iter())
            if has_glyphs:
                labels.extend(x.text.strip() for x in node if x.tag is ET.Comment and x.text and x.text.strip())
    return labels
