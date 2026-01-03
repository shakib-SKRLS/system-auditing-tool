import platform
import subprocess
from tabulate import tabulate

dangerous_ports = ["21", "22", "23", "3389", "445"]

def run_command(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
    except:
        return ""

# ---------------- LINUX FIREWALL CHECK ----------------
def linux_firewall_audit():
    findings = []

    # 1. Firewall Status
    ufw_status = run_command("ufw status verbose")
    if "Status: active" in ufw_status:
        findings.append(("Firewall Status", "Enabled", "PASS"))
    else:
        findings.append(("Firewall Status", "Disabled", "FAIL"))

    # 2. Default Policies
    if "Default: deny (incoming)" in ufw_status:
        findings.append(("Default Incoming Policy", "DENY", "PASS"))
    else:
        findings.append(("Default Incoming Policy", "ALLOW", "FAIL"))

    if "deny (outgoing)" in ufw_status:
        findings.append(("Default Outgoing Policy", "DENY", "WARN"))
    else:
        findings.append(("Default Outgoing Policy", "ALLOW", "PASS"))

    # 3. Open Ports Check
    open_ports = run_command("ss -tuln")
    risky_ports = [p for p in dangerous_ports if p in open_ports]

    if risky_ports:
        findings.append(("Dangerous Open Ports", ", ".join(risky_ports), "FAIL"))
    else:
        findings.append(("Dangerous Open Ports", "None", "PASS"))

    # 4. Logging
    if "Logging: on" in ufw_status:
        findings.append(("Firewall Logging", "Enabled", "PASS"))
    else:
        findings.append(("Firewall Logging", "Disabled", "WARN"))

    return findings


# ---------------- WINDOWS FIREWALL CHECK ----------------
def windows_firewall_audit():
    findings = []

    fw_status = run_command("netsh advfirewall show allprofiles")

    # 1. Firewall Status
    if "State ON" in fw_status:
        findings.append(("Firewall Status", "Enabled", "PASS"))
    else:
        findings.append(("Firewall Status", "Disabled", "FAIL"))

    # 2. Default Inbound Policy
    if "Inbound connections are blocked" in fw_status:
        findings.append(("Inbound Policy", "BLOCK", "PASS"))
    else:
        findings.append(("Inbound Policy", "ALLOW", "FAIL"))

    # 3. Logging
    if "Log Allowed Connections" in fw_status:
        findings.append(("Firewall Logging", "Enabled", "PASS"))
    else:
        findings.append(("Firewall Logging", "Disabled", "WARN"))

    # 4. Open Ports (basic)
    open_ports = run_command("netstat -ano")
    risky_ports = [p for p in dangerous_ports if f":{p} " in open_ports]

    if risky_ports:
        findings.append(("Dangerous Open Ports", ", ".join(risky_ports), "FAIL"))
    else:
        findings.append(("Dangerous Open Ports", "None", "PASS"))

    return findings


# ---------------- FINAL RISK SCORING ----------------
def calculate_risk(findings):
    fail = sum(1 for f in findings if f[2] == "FAIL")
    warn = sum(1 for f in findings if f[2] == "WARN")

    if fail >= 2:
        return "HIGH"
    elif warn >= 2 or fail == 1:
        return "MEDIUM"
    else:
        return "LOW"


def firewall_security_audit():
    os_type = platform.system()

    print("\n FIREWALL SECURITY CONFIGURATION AUDIT\n")

    if os_type == "Linux":
        findings = linux_firewall_audit()
    elif os_type == "Windows":
        findings = windows_firewall_audit()
    else:
        print("Unsupported OS")
        return

    risk = calculate_risk(findings)

    print(tabulate(findings, headers=["Check", "Result", "Status"], tablefmt="grid"))
    print(f"\n OVERALL FIREWALL RISK LEVEL: {risk}\n")


if __name__ == "__main__":
    firewall_security_audit()
