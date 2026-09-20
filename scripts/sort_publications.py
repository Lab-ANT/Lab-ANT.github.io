#!/usr/bin/env python3
from pathlib import Path
import re
import yaml

PATH = Path("_data/publications.yml")

def temporal_rank(pub):
    date = str(pub.get("date") or "")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        return int(date.replace("-", ""))
    return int(pub.get("year") or 0) * 10000

data = yaml.safe_load(PATH.read_text(encoding="utf-8"))
priorities = data.get("venue_priorities", {})
publications = data.get("publications", [])

warnings = []

for pub in publications:
    if not pub.get("title"):
        raise ValueError(f"Publication without title: {pub}")
    if not pub.get("year"):
        raise ValueError(f"Publication without year: {pub.get('title')}")

    if not pub.get("venue_group"):
        pub["venue_group"] = pub.get("venue_short") or "Other / Unspecified"

    venue = pub["venue_group"]
    if venue not in priorities:
        warnings.append(f"Unmapped venue priority: {venue} :: {pub['title']}")

def sort_key(pub):
    venue = pub.get("venue_group") or pub.get("venue_short") or "Other / Unspecified"
    return (
        -int(pub.get("year") or 0),
        priorities.get(venue, 90),
        venue.casefold(),
        -temporal_rank(pub),
        pub["title"].casefold(),
    )

data["publications"] = sorted(publications, key=sort_key)

header = (
    "# Display order: year descending -> venue priority -> same venue together -> date descending within venue.\n"
    "# venue_priorities are ANT Lab website display preferences, not universal academic rankings.\n"
    "# venue_short uses established/common venue abbreviations where available.\n\n"
)

PATH.write_text(
    header + yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000),
    encoding="utf-8",
)

for warning in warnings:
    print("WARNING:", warning)

print(f"Sorted {len(publications)} publications.")
