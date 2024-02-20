# fhs_xmltv_tools

## Version

0.1.16

For changes see
[changelog](https://github.com/foxhunt72/fhs-xmltv-tools/blob/main/CHANGELOG.md)

## Intro

I wanted to know more about the [xmltv](http://wiki.xmltv.org) xml file
i downloaded for my iptv and i wanted to know how it all worked. So i am
starting to create my own tools

You can do the following things with your xmltv file

-   list the channels inside
-   analyse-programs, show channels with first start time and last stop
    time
-   you can cleanup your xmltv file, remove all except of the list of
    channels that you want to have
-   you can join to xmltv files to one
-   change the timezone of a time in the programs
-   search for a program in a xmltv
-   search for a program in sql
-   save program data to a sql database

I also created a program to handle m3u8 files with iptv channels, see
[iptv](https://github.com/foxhunt72/fhs-iptv-tools) or
[pipiptv](https://pypi.org/project/fhs-iptv-tools)

And automate and chain all the staps using a [yaml
command](#yaml command) task file.

But the tool is getting more advanced every day, so use it, you can find
the [source](https://github.com/foxhunt72/fhs-xmltv-tools) on github.

See pypi: <https://pypi.org/project/fhs-xmltv-tools/> or github
<https://github.com/foxhunt72/fhx-xmltv-tools>

Clean up xmltv files, with only the channels you want and even join
multiple together, also easy if you need to change timezone from one of
the files.

You can use this with every program that needs some xmltv file, like
[tvheadend](https://tvheadend.org), [kodi](https://kodi.tv),
[nextpvr](https://www.nextpvr.com) etc.

## Usage

-   fhs-xmltv-tools interactive
-   fhs-xmltv-tools [analyse-programs](#analyse-programs) \--xmltv-file
    \<xml_file\>
-   fhs-xmltv-tools [list-channels](#list-channels) \--xmltv-file
    \<xml_file
-   fhs-xmltv-tools [channel-details](#channel-details) \--xmltv-file
    \<xml_file\> \[\--channel-id \<channel_id\>\] \[\--index \<index\>\]
-   fhs-xmltv-tools [join-xml-files](#join-xml-files) \--xmltv-file
    \<xml_file\> \--xmltv-file-add \<xml_file2\> \--xmltv-out
    \<xmltv_out\>
-   fhs-xmltv-tools [search-program](#search-program) \--xmltv-file
    \<xml_file\> \--search \<regex to program name to search\>
-   fhs-xmltv-tools [write-xmlfile-channels](#write-xmlfile-channels)
    \<channel_file\> \--xmltv-file \<xml_file\> \--xmltv-out
    \<xml_out)\>
-   fhs-xmltv-tools [xmltv-to-sql](#xmltv-to-sql) \--xmltv-file
    \<xml_file\> \[\--sqltype \<sqltype\> \--sqlconnect \<sqlconnect\>
-   fhs-xmltv-tools [search-program-sql](#search-program-sql)
    \[\--sqltype \<sqltype\> \--sqlconnect \<sqlconnect\> \--search
    \<regex to program name to search\>

And the best option, i think to automate your xml needs

-   fhs-xmltv-tools [run-tasks](#run-tasks) \--yaml-command
    \<yaml_command_file\>

See the [yaml command](#yaml command) file in Examples.

Offcourse this are only the basic options use the \--help to see all the
extra options

## Installation {#example-proef}

``` bash
git clone https://github.com/foxhunt72/fhs-xmltv-tools
cd fhs-xmltv-tools
pip3 install .

pipx install fhs_xmltv_tools
pipx install fhs_xmltv_tools[all]
phpx install fhs_xmltv_tools[sqlite]
or
pip3 install fhs_xmltv_tools
pip3 install fhs_xmltv_tools[all]
pip3 install fhs_xmltv_tools[sqlite]
```

### Scripts yaml example

::: {#yaml command}
This is a simpel yaml task file. Change the url etc.
:::

And run it with

``` bash
fhs-xmltv-tools run-tasks --yaml-command <yaml_command_file>
```

Yaml task file.

``` yaml
tasks:
  - name: download tvxml file
    command: execute_command
    execute: "wget -4 https://download_url_xmltv.xml.gz -O - | gzip -d >/tmp/test.xml && mv -f /tmp/test.xml tv.epg.xml"
    shell: true
    tags: update
  - name: load xmltv file
    command: loadxml
    file: tv.epg.xml
    store: tv
  - name: analyse_programs
    title: tv_programs
    command: analyse_programs
    store: tv
  - name: clean up tv
    command: keep_channels
    store: tv
    channels:
      - RTL4.nl
      - RTL5.nl
  - name: change timezone
    command: change_timezone
    search: " +0000"
    replace: " +0200"
    store: tv
  - name: load xmltv  file
    command: loadxml
    file: tv20220924_21.xmltv
    store: xmltv
  - name: clean up xmltv
    command: only_channels
    store: xmltv
    channels:
      - AnimalPlanet.dk
      - fox9knin.us
  - name: add xmltv to tv
    command: add
    store: tv
    add_store: xmltv
  - name: save tv file
    command: savexml
    file: /tmp/new_tv.xml
    store: tv
  - name: save sql
    command: savesql
    sqlconnect: /tmp/new_tv.db
    store: tv
```

### Commands explained

#### analyse-program {#analyse-programs}

This functions will read a xmltv file and give a list of all channels
with a per channel a start and stop time.

As options you have:

-   \--xmltv-file \<xmltv_file_to_read\> or use environt varialbe
    fhs_xmltv_file
-   \--force-color force use of color in output (for example to save to
    file)
-   \--no-color use no color in output

See help output of command with \--help

``` bash
fhs-xmltv-tools analyse-programs --help | cat

Usage: fhs-xmltv-tools analyse-programs [OPTIONS]                                                                                                                                  

Analyse channels xml.                                                                                                                                                              
Args:     force_color: force color in pipeline for example     xmltv_file: xmltv file to use                                                                                       

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --xmltv-file                   TEXT  read xmltv file [env var: fhs_xmltv_file] [default: None] [required]                                                                     │
│    --force-color    --no-color          force color in pipelines [default: no-color]                                                                                             │
│    --help                               Show this message and exit.                                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Example usage

``` bash
# download a tvguide for example us
wget -4 https://iptv-org.github.io/epg/guides/us/tvguide.com.epg.xml.gz -O - | gzip -d >tvguide.com.epg.xml

fhs-xmltv-tools analyse-programs --xmltv-file tvguide.com.epg.xml

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Id                            ┃ start time           ┃ end time             ┃ programs ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ ABCEast.us                    │ 20221006000000 +0000 │ 20221008000000 +0000 │       38 │
│ AEEast.us                     │ 20221006000000 +0000 │ 20221008000000 +0000 │       54 │
│ AMCEast.us                    │ 20221006000000 +0000 │ 20221008020000 +0000 │       39 │
│ AnimalPlanetEast.us           │ 20221006000000 +0000 │ 20221008000000 +0000 │       48 │
│ BBCAmericaEast.us             │ 20221006000000 +0000 │ 20221008010000 +0000 │       35 │
│ BETEast.us                    │ 20221006000000 +0000 │ 20221008000000 +0000 │       69 │


.. _`list-channels`:
```

#### list-channels

This functions will read a xmltv file and give a list of all channels
with a per channel a index, id and channel name

As options you have:

-   \--xmltv-file \<xmltv_file_to_read\> or use environt varialbe
    fhs_xmltv_file
-   \--force-color force use of color in output (for example to save to
    file)
-   \--no-color use no color in output
-   \--ignore-empty-id don\'t display channels without a id

Example usage

``` bash
# download a tvguide for example us
wget -4 https://iptv-org.github.io/epg/guides/us/tvguide.com.epg.xml.gz -O - | gzip -d >tvguide.com.epg.xml

fhs-xmltv-tools list-channels --xmltv-file tvguide.com.epg.xml
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Index ┃ Id                            ┃ Channel                      ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│     1 │ ABCEast.us                    │ ABC East                     │
│     2 │ AEEast.us                     │ A&E East                     │
│     3 │ AMCEast.us                    │ AMC East                     │
│     4 │ AnimalPlanetEast.us           │ Animal Planet East           │
│     5 │ BBCAmericaEast.us             │ BBC America East             │
│     6 │ BETEast.us                    │ BET East                     │
│     7 │ BravoEast.us                  │ Bravo East                   │


.. _`channel-details`:
```

#### channel-details

List the channel info from a xmltv file

As options you have:

-   \--xmltv-file \<xmltv_file_to_read\> or use environt varialbe
    fhs_xmltv_file
-   \--index \<indexnr\> display the channel with index nr, see output
    of [list-channels](#list-channels)
-   \--channelid display the channel with channel id, see output of
    [list-channels](#list-channels)

Example usage

``` bash
# download a tvguide for example us
wget -4 https://iptv-org.github.io/epg/guides/us/tvguide.com.epg.xml.gz -O - | gzip -d >tvguide.com.epg.xml

fhs-xmltv-tools channel-details --xmltv-file tvguide.com.epg.xml --index 1
Channel(display_name=[DisplayName(content=['ABC East'], lang=None)],
      icon=[Icon(src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/ABC-2021-LOGO.svg/512px-ABC-2021-LOGO.svg.png',
                 width=None,
                 height=None)],
      url=['https://tvguide.com'],
      id='ABCEast.us')
```

#### join-xml-files

Join 2 xml files to one xml file.

As options you have

``` bash
fhs-xmltv-tools join-xml-files --help

Usage: fhs-xmltv-tools join-xml-files [OPTIONS]                                                           

 Join 2 xml files and write them out as 1 xml.                                                             
 Args:     xmltv_file: xmltv file to use     xmltv_file_add: xmltv file to use     xmltv_out: write xmltv  
 file     force_color: force color in pipeline for example                                                 

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --xmltv-file                      TEXT  read xmltv file [env var: fhs_xmltv_file] [default: None]    │
│                                            [required]                                                   │
│ *  --xmltv-file-add                  TEXT  read xmltv file [env var: fhs_xmltv_file] [default: None]    │
│                                            [required]                                                   │
│ *  --xmltv-out                       TEXT  write xmltv file [env var: fhs_xmltv_out] [default: None]    │
│                                            [required]                                                   │
│    --force-color       --no-color          force color in pipelines [default: no-color]                 │
│    --help                                  Show this message and exit.                                  │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

As a example

``` bash
# download a tvguide for example us
wget -4 https://iptv-org.github.io/epg/guides/us/tvguide.com.epg.xml.gz -O - | gzip -d >tvguide.com.epg.xml
wget -4 https://iptv-org.github.io/epg/guides/yt/canalplus-reunion.com.epg.xml.gz -O - | gzip -d >canalplus-reunion.com.epg.xml

fhs-xmltv-tools join-xml-files --xmltv-file tvguide.com.epg.xml --xmltv-file-add canalplus-reunion.com.epg.xml --xmltv-out out.xml
```

#### search-program

Search a program in a xmltv-file

``` bash
fhs-xmltv-tools search-program --help

Usage: fhs-xmltv-tools search-program [OPTIONS]                                                           

Search program in xml.                                                                                    
Args:     search: string or regex to search     force_color: force color in pipeline for example          
force_case: normal search is case insensitive but with this option force case sensitive     xmltv_file:   
xmltv file to use                                                                                         
```

╭─ Options
───────────────────────────────────────────────────────────────────────────────────────────────╮
│ \* \--search TEXT regex search \[default: None\] \[required\] │ │ \*
\--xmltv-file TEXT read xmltv file \[env var: fhs_xmltv_file\] │ │
\[default: None\] \[required\] │ │ \--force-color \--no-color force
color in pipelines \[default: no-color\] │ │ \--force-case-sensitive │ │
\--help Show this message and exit. │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯

#### write-xmlfile-channels

Cleanup xmltv file by only writing the channels to a new files that you
listed in a file.

``` bash
fhs-xmltv-tools write-xmlfile-channels --help                                                                                                           
Usage: fhs-xmltv-tools write-xmlfile-channels [OPTIONS] CHANNEL_FILE                                      

Write xmlfile with only used channels to xml.                                                             
Args:     channel_file: file with channels one per line     xmltv_file: xmltv file to use     xmltv_out:  
write xmltv file     force_color: force color in pipeline for example                                     

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    channel_file      TEXT  [default: None] [required]                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --xmltv-file                   TEXT  read xmltv file [env var: fhs_xmltv_file] [default: None]       │
│                                         [required]                                                      │
│ *  --xmltv-out                    TEXT  write xmltv file [env var: fhs_xmltv_out] [default: None]       │
│                                         [required]                                                      │
│    --force-color    --no-color          force color in pipelines [default: no-color]                    │
│    --help                               Show this message and exit.                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

channel_file is a text one with one channel id on every line

#### run-tasks

Running all the automation you want for xmltv files, task for task using
a

Usage:

``` bash
fhs-xmltv-tools run-tasks --help

Usage: fhs-xmltv-tools run-tasks [OPTIONS]                                                                                   

Run tasks in yaml file.                                                                                                      
Args:     yaml_command: xmltv file to use     force_color: force color in pipeline for example     include_tag: tags from    
task to include     exclude_tag: exclude tasks with this tag                                                                 

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --yaml-command                  TEXT  read yaml file [env var: fhs_xmltv_yaml] [default: None] [required]               │
│    --force-color     --no-color          force color in pipelines [default: no-color]                                      │
│    --include-tag                   TEXT  [default: None]                                                                   │
│    --exclude-tag                   TEXT  [default: None]                                                                   │
│    --help                                Show this message and exit.                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### save-xmlfile-to-sql {#xmltv-to-sql}

Write the program data to a sql locaton (like sqlite), that way you can
search in programs for longer times, the search options will come soon.

``` bash
fhs-xmltv-tools xmltv-to-sql --help                                                                                                           
Usage: fhs-xmltv-tools xmltv-to-sql [OPTIONS]

Xmltv to sql (using sqlalchemy).
Args:     force_color: force color in pipeline for example     xmltv_file: xmltv file to use
sqltype: sqltype type sqlite or sqlalchemy     sqlconnect: connect string, this is the filepath is
using sqltype = sqlite

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --xmltv-file                   TEXT  read xmltv file [env var: fhs_xmltv_file] [default: None]     │
│                                         [required]                                                    │
│    --sqltype                      TEXT  sqltype for now, (default) sqlite or sqlalchemy               │
│                                         [default: sqlite]                                             │
│ *  --sqlconnect                   TEXT  sqlconnect how to connect. [default: None] [required]         │
│    --force-color    --no-color          force color in pipelines [default: no-color]                  │
│    --help                               Show this message and exit.                                   │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

sqlconnect is the file name if using sqlite

#### search-program-sql

Search a program in a sql datebase.

You can find a example
[yaml](https://github.com/foxhunt72/fhs-xmltv-tools/raw/main/Examples/tasks_example.yml)
file in the source and also some extra documentation in the
[examples](https://github.com/foxhunt72/fhs-xmltv-tools/tree/main/Examples)
directory.

##### Requirements

-   typer\[all\]
-   py-xmltv
-   pyyaml

## Compatibility

## Licence

MIT Licencse

## Authors

Richard de Vos

[fhs_xmltv_tools]{.title-ref} was written by [Richard de
Vos](rdevos72@gmail.com).
