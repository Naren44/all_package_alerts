def main():
    print("🚀 Listing all OSV packages...")

    vulns = fetch_osv_vulns()

    if not vulns:
        print("❌ No vulnerabilities returned from OSV")
        return

    print(f"📊 Total vulnerabilities fetched: {len(vulns)}\n")

    for v in vulns:
        vuln_id = v.get("id", "N/A")

        affected = v.get("affected", [])
        if not affected:
            continue

        package = affected[0].get("package", {})
        name = package.get("name", "unknown")
        ecosystem = package.get("ecosystem", "unknown")

        summary = v.get("summary", "No summary")

        print("🆔 ID:", vuln_id)
        print("📦 Package:", name)
        print("🧬 Ecosystem:", ecosystem)
        print("📝 Summary:", summary)
        print("-" * 50)
