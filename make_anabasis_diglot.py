import re
import lxml.etree as ET
from greek_normalisation.utils import nfc
from collections import defaultdict


EN = defaultdict(list)
GR = defaultdict(list)

BASE = 'anabasis_1.xml'
DATA_DIR = ".\\source_data\\"
EN_SRC = DATA_DIR + 'en_' + BASE
GR_SRC = DATA_DIR + 'gr_' + BASE


def clean_english(xml):
    ET.strip_elements(xml, 'note', with_tail=False)
    ET.strip_tags(xml, 'placeName')
    ET.strip_tags(xml, 'persName')
    ET.strip_tags(xml, 'del')
    ET.strip_tags(xml, 'add')

    for x in xml.findall('//milestone[@unit="para"]'):
        prev = x.getprevious()
        parent = x.getparent()
        prev.tail = (prev.tail or '') + ' ' + (x.tail or '')
        parent.remove(x)
    return xml
          


def process_file(xml):
    chapter = '0'
    output = {}
    p = xml.find('//p')
    for node in p.getchildren():
        unit = node.get('unit')
        if unit == 'chapter':
            chapter = node.get('n')
            if node.tail:
                output[f"{chapter}.0"] = node.tail.strip()
        if unit == 'section':
            output[f"{chapter}.{node.get('n')}"]  = node.tail.strip()
    return output


ENFILE = clean_english(ET.parse(EN_SRC))
GRFILE = clean_english(ET.parse(GR_SRC))

en_data = process_file(ENFILE)
gr_data = process_file(GRFILE)


HEADER = """<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>Diglot</title>
		<meta name="viewport" content="width=device-width,initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/alpheios-components@latest/dist/style/style-components.min.css"/>
        <link rel="stylesheet" href="typebase.css" type="text/css" />
        <link rel="stylesheet" href="normalize.css" type="text/css" />
        <link rel="stylesheet" href="fonts.css" type="text/css" />
    </head>
    <body>
    <div >
    """

FOOTER ="""</div>
</body>
<style>
    .wrapper {
        display: flex;
        margin: 4px;

    }

    .gr {
        flex:1;
        margin-right:2px;
    }
    .en { flex: 0;}
    .en-data { display: none; }
    .marker {margin-right: 0.5em;}
    .number {margin-right: 0.25em;}
</style>
<script>
    function toggleEn(e) {
        console.log('clicked');
        let par = e.target.parentElement;
        let x = par.querySelector('.en-data');
        if (x.style.display === "none") {
            x.style.display = "inline";
            par.style.flex = 1;
        } else {
            x.style.display = "none";
            par.style.flex = 0;
        }
    }

    function toggleMe(e) {
        console.log('clicked');
        let par = e.target;
        let x = par.querySelector('.en-data');
        if (x.style.display === "none") {
            x.style.display = "inline";
            par.style.flex = 1;
        } else {
            x.style.display = "none";
            par.style.flex = 0;
        }
    }

    const elems = document.getElementsByClassName('marker');

    for (var i=0; i < elems.length; i ++) {
        elems[i].addEventListener('click', toggleEn);
    }

    const elemsB = document.getElementsByClassName('en-data');
    for (var i=0; i < elemsB.length; i ++) {
        elemsB[i].addEventListener('click', toggleEn);
    }

</script>
<script type="text/javascript">
        document.addEventListener("DOMContentLoaded", function(event) {
        import ("https://cdn.jsdelivr.net/npm/alpheios-embedded@latest/dist/alpheios-embedded.min.js").then(embedLib => {
            window.AlpheiosEmbed.importDependencies({ 
            mode: 'cdn'
            }).then(Embedded => {
            new Embedded({clientId: "thrax-grammar-fhard"}).activate();
            }).catch(e => {
            console.error(`Import of Alpheios embedded library dependencies failed: ${e}`)
            })

        }).catch(e => {
            console.error(`Import of Alpheios Embedded library failed: ${e}`)
        })
        });
    </script>
</body></html>"""

with open('.\\docs\\index.html', 'w', encoding="UTF-8") as f:
    print(HEADER, file=f)
    print("<h1>Anabasis, Book 1</h1>", file=f)
    for key, text in gr_data.items():
        en = en_data[key]
        print('<div class="wrapper">', file=f)
        print(f'    <div class="number">{key}</div>', file=f)
        print(f'    <div class="gr alpheios-enabled"  lang="grc">{text}</div>', file=f)
        print(f'    <div class="en" lang="en"><span class="marker">&#8853;</span><span class="en-data">{en}</span></div>', file=f)
        # <div class="wrapper"><div class="gr">Greek</div><div class="en"><span class="marker">&#8853;</span><span class="en-data">EN</span></div></div>
        print('</div>', file=f)
    print(FOOTER, file=f)




    



