#!/usr/bin/env python3
import sys, json, urllib.request

try:
    alert_file = sys.argv[1]
    # Dynamically grab the webhook URL to prevent crash on parameter shifts
    hook_url = sys.argv[3] if len(sys.argv) > 3 else sys.argv[2]

    # Strip incompatible slack endpoints to allow native JSON embedding
    if hook_url.endswith("/slack"):
        hook_url = hook_url[:-6]

    with open(alert_file) as f:
        alert = json.load(f)

    r = alert.get("rule", {})
    lvl = int(r.get("level", 0))
    # Dynamic color coding based on severity level
    clr = 16711680 if lvl >= 10 else (16753920 if lvl >= 5 else 65280)
    log = str(alert.get("full_log", "No log provided"))[:1000]
    ticks = chr(96) * 3

    payload = {
        "username": "Wazuh SIEM",
        "embeds": [{
            "title": "Level {} - {}".format(lvl, r.get("description", "Alert")),
            "color": clr,
            "fields": [
                {"name": "Rule ID", "value": str(r.get("id", "N/A")), "inline": True},
                {"name": "Agent", "value": str(alert.get("agent", {}).get("name", "Manager")), "inline": True},
                {"name": "Log", "value": ticks + "\n" + log + "\n" + ticks, "inline": False}
            ]
        }]
    }

    req = urllib.request.Request(
        hook_url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "Wazuh"}
    )
    urllib.request.urlopen(req)

except Exception as e:
    sys.stderr.write("Discord Error: " + str(e) + "\n")
    sys.exit(1)
