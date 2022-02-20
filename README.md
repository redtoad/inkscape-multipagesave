# inkscape-multipagesave

This extension to Inkscape will export SVG layers independently to PDFs

## Install

To install this extension, download and unpack the archive file. Copy the files into the directory listed at Edit > Preferences > System: User extensions (on my machine, for instance, it is `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions`). After a restart of Inkscape, the new extension will be available.

## Development

There is some [official documentation](1) available but I found the best source to the official Python extensions. The one most closely related is the [Guillotine extension](2). Take a look!

Once you done you changes, be sure to run the tests:

    pipenv install --dev
    pipenv run pytest -v

## License

This code is released under GPL3. 

[1]: https://inkscape.org/develop/extensions/
[2]: https://gitlab.com/inkscape/extensions/-/blob/master/guillotine.py