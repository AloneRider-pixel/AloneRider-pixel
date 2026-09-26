import json
import re
from pathlib import Path

readme = Path("README.md").read_text(encoding="utf-8")
manifest = json.loads(Path("profile-manifest.json").read_text(encoding="utf-8"))

required = manifest["required_sections"]
missing = [section for section in required if section not in readme]
if missing:
    raise SystemExit("Profile validation failed: " + ", ".join(missing))

for project in manifest["projects"]:
    name = project["name"]
    repository_url = project["repository_url"]
    if name not in readme:
        raise SystemExit(f"Profile validation failed: missing project '{name}'")
    if repository_url not in readme:
        raise SystemExit(f"Profile validation failed: missing repository link for '{name}'")
    for evidence_path in project.get("evidence_paths", []):
        evidence_url = f"{repository_url}/blob/main/{evidence_path}"
        if evidence_url not in readme:
            raise SystemExit(f"Profile validation failed: missing evidence link '{evidence_url}'")

urls = re.findall(r"https?://[^) >]+", readme)
if len(urls) < manifest["minimum_links"]:
    raise SystemExit(
        f"Profile validation failed: expected >={manifest['minimum_links']} links, found {len(urls)}"
    )

if "Evidence-first profile policy" not in readme:
    raise SystemExit("Profile validation failed: evidence policy section missing")

print(
    f"profile verification passed: {len(urls)} links, "
    f"{len(manifest['projects'])} traceable projects, and {len(required)} required sections"
)
