# e621-dl

**e621-dl** is a simple and fast e621 post/pool downloader. It is based upon the [e621](https://github.com/Hmiku8338/e621-py-stable) api wrapper both in implementation and interface.

## Installation

`pip install e621-dl`

## Quickstart

### Downloading Posts

* To download posts with the ids 12345 and 67891:
`e6 posts get 12345 67891`
* To download all posts that match the canine but not the 3d tag:
`e6 posts search "canine -3d"`
* To download 500 posts that match the 3d tag:
`e6 posts search 3d -m 500`
* To download posts that match the 3d tag to directory e621_downloads:
`e6 posts search 3d -d e621_downloads`
* To download all posts that match the 3d tag and replace all post duplicates from the parent directory with symlinks:
`e6 posts search 3d -s`

### Downloading Pools

* To download the pools with the ids 12345 and 67891:
`e6 pools get 12345 67891`
* To download at most 10 pools whose names start with "Hello" and end with "Kitty" with anything else in the middle.
`e6 pools search --name-matches Hello*Kitty -m 10`
* To download the top 3 active series ordered by post count to a directory named "my_top_3":
`e6 pools search --is-active --order post_count -m 3 -d my_top_3`
* There are a lot more options so I recommend checking out the output of `e6 pools search --help`

### Using Api Key

* To save e621 login information to be used for every future query:
`e6 login`
* To remove e621 login information:
`e6 logout`

### Optimizing Space

* To replace all post duplicates from the current directory (all of its subdirectories) with symlinks:
`e6 clean`

## FAQ and Known Issues

* If your tags include the minus (-) sign, a colon (:), or any other character bash/typer might consider special -- you must wrap your query in quotation marks. For example,
`e6 posts search "3d -canine order:score"`
* For advanced reference, use `--help` option. For example, `e6 --help`, `e6 posts search --help`, etc.
