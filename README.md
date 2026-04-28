# leopold-briefe-preprocessing

Repo to generate basic XML/TEI for further annotating

## transkribus-out

This folder holds the XML/TEI data from the manually created Transkribus export

### how to export

* go to the [collection overview](https://app.transkribus.org/collection/2394287)
* select those documents you want to export (see [screen-001-export.png](screenshots/screen-001-export.png))
* in the [next page](https://app.transkribus.org/collection/2394287/export), select TEI and check the following options (see [export options](screenshots/screen-002-export-options.png))
  * **File name pattern**: file name
  * **Tags in export**: Export all tags in document
  * **Stylesheet**: page2tei
  * **Use rectangles**
  * **Use 'tei:ab'**
  * **Combine'continued'**
  * **Use '\tei:rs[@type]'**
* click **Start export**
* You'll get an email when the export is completed.
* Download and unzip the export-zip. Copy the folders in the zip into `transkribus-out`
