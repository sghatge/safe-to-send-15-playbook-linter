"""Lint an ops playbook (or AI skill file) before you hand it to a model.

A model follows a playbook literally. This linter checks for the four parts every
executable playbook needs, and flags vague words a model cannot act on.
Standard library only.
"""
import re
import sys

REQUIRED = {
    "trigger": r"^#+\s*(when to use|trigger|use this when)",
    "guardrails": r"^#+\s*(never|data safety|guardrails|do not)",
    "steps": r"^\s*1\.\s+\S",
    "output": r"^#+\s*(output|report|deliverable|result format)",
}
VAGUE = ["as needed", "as appropriate", "if necessary", "ensure", "properly", "etc", "and so on",
         "relevant", "best judgement", "best judgment", "where possible", "quickly"]


def lint(text):
    findings = []
    for part, pattern in REQUIRED.items():
        if not re.search(pattern, text, re.I | re.M):
            findings.append(("missing", part))
    for n, line in enumerate(text.splitlines(), 1):
        for word in VAGUE:
            if re.search(r"\b" + re.escape(word) + r"\b", line, re.I):
                findings.append(("vague", f"line {n}: '{word}' -> {line.strip()[:70]}"))
    return findings


def score(findings):
    missing = sum(1 for k, _ in findings if k == "missing")
    vague = sum(1 for k, _ in findings if k == "vague")
    return max(0, 100 - 20 * missing - 5 * vague)


def main(paths):
    worst = 100
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            f = lint(fh.read())
        s = score(f)
        worst = min(worst, s)
        print(f"{p}: {s}/100")
        for kind, detail in f:
            print(f"   {kind:<8} {detail}")
    return 0 if worst >= 80 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["examples/presend_check_before.md", "examples/presend_check_after.md"]))
