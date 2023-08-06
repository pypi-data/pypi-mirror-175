# fead

This is a tool for advertising other blogs you like on your own
by embedding the summary of their latest post(s) extracted from their web feed.
It is a rewrite of [openring] with ([rejected]) concurrency support
in Python without any third-party library.

## Usage

```console
$ fead --help
Usage: fead [OPTION]...

Generate adverts from web feeds.

Options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -F PATH, --feeds PATH
                        file containing newline-separated web feed URLs
  -f URL, --feed URL    addtional web feed URL (multiple use)
  -n N, --count N       maximum number of ads in total (default to 3)
  -p N, --per-feed N    maximum number of ads per feed (default to 1)
  -l N, --length N      maximum summary length (default to 256)
  -t PATH, --template PATH
                        template file (default to stdin)
  -o PATH, --output PATH
                        output file (default to stdout)

Any use of -f before -F is ignored.
```

## Template format

The template is used by Python [`str.format`][format] to generate each advert.
It can contain the following fields, delimited by braces ('{' and '}').

* `source_title`: title of the web feed
* `source_link`: URL to the feed's website
* `title`: title of the feed item
* `link`: URL to the item
* `time`: publication time
* `summary`: truncated content or description

The publication time is a Python [`datetime.datetime`][datetime] object,
which supports at least C89 format codes, e.g. `{time:%Y-%m-%d}`.

## Contributing

Patches should be sent to [~cnx/misc@lists.sr.ht]
using [git send-email] with the following configurations:

    git config sendemail.to '~cnx/misc@lists.sr.ht'
    git config format.subjectPrefix 'PATCH fead'

## Copying

![AGPLv3](https://www.gnu.org/graphics/agplv3-155x51.png)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either [version 3 of the License][agplv3],
or (at your option) any later version.

[openring]: https://sr.ht/~sircmpwn/openring
[rejected]: https://lists.sr.ht/~sircmpwn/public-inbox/patches/27621
[format]: https://docs.python.org/3/library/string.html#formatstrings
[datetime]: https://docs.python.org/3/library/datetime.html#datetime-objects
[~cnx/misc@lists.sr.ht]: https://lists.sr.ht/~cnx/misc
[git send-email]: https://git-send-email.io
[agplv3]: https://www.gnu.org/licenses/agpl-3.0.html
