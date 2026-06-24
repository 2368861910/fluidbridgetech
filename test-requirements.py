#!/usr/bin/env python3
"""Validate FBT website against PPT requirements."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent

def read(path: str) -> str:
    return (ROOT / path.lstrip("/")).read_text(encoding="utf-8")

def check(name: str, ok: bool, detail: str = ""):
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    return ok

def main():
    html = read("index.html")
    css = read("css/fbt.css")
    theme = read("css/styles.css")
    js = read("js/scripts.js")
    all_ok = True

    masthead = html.split('class="masthead"')[1].split("</header>")[0]
    about = html.split('id="about"')[1].split('id="services"')[0]
    services = html.split('id="services"')[1].split('id="contact"')[0]
    contact = html.split('id="contact"')[1].split("<footer")[0]

    print("=== Slide 1 ===")
    all_ok &= check("1. Company logo", 'src="assets/img/logo.png"' in html)
    all_ok &= check("2. Hero title", "FLUID BRIDGE , LINK THE WORLD" in html)
    all_ok &= check("3. Blue divider element", "fbt-divider-blue" in masthead)
    all_ok &= check("3. Blue color #0055DD", "#0055DD" in css and "fbt-divider-blue" in css)
    all_ok &= check("3. Blue divider after title",
                    masthead.index("fbt-divider-blue") > masthead.index("LINK THE WORLD"))
    all_ok &= check("4. Hero description", "We supply high-quality valves and professional services！" in masthead)
    all_ok &= check("4. Welcome text", "Welcome to cooperate!" in masthead)
    all_ok &= check("5. White divider element", "fbt-divider-white" in masthead)
    all_ok &= check("5. White color #FFFFFF", "#FFFFFF" in css and "fbt-divider-white" in css)
    all_ok &= check("5. White divider below Welcome",
                    masthead.index("Welcome to cooperate!") < masthead.index("fbt-divider-white"))
    all_ok &= check("6. Hero mask 30% black", "rgba(0, 0, 0, 0.3)" in css)

    print("\n=== Slide 2 ===")
    all_ok &= check("7. About company name", "Wenzhou Fluid Bridge Valve Technology Co., Ltd." in about)
    all_ok &= check("8. About description", "FBT operates under a customer-first approach" in about)
    all_ok &= check("9. No button in about", "btn" not in about)
    all_ok &= check("10. About black background", "bg-black" in html.split('id="about"')[0][-80:])
    all_ok &= check("11-14. Four services present",
                    all(s in services for s in ["Valve Sourcing", "Quality Inspection", "Project Management", "China Office Services"]))

    print("\n=== Slide 3 ===")
    all_ok &= check("15. Nav active blue", "#0055DD" in theme)
    all_ok &= check("16. No portfolio", 'id="portfolio"' not in html)
    all_ok &= check("16. No download CTA", "Free Download" not in html)

    print("\n=== Slide 4 ===")
    all_ok &= check("17. Contact title", "Welcome for cooperation!" in contact)
    all_ok &= check("18. Black divider", "fbt-divider-black" in contact)
    all_ok &= check("19. Contact description", "We supply high-quality valves and professional services！" in contact)
    all_ok &= check("20. No form", "<form" not in contact)
    all_ok &= check("20. Contact fields", all(x in contact for x in ["Name", "Position", "E-mail", "Phone"]))
    all_ok &= check("20. Contact person", "Gamez Flor Alejandro" in contact)
    all_ok &= check("21. No phone icon", "bi-phone" not in html)
    all_ok &= check("22. Footer", "Copyright &copy; 2026" in html)

    print("\n=== Assets ===")
    all_ok &= check("fbt.css exists", (ROOT / "css/fbt.css").exists())
    all_ok &= check("No SimpleLightbox", "SimpleLightbox" not in js)
    all_ok &= check("No orange primary", "#f4623a" not in theme)

    print("-" * 40)
    print("All checks passed." if all_ok else "Some checks failed.")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
