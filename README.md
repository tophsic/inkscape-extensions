inkscape-extensions
===================

My Inkscape extensions


Commands to automate some things on producing tags for my resume :

sed 's/>[^<]*<\/tspan/>Lorem ipsum<\/tspan/' tag.svg
inkscape tag.svg --verb=net.plom.christophe.inkscape.tag --verb=net.plom.christophe.inkscape.document --verb=FileSave --verb=FileClose
