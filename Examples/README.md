Example task file, to download, cleanup, merge and save a new xmltv file.


```
pipx install fhs_xmltv_tools

fhs-xmltv-tools run-tasks --yaml-command tasks_example.yml

or for more options

fhs-xmltv-tools --help
```

# Intro

The yaml command file exists of a array of tasks, each entry of the array is one step
to create your perfect xml file.

For exempla a tasks file with one entry to load a xmltv file with the name tv.epg.xml
```
---
tasks:
  - name: load xmltv file
    command: loadxml
    file: tv.epg.xml
    store: tv
```

Every task entry has a name and a command.
The name your description of that step.
The command is the command that you want to run, the following options are posible for command.

- loadxml
  - load a xml file into memory, use the store options to choice the memory name.
- execute_command
  - Execute a shell command, use shell: true if you want to chain multiple commands with a pipe command.
- analyse_programs
  - Analyse a loaded xmltv file, use store to choice which memory place to use.
- keep_channels
  - Keep only the named channels
- change_timezone
  - Change the timezone in the program data, this is more a search and replace on the start and stop time.
- add
  - add a xml store to another store
- savexml
  - save a xml store back to disk.
- savesql
  - save a xml store data to sql (for now sqlite only)


# More examples

## loadxml

```
 - name: load xmltv file
   command: loadxml
   file: tv.epg.xml
   store: tv
```

- name: just your description
- command: loadxml
- file: filename to load
- store: memory name to store xmltv in, so you can use it with the other commands.

## execute_command

```
 - name: download tvxml file
   command: execute_command
   execute: "wget -4 https://iptv-org.github.io/epg/guides/us/tvguide.com.epg.xml.gz -O - | gzip -d >tvguide.com.epg.xml"
   shell: true
   tags: update
```

```
 - name: download tvxml file
   command: execute_command
   execute:
     - "wget"
     - "https://download_url"
     - "-O"
     - "proef.xml"
   shell: false
   tags: update
```

- name: just your description
- command: execute_command
- execute: <string to execute> if shell: true
- shell: true  (use shell to execute)
- tags: tags_to_only_execute_parts_of_tasks_file, can be used by every command type

## analyse_program

```
 - name: analyse_programs
   title: tv_programs
   command: analyse_programs
   store: tv
```

- name: again your description
- command: analyse_programs
- title: <title for output, just makes it nicer if you have multiple xmltv to output>
- store: memory store to use (offcourse first load a xmltv with the loadxml command)

## keep_channels

Delete every channels that isn't mentioned
Alias for only_channels 

```
 - name: clean up tv
   command: only_channels
   store: tv
   channels:
    - RTL4.nl
    - RTL5.nl
```

- name: description
- command: only_channels
- store: store to update
- channels: list of channels id to keep, the rest is removed

## change_timezone

```
 - name: change timezone
   command: change_timezone
   search: " +0000"
   replace: " +0200"
   store: tv
```

- name: description
- command: change_timezone
- search: text to search in start/stop time " +0000"
- replace: text to replace search with " +0200"


## add

```
 - name: add xmltv to tv
   command: add
   store: tv
   add_store: xmltv
```

- name: description
- command: add
- store: store to add channels and programs from second store
- add_store: store that you are adding

Offcourse you need to load both stores with the loadxml command in to memory and maybe clean them up with only_channels before joining.

See the example task file in this directory.

## savexml

```
 - name: save tv file
   command: savexml
   file: /tmp/new_tv.xml
   store: tv
```

- name: description
- command: savexml
- file: file to save xml to
- store: memory store to save to disk


## savesql

```
 - name: save xmltv data to sql
   command: savesql
   sqlconnect: /data/sqlite.db
   sqltype: sqlite
   store: tv
```

- name: description
- command: savesql
- store: memory store to save to sql
- sqltype: type of sqldata base for now 'sqlite' or 'sqlalchemy'
- sqlconnect: connect string for sql,
    - if sqltype is 'sqlite' then this is a file path
    - if sqltype is 'sqlalchemy' then this is a sqlalchemy engine url
      please make sure that the right python packages for your database are installed 


## clean_sql

```
 - name: clean program data from sql
   command: clean_sql
   sqlconnect: /data/sqlite.db
   sqltype: sqlite
   days: 180
```

- name: description
- command: clean_sql
- sqltype: type of sqldata base for now 'sqlite' or 'sqlalchemy'
- sqlconnect: connect string for sql,
    - if sqltype is 'sqlite' then this is a file path
    - if sqltype is 'sqlalchemy' then this is a sqlalchemy engine url
      please make sure that the right python packages for your database are installed 
- days: days to keep of program data, (default 90 days)

