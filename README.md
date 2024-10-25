# How'd I do it?
1. Download the [CIDOC](https://cidoc-crm.org/html/cidoc_crm_v7.1.3.html) and
   [CRMtex](https://cidoc-crm.org/extensions/crmtex/html/CRMtex_v2.0.html) websites
   - Open each page in private browsing. Right click anywhere on the page, click "Save As", and use
     the format "Webpage, Complete". Name it "crmtex-site".
     - Why private browsing? Some browser extensions inject stuff into the page. They're disabled
       in private browsing (usually at least) so it saves me having to manually remove that
       content.
2. Manually remove all the scripts injected by font awesome
   - For the CRMtext site, that's everything between the font awesome script and the jquery script
     in the header
3. Manually insert the AJAX-fetched schema file
   - When the page loads, it downloads an XML schema file from their server. Since we don't have a
     server and that file wasn't downloaded in "Website, Complete" bundle, we have to insert it manually.
   - Open the dev tools network tab, filter to Fetch/XHR, and refresh the page. You'll see a
     request to something like
     https://cidoc-crm.org/extensions/crmtex/html/CRMtex_v2.0.xml?v=20240213_122815
   - Copy the response. We'll paste it in the next step.
4. Reference the inserted script instead of AJAX-loading the XML schema
   - In `crmtex-site/crmtex_files/cidoc_scripts.js`, find a call to `$.ajax()` (there should only be one). Comment
     it out, retaining the call to `closeModals()` like so:
     ```js
     closeModals();
     // $.ajax({
     //     type: "GET",
     //     url: xmlUrl,
     //     dataType: "xml",
     //     error: function (e) {
     //         /*alert("An error occurred while processing XML file");*/
     //         console.log("XML reading Failed: ", e);
     
     //     },
     //     success: function (xml) {
     //         xmlFile = xml;
     //     },
     //     complete: function (data) {
     //         closeModals();
     //     }
     
     
     // });
     ```
     - It might not be strictly necessary to add the call to `closeModals()`, but better safe than sorry
   - In the same file, find the declaration of the `xmlFile` variable (search for `var xmlFile`),
     and modify it like so:
     ```js
     var xmlFile = `
       ...paste xml file copied in previous step here...
     `
     ```
5. CRMtex also depends on CIDOC, CRMinf, CRMSci, and FRBRoo. To get stuff from those ontologies to show up
   with names in the graph, paste their schema definitions into `xmlFile` too
   - For all of the dependency schemas *except CRMinf*, there are published doc sites using the same
     tech, so those sites also AJAX in XML files:
     - https://cidoc-crm.org/html/cidoc_crm_v7.1.3.xml?v=20240213_122815
     - https://www.cidoc-crm.org/extensions/crmsci/html/CRMsci_v2.0.xml?v=20240213_122815
   - For each of these, extract their classes and properties and insert them into the appropriate
     parent tags in `xmlFile`
   - Also add `external="true"` to each of their main parent tags. This is used by some of the code
     modifications to point links at their docs sites rather than internal anchors.
6. Run the python script on the downloaded HTML page
7. Use my modified `cidoc_scripts.js` (see git for changes)
8. TODO: deploy!!!