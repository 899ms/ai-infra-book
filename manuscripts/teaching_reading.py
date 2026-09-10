"""Keep diagrams at book width on narrow screens; scroll within the figure."""
import re
CSS='''
.book-diagram-scroll{max-width:100%;overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain}
.book-diagram-scroll img{display:block;width:100%;max-width:720px;height:auto;margin:12px auto}
.book-diagram-scroll:focus-visible{outline:2px solid #286b98;outline-offset:2px}
@media(max-width:650px){.book-diagram-scroll img{width:560px;min-width:560px;max-width:none}.book-diagram-scroll{scrollbar-width:thin}}
@media print{.book-diagram-scroll{overflow:visible;break-inside:avoid}.book-diagram-scroll img{width:420pt;min-width:0;max-width:100%}}
'''
def readable_diagrams(page):
    # Chapter 5 already has the approved, equivalent diagram-scroll treatment.
    if 'class="diagram-scroll"' not in page:
        page=re.sub(r'<img\b[^>]*>',lambda m:'<span class="book-diagram-scroll" style="display:block" tabindex="0" role="region" aria-label="配图；窄屏可横向滚动查看">'+m[0]+'</span>',page)
    page=page.replace('</style>',CSS+'</style>',1)
    return page
