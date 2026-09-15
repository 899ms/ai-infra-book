import hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--no-first-run','--disable-background-networking'])
    page=browser.new_page(viewport=dict(width=1280,height=960),device_scale_factor=1)
    page.goto((R/'task.html').as_uri());page.screenshot(path=str(R/'initial.png'))
    state=page.evaluate('window.orderState')
    assert state==dict(warehouse='West',product='HDMI Cable',quantity=1,project='',delivery='Standard',saved=False)
    (R/'browser-readiness.json').write_text(json.dumps(dict(browser_version=browser.version,viewport=[1280,960],initial_state=state,html_sha256=hashlib.sha256((R/'task.html').read_bytes()).hexdigest(),screenshot_sha256=hashlib.sha256((R/'initial.png').read_bytes()).hexdigest(),scope='Isolated browser and initial task only; no agent task or network experiment completed'),indent=2)+'\n')
    browser.close()
