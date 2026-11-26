from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, os, shutil, tempfile, threading
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
def main():
    screenshots=ROOT/"browser-checks";screenshots.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        shutil.copytree(ROOT/"dist",Path(temporary)/"example-tool")
        server=ThreadingHTTPServer(("127.0.0.1",0),partial(QuietHandler,directory=temporary))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=os.environ.get("CHROMIUM_EXECUTABLE"))
                page=browser.new_page(viewport={"width":1280,"height":1000})
                errors=[];requests=[]
                page.on("pageerror",lambda e:errors.append(str(e)))
                page.on("request",lambda r:requests.append(r.url))
                page.goto(f"http://127.0.0.1:{server.server_port}/example-tool/")
                page.locator("#sample").click()
                assert page.locator("#total").inner_text()=="6"
                assert page.locator("#unique").inner_text()=="5"
                page.locator("#dedupe").check()
                page.locator("#all").click()
                assert "5 selected" in page.locator("#summary").inner_text()
                with page.expect_download() as event:page.locator("#bookmarks").click()
                assert Path(event.value.path()).read_text().count("<DT><A")==5
                fixture=json.dumps({"tabs":[{"url":"https://private.invalid/account?secret=example","title":"<img src=x onerror=alert(1)>"},{"url":"javascript:alert(1)","title":"blocked"},{"url":"https://new.example/","title":"New source"}]}).encode()
                page.locator("#file").set_input_files({"name":"private-session.json","mimeType":"application/json","buffer":fixture})
                expect(page.locator("#total")).to_have_text("2")
                assert page.locator("#results img").count()==0
                assert "<img src=x" in page.locator("#results").inner_text()
                assert not any("private.invalid" in u or "new.example" in u for u in requests)
                page.locator("#search").fill("new source")
                page.locator("#all").click()
                assert "1 selected" in page.locator("#summary").inner_text()
                with page.expect_download() as event:page.locator("#json").click()
                data=json.loads(Path(event.value.path()).read_text())
                assert len(data["tabs"])==1 and data["tabs"][0]["url"]=="https://new.example/"
                page.locator("#clear").click()
                assert page.locator("#total").inner_text()=="0"
                page.locator("#sample").click()

                page.screenshot(path=str(screenshots/"desktop.png"),full_page=True)
                page.set_viewport_size({"width":390,"height":844})
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                page.screenshot(path=str(screenshots/"mobile.png"),full_page=True)
                assert not errors,errors
                browser.close()
            print("Browser checks passed: task flow, privacy, safe rendering and mobile layout")
        finally:server.shutdown()
if __name__=="__main__":main()
