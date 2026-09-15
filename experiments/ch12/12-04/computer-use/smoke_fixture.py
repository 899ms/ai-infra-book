"""Validate the test app itself; scripted selectors are not model-agent evidence."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
expected=dict(warehouse='East',product='USB-C Adapter',quantity=12,project='Vision Lab',delivery='Express',saved=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--no-first-run','--disable-background-networking'])
    page=browser.new_page(viewport=dict(width=1280,height=960),device_scale_factor=1)
    page.goto((R/'task.html').as_uri())
    page.get_by_role('button',name='East',exact=True).click()
    page.get_by_role('button',name='USB-C Adapter').click()
    page.get_by_label('Quantity',exact=True).fill('12')
    page.get_by_label('Project name',exact=True).fill('Vision Lab')
    page.get_by_role('button',name='Express · next day',exact=True).click()
    page.get_by_role('button',name='Save order',exact=True).click()
    state=page.evaluate('window.orderState');assert state==expected
    page.screenshot(path=str(R/'fixture-smoke-final.png'))
    (R/'fixture-smoke.json').write_text(json.dumps(dict(final_state=state,actions=page.evaluate('window.actionLog'),scope='Scripted app functional test, not Computer Use model success or a network result'),indent=2)+'\n')
    browser.close()
