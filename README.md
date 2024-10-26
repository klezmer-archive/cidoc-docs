# How'd I do it?
1. Download the necessary assets from [CRMtex](https://cidoc-crm.org/extensions/crmtex/html/CRMtex_v2.0.html)
   - HTML source: view page source, copy, and paste it into crmtex.html.orig
   - JS TODO
2. Prefix all the URLs in the HTML `<head>` with `https://cidoc-crm.org/`
   - We can still use them, but those links need to be fully-qualified now
4. Manually insert the AJAX-fetched schema file
   - When the page loads, it downloads an XML schema file from their server. Since we don't have a
     server and that file wasn't downloaded in "Website, Complete" bundle, we have to insert it manually.
   - Open the dev tools network tab, filter to Fetch/XHR, and refresh the page. You'll see a
     request to something like
     https://cidoc-crm.org/extensions/crmtex/html/CRMtex_v2.0.xml?v=20240213_122815
   - Copy the response. We'll paste it in the next step.
5. Reference the inserted script instead of AJAX-loading the XML schema
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
6. CRMtex also depends on CIDOC, CRMinf, CRMSci, and FRBRoo. To get stuff from those ontologies to show up
   with names in the graph, paste their schema definitions into `xmlFile` too
   - For all of the dependency schemas *except CRMinf*, there are published doc sites using the same
     tech, so those sites also AJAX in XML files:
     - https://cidoc-crm.org/html/cidoc_crm_v7.1.3.xml?v=20240213_122815
     - https://www.cidoc-crm.org/extensions/crmsci/html/CRMsci_v2.0.xml?v=20240213_122815
   - For each of these, extract their classes and properties and insert them into the appropriate
     parent tags in `xmlFile`
   - Also add `external="true"` to each of their main parent tags. This is used by some of the code
     modifications to point links at their docs sites rather than internal anchors.
7. Change the link in the `<head>` to point to `/cidoc_scripts.js`. To see details of the
   modifications, look at the git log
8. Run the python script on the downloaded HTML page: `python main.py crmtext.html.orig > docs/crmtex.html`