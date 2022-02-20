


from multipagesave import Layer, MultipageSave

def test_find_layers():

   ext = MultipageSave()
   ext.options.ids = []  # overwrite parser args
   ext.load(TEST_SVG)  # load test SVG document

   layers = ext.find_layers()

   assert len(layers) == 3

   assert layers["layer1"].label == "layer 1 (locked)"
   assert layers["layer1"].locked == True
   assert layers["layer2"].label == "layer 2"
   assert layers["layer2"].locked == False
   assert layers["layer3"].label == "layer 3"
   assert layers["layer3"].locked == False


TEST_SVG = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1"
   id="svg5"
   inkscape:version="1.1.2 (b8e25be8, 2022-02-05)"
   sodipodi:docname="example.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview7"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="0.41519421"
     inkscape:cx="415.46822"
     inkscape:cy="788.78749"
     inkscape:window-width="1383"
     inkscape:window-height="907"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="0"
     inkscape:current-layer="layer3" />
  <defs
     id="defs2" />
  <g
     inkscape:label="layer 1 (locked)"
     inkscape:groupmode="layer"
     id="layer1"
     sodipodi:insensitive="true">
    <text
       xml:space="preserve"
       style="font-size:36.0153px;line-height:1.25;font-family:calibri;-inkscape-font-specification:calibri;stroke-width:0.900385"
       x="56.402206"
       y="107.41101"
       id="text167"><tspan
         sodipodi:role="line"
         id="tspan165"
         style="stroke-width:0.900385"
         x="56.402206"
         y="107.41101">Page 1</tspan></text>
  </g>
  <g
     inkscape:groupmode="layer"
     id="layer2"
     inkscape:label="layer 2">
    <text
       xml:space="preserve"
       style="font-size:36.0153px;line-height:1.25;font-family:calibri;-inkscape-font-specification:calibri;stroke-width:0.900385"
       x="56.428585"
       y="156.37862"
       id="text167-7"><tspan
         sodipodi:role="line"
         id="tspan165-5"
         style="stroke-width:0.900385"
         x="56.428585"
         y="156.37862">Page 2</tspan></text>
  </g>
  <g
     inkscape:groupmode="layer"
     id="layer3"
     inkscape:label="layer 3">
    <text
       xml:space="preserve"
       style="font-size:36.0153px;line-height:1.25;font-family:calibri;-inkscape-font-specification:calibri;stroke-width:0.900385"
       x="56.516514"
       y="206.08427"
       id="text167-9"><tspan
         sodipodi:role="line"
         id="tspan165-8"
         style="stroke-width:0.900385"
         x="56.516514"
         y="206.08427">Page 3</tspan></text>
  </g>
</svg>
""".encode("utf-8")