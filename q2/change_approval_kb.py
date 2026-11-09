"""Knowledge base for network change approval (AIMLZG557 Q2, 2025AG05066).

The facts and rules match the write-up. Forward chaining derives every fact
the rules allow and records the rule and premises behind each one, so every
answer can be explained. Device names, people and changes are illustrative.
"""

BASE_FACTS = {
    # Device roles
    ("Role", "ggn-cr-01", "CoreRouter"),
    ("Role", "ggn-cr-02", "CoreRouter"),
    ("Role", "ggn-agg-07", "AggSwitch"),
    ("Role", "ggn-olt-12", "OLT"),
    ("Role", "dli-bng-02", "BNG"),
    ("Role", "dli-olt-05", "OLT"),
    # Regions; Delhi has no Open fact because of the festive change freeze
    ("InRegion", "ggn-cr-01", "Gurugram"),
    ("InRegion", "ggn-cr-02", "Gurugram"),
    ("InRegion", "ggn-agg-07", "Gurugram"),
    ("InRegion", "ggn-olt-12", "Gurugram"),
    ("InRegion", "dli-bng-02", "Delhi"),
    ("InRegion", "dli-olt-05", "Delhi"),
    ("Open", "Gurugram"),
    # Changes and the devices they touch
    ("Targets", "CHG100", "ggn-cr-02"),
    ("Targets", "CHG101", "ggn-olt-12"),
    ("Targets", "CHG101", "ggn-agg-07"),
    ("Targets", "CHG102", "ggn-cr-01"),
    ("Targets", "CHG103", "dli-olt-05"),
    ("Targets", "CHG104", "ggn-agg-07"),
    ("Targets", "CHG105", "dli-bng-02"),
    ("FromTemplate", "CHG101"),
    ("FromTemplate", "CHG103"),
    ("FromTemplate", "CHG104"),
    # Requesters and reviewers
    ("RequestedBy", "CHG101", "Asha"),
    ("ReviewedBy", "CHG101", "Ravi"),
    ("RequestedBy", "CHG102", "Ravi"),
    ("ReviewedBy", "CHG102", "Meera"),
    ("RequestedBy", "CHG103", "Karan"),
    ("ReviewedBy", "CHG103", "Asha"),
    ("RequestedBy", "CHG104", "Meera"),
    ("ReviewedBy", "CHG104", "Meera"),
    ("RequestedBy", "CHG105", "Karan"),
    ("ReviewedBy", "CHG105", "Ravi"),
    # Approvals and plans
    ("RollbackPlan", "CHG102"),
    ("CABApproved", "CHG105"),
    ("RollbackPlan", "CHG105"),
    ("Emergency", "CHG105"),
    ("DutyManagerApproved", "CHG105"),
    # Schedule
    ("ScheduledIn", "CHG101", "NightWindow"),
    ("ScheduledIn", "CHG102", "NightWindow"),
    ("ScheduledIn", "CHG103", "NightWindow"),
    ("ScheduledIn", "CHG104", "NightWindow"),
    ("ScheduledIn", "CHG105", "EveningPeak"),
    # Config backups taken in the last 24 hours
    ("BackupFresh", "ggn-cr-01"),
    ("BackupFresh", "ggn-agg-07"),
    ("BackupFresh", "ggn-olt-12"),
    ("BackupFresh", "dli-bng-02"),
    ("BackupFresh", "dli-olt-05"),
    # Pre-change health from monitoring
    ("Reachable", "ggn-cr-01"),
    ("Reachable", "ggn-agg-07"),
    ("Reachable", "ggn-olt-12"),
    ("Reachable", "dli-bng-02"),
    ("Reachable", "dli-olt-05"),
    ("IncidentFree", "ggn-cr-01"),
    ("IncidentFree", "ggn-agg-07"),
    ("IncidentFree", "ggn-olt-12"),
    ("IncidentFree", "dli-bng-02"),
    ("IncidentFree", "dli-olt-05"),
    # Post-change check for a change already pushed last night
    ("Deployed", "CHG100"),
    ("BgpPeers", "ggn-cr-02", "Before", 4),
    ("BgpPeers", "ggn-cr-02", "After", 3),
}
# Golden-config checks: every change under review passes all three
for _c in ("CHG101", "CHG102", "CHG103", "CHG104", "CHG105"):
    BASE_FACTS |= {("NoTelnet", _c), ("NtpSet", _c), ("TacacsSet", _c)}

GATES = ("RiskCleared", "PeerReviewed", "TimeOK", "FreezeOK",
         "BackupOK", "Compliant", "PrecheckOK")


def fire(kb):
    """Yield (conclusion, rule, premises) for each rule whose premises hold."""
    has = kb.__contains__
    for fact in list(kb):
        kind = fact[0]
        if kind == "Role":
            _, d, role = fact
            rule = {"CoreRouter": "K1", "BNG": "K2", "OLT": "K3", "AggSwitch": "K4"}[role]
            cls = "CoreDevice" if role in ("CoreRouter", "BNG") else "AccessDevice"
            yield (cls, d), rule, [fact]
        elif kind == "Targets":
            _, c, d = fact
            if has(("CoreDevice", d)):
                yield ("HighRisk", c), "K5", [fact, ("CoreDevice", d)]
        elif kind == "Reachable":
            d = fact[1]
            if has(("IncidentFree", d)):
                yield ("Healthy", d), "K16", [fact, ("IncidentFree", d)]
        elif kind == "Deployed":
            c = fact[1]
            for d in targets(kb, c):
                before = [f[3] for f in kb if f[:3] == ("BgpPeers", d, "Before")]
                after = [f[3] for f in kb if f[:3] == ("BgpPeers", d, "After")]
                for n1 in before:
                    for n2 in after:
                        if n2 < n1:
                            yield ("RollbackRequired", c), "K20", [
                                fact, ("Targets", c, d), ("BgpPeers", d, "Before", n1),
                                ("BgpPeers", d, "After", n2), f"{n2} < {n1}"]

    for c in sorted({f[1] for f in kb if f[0] == "Targets"}):
        ts = targets(kb, c)
        if has(("FromTemplate", c)) and all(has(("AccessDevice", d)) for d in ts):
            yield ("Standard", c), "K6", [("FromTemplate", c)] + [("AccessDevice", d) for d in ts]
        if has(("Standard", c)):
            yield ("RiskCleared", c), "K7", [("Standard", c)]
        if has(("CABApproved", c)) and has(("RollbackPlan", c)):
            yield ("RiskCleared", c), "K8", [("CABApproved", c), ("RollbackPlan", c)]
        for x in people(kb, "RequestedBy", c):
            for y in people(kb, "ReviewedBy", c):
                if x != y:
                    yield ("PeerReviewed", c), "K9", [("RequestedBy", c, x), ("ReviewedBy", c, y), f"{x} ≠ {y}"]
        if has(("ScheduledIn", c, "NightWindow")):
            yield ("TimeOK", c), "K10", [("ScheduledIn", c, "NightWindow")]
        if has(("Emergency", c)) and has(("DutyManagerApproved", c)):
            yield ("TimeOK", c), "K11", [("Emergency", c), ("DutyManagerApproved", c)]
            yield ("FreezeOK", c), "K13", [("Emergency", c), ("DutyManagerApproved", c)]
        open_regions = []
        for d in ts:
            regions = [f[2] for f in kb if f[:2] == ("InRegion", d) and has(("Open", f[2]))]
            if not regions:
                break
            open_regions += [("InRegion", d, regions[0]), ("Open", regions[0])]
        else:
            yield ("FreezeOK", c), "K12", list(dict.fromkeys(open_regions))
        if all(has(("BackupFresh", d)) for d in ts):
            yield ("BackupOK", c), "K14", [("BackupFresh", d) for d in ts]
        checks = [("NoTelnet", c), ("NtpSet", c), ("TacacsSet", c)]
        if all(map(has, checks)):
            yield ("Compliant", c), "K15", checks
        if all(has(("Healthy", d)) for d in ts):
            yield ("PrecheckOK", c), "K17", [("Healthy", d) for d in ts]
        if all(has((g, c)) for g in GATES):
            yield ("Approved", c), "K18", [(g, c) for g in GATES]
        if has(("Approved", c)) and has(("HighRisk", c)):
            yield ("EngineerOnCall", c), "K19", [("Approved", c), ("HighRisk", c)]


def targets(kb, c):
    return sorted(f[2] for f in kb if f[0] == "Targets" and f[1] == c)


def people(kb, kind, c):
    return [f[2] for f in kb if f[0] == kind and f[1] == c]


def forward_chain(base):
    kb, why, order = set(base), {}, []
    changed = True
    while changed:
        changed = False
        for conclusion, rule, premises in list(fire(kb)):
            if conclusion not in kb:
                kb.add(conclusion)
                why[conclusion] = (rule, premises)
                order.append(conclusion)
                changed = True
    return kb, why, order


def show(fact):
    if isinstance(fact, str):
        return fact
    return f"{fact[0]}({', '.join(map(str, fact[1:]))})"


def explain(fact, why, depth=0):
    pad = "  " * depth
    if isinstance(fact, str):
        print(f"{pad}{fact}  [comparison]")
    elif fact in why:
        rule, premises = why[fact]
        print(f"{pad}{show(fact)}  [{rule}]")
        for p in premises:
            explain(p, why, depth + 1)
    else:
        print(f"{pad}{show(fact)}  [fact]")


def query1(kb, why):
    print("Q1. Is CHG101 approved for tonight's window?")
    print("Answer:", "yes" if ("Approved", "CHG101") in kb else "no")
    explain(("Approved", "CHG101"), why, 1)


def query2(kb, why):
    print("Q2. Can CHG102 be pushed tonight?")
    missing = [g for g in GATES if (g, "CHG102") not in kb]
    print("Answer:", "yes" if ("Approved", "CHG102") in kb else "no",
          "| unproved gates:", ", ".join(missing))
    print("  Standard(CHG102) proved:", ("Standard", "CHG102") in kb,
          "| CABApproved(CHG102) is a fact:", ("CABApproved", "CHG102") in kb,
          "| HighRisk(CHG102) proved:", ("HighRisk", "CHG102") in kb)


def query3(kb, why):
    print("Q3. Which changes are approved for push?")
    approved = sorted(f[1] for f in kb if f[0] == "Approved")
    print("Answer: Approved(c) for c =", ", ".join(approved))
    for c in ("CHG101", "CHG102", "CHG103", "CHG104", "CHG105"):
        gaps = [g for g in GATES if (g, c) not in kb]
        print(f"  {c}: {'approved' if not gaps else 'blocked, unproved: ' + ', '.join(gaps)}")


def query4(kb, why):
    print("Q4. Can emergency change CHG105 run during the Delhi freeze, and how?")
    print("Answer:", "yes" if ("Approved", "CHG105") in kb else "no",
          "| engineer on call:", ("EngineerOnCall", "CHG105") in kb)
    explain(("EngineerOnCall", "CHG105"), why, 1)


def query5(kb, why):
    print("Q5. Must CHG100 be rolled back?")
    print("Answer:", "yes" if ("RollbackRequired", "CHG100") in kb else "no")
    explain(("RollbackRequired", "CHG100"), why, 1)


QUERIES = {"1": query1, "2": query2, "3": query3, "4": query4, "5": query5}


def main(selected):
    """Run the queries named on the command line (e.g. 2 3), or all five."""
    kb, why, order = forward_chain(BASE_FACTS)
    print(f"Base facts: {len(BASE_FACTS)}, inference rules: 20, derived facts: {len(order)}")
    for q in selected or QUERIES:
        print()
        QUERIES[q](kb, why)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
