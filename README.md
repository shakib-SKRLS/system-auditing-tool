# system-auditing-tool

Small Python scripts that audit a machine's CPU/RAM and firewall state.

## Scripts
- `cpu&ram_info.py` — reports processor, physical/logical cores, CPU usage and frequency, and RAM/swap totals and usage, using `psutil` and `platform`.
- `firewall_check.py` — checks the firewall on Linux (UFW status, default policies, dangerous open ports 21, 22, 23, 3389, 445, logging) and on Windows (`netsh advfirewall`, open ports), then gives a LOW / MEDIUM / HIGH risk score.

## How to run
```bash
pip install psutil tabulate
python cpu&ram_info.py
python firewall_check.py
```

## License
MIT
