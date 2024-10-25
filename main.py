import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

with open('./crmtex-site/crmtex.html') as f:
    soup = BeautifulSoup(f, features='html.parser')

# Update all the in-page fragment links to point to the local page rather than the actual CRMtex
# website
for el in soup.find_all(href=re.compile(r'^https://cidoc-crm.org/extensions/crmtex/html/CRMtex_v2.0.html')):
    el['href'] = '#' + urlparse(el['href']).fragment

for el in soup.find_all(class_='entity-first-cell'):
    # Add inheritance graph button to class and property headings
    typ = el.find(class_=['prop', 'cls'])['class'][0]
    fn = {'cls': 'searchXMLClass', 'prop': 'searchXMLProperty'}
    el_id = el.find(class_=['prop', 'cls'])['id']
    graph_el = BeautifulSoup(f"""
        <a class="graphLink" onClick="{fn[typ]}('{el_id}')" title="Display Class hierarchical Graph">
            <i class="fas fa-sitemap" aria_hidden="true" />
        </a>
    """, features='html.parser')
    
    parent = el.find('span', class_=['cls', 'prop'])
    parent.append(graph_el)

    # Add "show all properties" button
    if typ == 'cls':
        props_el = BeautifulSoup(f"""
            <a class="inheretedLink" href="javascript:void(0)"
               onclick="showInheritedPropertiesOfClass('{el_id}');"
               title="Show all direct and inherited, outgoing and incoming properties"
            >
                (show all properties)
            </a>
        """, features='html.parser')
        parent.append(props_el)

# Write the modified file out
with open('./crmtex-site/crmtex-modified.html', 'w') as f:
    f.write(soup.prettify())
