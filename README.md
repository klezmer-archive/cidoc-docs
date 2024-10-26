# How'd I do it?
1. Download the necessary assets from [CRMtex](https://cidoc-crm.org/extensions/crmtex/html/CRMtex_v2.0.html)
   - HTML source: view page source, copy, and paste it into crmtex.html.orig
   - `cidoc_scripts.js`: grab it from the devtools network panel
2. Prefix all the URLs in the HTML `<head>` with `https://cidoc-crm.org/`
   - We can still use them, but those links need to be fully-qualified now
4. Manually insert the AJAX-fetched schema file
   - When the page loads, it downloads an XML schema file from their server. Open the dev tools
     network tab, filter to Fetch/XHR, and refresh the page. You'll see a request to something like
     https://cidoc-crm.org/extensions/crmtex/html/CRMtex_v2.0.xml?v=20240213_122815
   - Copy the response and paste it in as the value for `xmlFile` at its declaration near the top of
     `cidoc_scripts.js`
5. CRMtex also depends on CIDOC, CRMinf, CRMSci, and FRBRoo. To get stuff from those ontologies to show up
   with names in the graph, paste their schema definitions into `xmlFile` too
   - For all of the dependency schemas *except CRMinf and FRBRoo*, there are published doc sites using the same
     tech, so those sites also AJAX in XML files:
     - https://cidoc-crm.org/html/cidoc_crm_v7.1.3.xml?v=20240213_122815
     - https://www.cidoc-crm.org/extensions/crmsci/html/CRMsci_v2.0.xml?v=20240213_122815
   - For each of these, extract their classes and properties and insert them into the appropriate
     parent tags in `xmlFile`
   - Also add `external="true"` to each of their main parent tags. This is used by some of the code
     modifications to point links at their docs sites rather than internal anchors.
   - Manually write and add class blocks to the XML for the 2-3 CRMinf and FRBRoo classes
6. Change the link in the `<head>` to point to `/cidoc_scripts.js`. To see details of the
   modifications, look at the git log
7. Run the python script on the downloaded HTML page: `python main.py crmtext.html.orig > docs/crmtex.html`

You're done!