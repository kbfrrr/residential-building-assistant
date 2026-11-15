"""Install either temporary validation or final nightly answer-check schedule."""
import argparse
import os
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schedule", choices=["validation", "nightly"], required=True)
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise SystemExit("Run with sudo python3 install.py --schedule validation")
    script = Path(__file__).resolve().with_name("quality_check.py")
    if not script.is_file() or " " in str(script):
        raise SystemExit("Extract bundle under /opt/residential-assistant/quality first")
    service = ("[Unit]\nDescription=Check three residential assistant answers and email results\n"
               "After=docker.service network-online.target\nWants=network-online.target\nRequires=docker.service\n\n"
               "[Service]\nType=oneshot\nUser=root\nUMask=0077\n"
               f"ExecStart=/usr/bin/python3 {script}\nTimeoutStartSec=8min\n")
    timing = ("OnActiveSec=2min\nOnUnitActiveSec=5min\n" if args.schedule == "validation"
              else "OnCalendar=*-*-* 18:15:00 UTC\nPersistent=true\n")
    timer = (f"[Unit]\nDescription=Residential answer check ({args.schedule})\n\n[Timer]\n"
             + timing + "AccuracySec=1s\nUnit=residential-quality.service\n\n[Install]\nWantedBy=timers.target\n")
    directory = Path("/etc/systemd/system")
    (directory / "residential-quality.service").write_text(service, encoding="utf-8")
    (directory / "residential-quality.timer").write_text(timer, encoding="utf-8")
    for arguments in (["daemon-reload"], ["enable", "residential-quality.timer"],
                      ["restart", "residential-quality.timer"]):
        subprocess.run(["systemctl", *arguments], check=True)
    print("Answer-check timer enabled: " + args.schedule)
    subprocess.run(["systemctl", "list-timers", "residential-quality.timer", "--all", "--no-pager"], check=True)


if __name__ == "__main__":
    main()
