"""Three heuristic regression checks, not the formal 15-question evaluation."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import time
import uuid

TOPIC = "arn:aws:sns:ap-southeast-1:125035824720:residential-assistant-alerts"
REGION = "ap-southeast-1"
MODEL = "gemini-3.6-flash"
CASES = [
    ("pool_monday", "Can I use the swimming pool on Monday?"),
    ("gym_hours", "What time does the gym open and close?"),
    ("unknown_parking_fee", "What is the fee for replacing a lost parking sticker?"),
]
NODE = r"""
const fs=require('fs');
const question=JSON.parse(fs.readFileSync(0,'utf8')).question;
fetch('http://gateway:8000/v1/chat/completions',{
  method:'POST', signal:AbortSignal.timeout(75000),
  headers:{'Content-Type':'application/json',Authorization:'Bearer '+process.env.RESIDENT_GATEWAY_KEY},
  body:JSON.stringify({model:'gemini-3.6-flash',stream:false,messages:[{role:'user',content:question}]})
}).then(async response=>{
  const data=await response.json();
  console.log(JSON.stringify({status:response.status,answer:response.ok ? data.choices?.[0]?.message?.content || '' : ''}));
}).catch(()=>{console.log(JSON.stringify({status:0,answer:'',error:'Request failed or timed out'}));process.exitCode=1});
"""


def judge(case_id, status, answer):
    if status != 200 or not isinstance(answer, str) or not answer.strip():
        return False
    text = answer.lower()
    if case_id == "pool_monday":
        return "monday" in text and "closed" in text and not re.search(r"open\s+(?:on\s+)?mondays?\b", text)
    if case_id == "gym_hours":
        return bool(re.search(r"\b0?6(?::00)?\s*a\.?m\.?", text)
                    and re.search(r"\b10(?::00)?\s*p\.?m\.?", text))
    if case_id == "unknown_parking_fee":
        missing = re.search(r"(?:not|doesn.t|does not)\s+(?:specif\w*|list\w*|provid\w*|mention\w*)", text)
        price = re.search(r"(?:[$₱€£]\s*\d|\b\d+(?:\.\d+)?\s*(?:pesos?|dollars?|php|usd)\b|\bfree\b)", text)
        return bool(missing and "office" in text and not price)
    return False


def ask(question):
    started = time.monotonic()
    result = subprocess.run(["docker", "exec", "-i", "residential-api-1", "node", "-e", NODE],
                            input=json.dumps({"question": question}), capture_output=True,
                            text=True, timeout=90)
    if result.returncode:
        return {"status": 0, "answer": "", "error": "Request command failed"}
    response = json.loads(result.stdout)
    response["duration_ms"] = round((time.monotonic() - started) * 1000)
    return response


def main():
    if os.geteuid() != 0:
        raise SystemExit("Run with sudo python3 quality_check.py")
    os.umask(0o077)
    import fcntl
    with open("/run/residential-quality.lock", "w") as guard:
        fcntl.flock(guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
        started = datetime.now(timezone.utc)
        run_id = started.strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
        results = []
        for case_id, question in CASES:
            try:
                response = ask(question)
            except Exception:
                response = {"status": 0, "answer": "", "error": "Request unavailable or invalid response"}
            results.append({"id": case_id, "question": question, **response,
                            "heuristic_pass": judge(case_id, response.get("status"), response.get("answer"))})
        passed = sum(row["heuristic_pass"] for row in results)
        folder = Path("/var/lib/residential-quality/results")
        folder.mkdir(parents=True, exist_ok=True, mode=0o700)
        path = folder / (run_id + ".json")
        report = {"run_id": run_id, "started_utc": started.isoformat(),
                  "completed_utc": datetime.now(timezone.utc).isoformat(), "model": MODEL,
                  "heuristic_passes": passed, "total": len(results), "results": results,
                  "scope": "Internal authenticated gateway/model/content checks; excludes browser login and public TLS. Heuristics require human review; not formal quality score.",
                  "notification_sent": False}
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        message = (f"Residential assistant scheduled answer check\nRun: {run_id}\n"
                   f"Completed UTC: {report['completed_utc']}\nHeuristic checks passed: {passed}/{len(results)}\n"
                   "Cases: " + ", ".join(row["id"] + (" PASS" if row["heuristic_pass"] else " REVIEW") for row in results)
                   + "\nRaw answers saved privately on EC2. This is a heuristic regression check, not the formal project evaluation.")
        published = subprocess.run(["/usr/local/bin/aws", "sns", "publish", "--topic-arn", TOPIC,
                                    "--subject", f"SAM10 answer check: {passed}/{len(results)}", "--message", message,
                                    "--region", REGION, "--no-cli-pager"], capture_output=True, text=True, timeout=90)
        if published.returncode:
            print(json.dumps({"event": "quality_notification_failed", "run_id": run_id, "report": str(path)}))
            return 1
        report["notification_sent"] = True
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"event": "quality_check_completed", "run_id": run_id,
                          "heuristic_passes": passed, "total": len(results), "notification_sent": True,
                          "report": str(path), "completed_utc": report["completed_utc"]}))
        return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
