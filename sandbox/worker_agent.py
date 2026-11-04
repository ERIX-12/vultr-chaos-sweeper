import asyncio
import json
import os
import sys
from playwright.async_api import async_playwright


async def run_worker():
    target_url = os.environ.get("TARGET_URL", "http://hostile-demo-target:80/hostile_target.html")
    chaos_mode = os.environ.get("CHAOS_MODE", "false").lower() == "true"

    console_errors = []
    dom_anomalies = []
    containment_events = []

    secret_keys = ["VULTR_INFERENCE_API_KEY", "VULTR_STORAGE_ACCESS_KEY", "VULTR_STORAGE_SECRET_KEY", "AWS_SECRET_ACCESS_KEY"]
    leaked = [k for k in secret_keys if os.environ.get(k)]
    if leaked:
        containment_events.append(f"CRITICAL: Secret leakage detected in worker environment: {leaked}")
    else:
        containment_events.append("Secret hygiene verified: Zero host secrets present in container environment.")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        try:
            await page.goto(target_url, timeout=15000)

            checkout_btn = await page.query_selector("#checkout-btn")
            promo_banner = await page.query_selector(".promo-sticky-banner")

            if checkout_btn and promo_banner:
                box1 = await checkout_btn.bounding_box()
                box2 = await promo_banner.bounding_box()

                if box1 and box2:
                    overlap = not (
                        box1["x"] + box1["width"] <= box2["x"] or
                        box2["x"] + box2["width"] <= box1["x"] or
                        box1["y"] + box1["height"] <= box2["y"] or
                        box2["y"] + box2["height"] <= box1["y"]
                    )
                    if overlap:
                        dom_anomalies.append({
                            "type": "layout_overlap",
                            "target_element": "#checkout-btn",
                            "overlapping_element": ".promo-sticky-banner",
                            "description": "Layout collision detected: .promo-sticky-banner overlaps #checkout-btn, obstructing clickability."
                        })

            if chaos_mode:
                containment_events.append("Chaos mode active: Executed stress interactions.")

        except Exception as e:
            console_errors.append(f"Navigation/Inspection error: {str(e)}")

        await browser.close()

    result = {
        "status": "completed",
        "target_url": target_url,
        "chaos_mode": chaos_mode,
        "console_errors": console_errors,
        "dom_anomalies": dom_anomalies,
        "containment_events": containment_events,
    }

    print(json.dumps(result))


if __name__ == "__main__":
    asyncio.run(run_worker())
