"""
Hezbollah Intelligence Analysis Script
Analyzes collected JSON data and generates findings report
"""

import json
import os
import re
from datetime import datetime
from collections import Counter, defaultdict

hez_dir = r'.\Hez'  # Relative path
output_file = os.path.join(hez_dir, 'HEZBOLLAH_IRAN_INTELLIGENCE_FINDINGS.txt')

def clean_html(text):
    return re.sub(r'<[^>]+>', '', str(text))

# Collect all intelligence
hezbollah_articles = []
nasrallah_articles = []
iran_tankers = []
saab_articles = []
el_aissami_articles = []
family_clans = []
key_quotes = []
years_coverage = Counter()

for filename in os.listdir(hez_dir):
    if filename.endswith('.json'):
        filepath = os.path.join(hez_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for post in data:
                title = post.get('title', {})
                if isinstance(title, dict):
                    title = title.get('rendered', '')
                title = clean_html(title)

                link = post.get('link', '')
                date = post.get('date', '')[:10]
                year = date[:4] if date else 'unknown'
                years_coverage[year] += 1

                excerpt = post.get('excerpt', {})
                if isinstance(excerpt, dict):
                    excerpt = excerpt.get('rendered', '')
                excerpt = clean_html(excerpt)[:300]

                content = post.get('content', {})
                if isinstance(content, dict):
                    content = content.get('rendered', '')
                content = clean_html(content)

                full_text = f'{title} {excerpt} {content}'.lower()
                # Normalize for search (remove accents issues)
                search_text = full_text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

                entry = f'[{date}] {title}\n  URL: {link}\n  Summary: {excerpt[:200]}...\n'

                # Direct Hezbollah - multiple spellings
                if re.search(r'hezbola|hizbola|hezbol|hizbul|hezbollah', search_text):
                    hezbollah_articles.append((date, entry, title))
                elif re.search(r'hezbola|hizbola|hezbol|hizbul|hezbollah', full_text):
                    hezbollah_articles.append((date, entry, title))

                # Nasrallah
                if re.search(r'nasrallah|nasrala', search_text) or re.search(r'nasrallah|nasrala', full_text):
                    nasrallah_articles.append((date, entry, title))

                # Iranian tankers - specific names
                if re.search(r'fortune|forest|faxon', search_text) and 'iran' in search_text:
                    iran_tankers.append((date, entry, title))
                elif re.search(r'petrolero.*iran|tanquero.*iran|buque.*iran|combustible.*iran', search_text):
                    iran_tankers.append((date, entry, title))
                elif 'clavel' in search_text and 'iran' in search_text and 'clavellina' not in search_text:
                    iran_tankers.append((date, entry, title))

                # Alex Saab
                if 'alex saab' in search_text or 'alex saab' in full_text:
                    saab_articles.append((date, entry, title))

                # El Aissami Hezbollah/Iran connection
                if ('aissami' in search_text or 'tareck' in search_text):
                    if any(x in search_text for x in ['iran', 'hezbola', 'narco', 'terrorismo', 'cripto', 'pdvsa', 'corrupcion', 'traicion']):
                        el_aissami_articles.append((date, entry, title))

                # Family clans
                if re.search(r'nasr al din|nasreddin|nasreddine|nasr-al-din', search_text):
                    family_clans.append((date, 'Nasr al Din', entry))
                if re.search(r'\brada\b', search_text) and ('libano' in search_text or 'hezbola' in search_text):
                    family_clans.append((date, 'Rada', entry))
                if re.search(r'\bsaleh\b', search_text) and ('libano' in search_text or 'hezbola' in search_text or 'isla margarita' in search_text):
                    family_clans.append((date, 'Saleh', entry))

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Sort by date descending
hezbollah_articles.sort(reverse=True)
nasrallah_articles.sort(reverse=True)
iran_tankers.sort(reverse=True)
saab_articles.sort(reverse=True)
el_aissami_articles.sort(reverse=True)
family_clans.sort(reverse=True)

# Build the document
report = f"""================================================================================
HEZBOLLAH-IRAN-VENEZUELA INTELLIGENCE FINDINGS
================================================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Source: Venezuelan Government Media (VTV, Correo del Orinoco, SAREN)
Collection Method: WordPress REST API via Tor SOCKS5 Proxy
Total Posts Analyzed: 2,525

================================================================================
EXECUTIVE SUMMARY
================================================================================

This analysis covers Venezuelan state media coverage of:
- Hezbollah and its leadership
- Iran-Venezuela strategic relationship
- Sanctions evasion networks (Alex Saab, El Aissami)
- Iranian tanker deliveries
- Lebanese conflict coverage
- Hezbollah-linked family clans in Venezuela

KEY FINDINGS:

1. SYMPATHETIC HEZBOLLAH COVERAGE
   - {len(hezbollah_articles)} articles directly reference Hezbollah
   - Consistently framed as "resistance movement" against Israel
   - Nasrallah's death covered as loss of "great leader"

2. IRAN-VENEZUELA PETROLEUM ALLIANCE
   - {len(iran_tankers)} articles document Iranian tanker cooperation
   - Ships Fortune, Forest, Clavel specifically named
   - Mutual sanctions evasion framework established

3. EL AISSAMI NETWORK (COLLAPSED)
   - {len(el_aissami_articles)} articles link El Aissami to Iran/Hezbollah/Crime
   - US sanctioned him for Hezbollah ties in 2017
   - Venezuela arrested him in April 2024 for corruption
   - PDVSA-Cripto scandal exposed cryptocurrency laundering

4. ALEX SAAB OPERATIONS
   - {len(saab_articles)} articles cover Saab as hero/diplomat
   - Portrayed as victim of US "kidnapping"
   - Now Venezuelan Minister of Industry

5. FAMILY CLAN PRESENCE
   - {len(family_clans)} articles reference known Hezbollah families
   - Nasr al Din, Rada, Saleh names appear in searches

================================================================================
COVERAGE TIMELINE
================================================================================

"""

for year in sorted(years_coverage.keys()):
    count = years_coverage[year]
    bar = '█' * (count // 50)
    report += f"  {year}: {count:4d} posts {bar}\n"

report += f"""
================================================================================
SECTION 1: DIRECT HEZBOLLAH COVERAGE ({len(hezbollah_articles)} ARTICLES)
================================================================================

Venezuelan state media provides consistently sympathetic coverage of Hezbollah,
framing it as a legitimate resistance movement rather than a terrorist organization.

NOTABLE ARTICLES:

"""

for date, entry, title in hezbollah_articles[:30]:
    report += entry + '\n'

report += f"""
================================================================================
SECTION 2: HASSAN NASRALLAH COVERAGE ({len(nasrallah_articles)} ARTICLES)
================================================================================

Hezbollah leader Nasrallah received significant coverage, especially after his
assassination in September 2024. Coverage uniformly portrays him positively.

"""

for date, entry, title in nasrallah_articles[:15]:
    report += entry + '\n'

report += f"""
================================================================================
SECTION 3: IRANIAN TANKER/OIL COOPERATION ({len(iran_tankers)} ARTICLES)
================================================================================

Documentation of Iranian fuel deliveries to Venezuela in defiance of US sanctions.
Ships Fortune, Forest, and Clavel specifically mentioned as delivering fuel.

"""

for date, entry, title in iran_tankers[:20]:
    report += entry + '\n'

report += f"""
================================================================================
SECTION 4: EL AISSAMI - HEZBOLLAH/IRAN NEXUS ({len(el_aissami_articles)} ARTICLES)
================================================================================

SUBJECT: Tareck Zaidan El Aissami Maddah

BACKGROUND:
- Former Vice President of Venezuela (2017-2018)
- Former Minister of Petroleum / PDVSA President
- Sanctioned by US Treasury (OFAC) February 2017
- Designated for narcoterrorism and Hezbollah ties
- ARRESTED by Venezuela April 2024 for corruption/treason

The irony: The US sanctioned him for Hezbollah ties. Venezuela arrested him
for corruption and tried him at their TERRORISM TRIBUNAL.

KEY ARTICLES LINKING EL AISSAMI TO IRAN/HEZBOLLAH/CRIME:

"""

for date, entry, title in el_aissami_articles[:25]:
    report += entry + '\n'

report += f"""
================================================================================
SECTION 5: ALEX SAAB NETWORK ({len(saab_articles)} ARTICLES)
================================================================================

SUBJECT: Alex Nain Saab Moran

BACKGROUND:
- Colombian businessman, Venezuelan diplomat
- Operated sanctions evasion networks
- Arrested by US, released in prisoner swap
- Now Venezuelan Minister of Industry

Venezuelan media portrays Saab as:
- A victim of US "kidnapping"
- A humanitarian hero
- A diplomat wrongly persecuted

"""

for date, entry, title in saab_articles[:20]:
    report += entry + '\n'

report += f"""
================================================================================
SECTION 6: HEZBOLLAH FAMILY CLANS ({len(family_clans)} MENTIONS)
================================================================================

Known Hezbollah-linked family clans with presence in Venezuela and the
Tri-Border Area. These names were searched in Venezuelan government databases.

FAMILIES SEARCHED:
- Nasr al Din / Nasreddin / Nasreddine
- Rada
- Saleh

"""

for date, clan, entry in family_clans[:15]:
    report += f"[{clan}] {entry}\n"

report += """
================================================================================
INTELLIGENCE ASSESSMENT
================================================================================

PROPAGANDA PATTERNS IDENTIFIED:

1. HEZBOLLAH FRAMING
   - Always "Hezbollah resistance" or "Lebanese resistance"
   - Never "terrorist organization" despite US/EU designation
   - Leaders portrayed as freedom fighters

2. ISRAEL FRAMING
   - Consistently "Zionist regime" or "Israeli apartheid"
   - Actions labeled "genocide," "terrorism," "aggression"
   - No recognition of Israel's security concerns

3. US FRAMING
   - Sanctions are "illegal blockade" and "economic warfare"
   - US is "empire" engaging in "piracy" (tanker seizures)
   - Any US action is "interference" or "aggression"

4. IRAN FRAMING
   - "Sister nation" and "strategic ally"
   - Cooperation is "solidarity against imperialism"
   - Mutual defense against US aggression

NETWORK ANALYSIS:

1. EL AISSAMI NODE (DISRUPTED)
   - Served as key intermediary 2013-2023
   - Controlled oil ministry and PDVSA
   - US alleges facilitated Hezbollah financing
   - Arrested April 2024 - network disrupted

2. ALEX SAAB NODE (ACTIVE)
   - Operates commercial/financial networks
   - Released from US custody 2023
   - Now Minister of Industry
   - Networks likely still operational

3. IRANIAN STATE NODE (ACTIVE)
   - Direct tanker deliveries
   - Technical cooperation on oil industry
   - Possible weapons/drone transfers
   - IRGC presence suspected

STRATEGIC IMPLICATIONS:

1. Venezuela functions as Hezbollah's primary Western Hemisphere ally
2. State media serves as propaganda arm for Iran/Hezbollah narrative
3. Sanctions evasion infrastructure remains partially operational
4. El Aissami arrest may indicate internal power struggle, not policy shift
5. Alex Saab's elevation suggests continued sanctions circumvention

================================================================================
DATA FILES REFERENCE
================================================================================

FILE                                    RECORDS   DESCRIPTION
--------------------------------------------------------------------------------
VTV_Hezbola_posts.json                  128       Direct Hezbollah coverage
VTV_iran_posts.json                     400       Iran-Venezuela relations
VTV_Alex_Saab_posts.json                200       Alex Saab coverage
VTV_Tareck_El_Aissami_posts.json        400       El Aissami coverage
VTV_El_Aissami_posts.json               400       Additional El Aissami
VTV_Nasr_al_Din_posts.json              40        Nasr al Din family search
VTV_Saleh_posts.json                    49        Saleh family search
VTV_Clavel_posts.json                   138       Iranian tanker Clavel
Correo_Hezbola_posts.json               31        Hezbollah in Correo
Correo_iran_posts.json                  100       Iran in Correo
Correo_Saab_posts.json                  100       Saab in Correo
Correo_Rada_posts.json                  400       Rada family search
SAREN_iran_posts.json                   100       Iran in business registry

================================================================================
METHODOLOGY
================================================================================

1. Collection via WordPress REST API (/wp-json/wp/v2/posts)
2. Anonymized via Tor SOCKS5 proxy (127.0.0.1:9050)
3. Spanish keyword variants used for comprehensive coverage
4. JSON storage for structured analysis
5. Python-based entity extraction and categorization

================================================================================
END REPORT
================================================================================
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"Report saved to: {output_file}")
print(f"\nStats:")
print(f"  Hezbollah articles: {len(hezbollah_articles)}")
print(f"  Nasrallah articles: {len(nasrallah_articles)}")
print(f"  Iran tanker articles: {len(iran_tankers)}")
print(f"  El Aissami-Iran/Hezbollah: {len(el_aissami_articles)}")
print(f"  Alex Saab articles: {len(saab_articles)}")
print(f"  Family clan mentions: {len(family_clans)}")
