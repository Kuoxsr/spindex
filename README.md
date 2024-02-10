# Sound Pack Indexer
This is a tool designed to auto-generate a `sounds.json` for a Minecraft resource pack given a folder structure containing a specific set of file types.

The project wasn't intended for public consumption.  Lots of things are non-optimal at the moment.  Please consider this a work in progress.  Why, then, am I writing this document as if explaining it to someone who has never seen it before?  Because I have a #$%^ memory, and I will likely forget all of this in a matter of weeks.  You benefit from my early senility.

## Why build this?
Since my plans for the future involve hundreds (perhaps _thousands_) of sound files (and their corresponding records in JSON), I needed some way of making the job faster.  Automating the creation of JSON is one way to do that, since it saves me from having to switch to a text editor over and over again while I edit sound files.

## How to set up a sound pack staging area
I do not recommend running this script on a production folder containing previously created JSON and `.ogg` files, because the existing JSON might contain changes you made manually that are not covered by this script (and various other issues), however, the file that is created uses the prefix `generated-` to avoid collisions, just in case.

What I _do_ recommend is setting up a special staging area for the edited files.

### Folder structure
A properly formatted staging area will consist of a namespace folder, which is analogous to a folder that would live in the `assets` folder in your pack, a sounds folder and a series of folders that exactly match the applicable Minecraft sound event name.  Here's an example:

```
mynamespace (can be "minecraft" if you don't want to use a custom namespace)
    sounds
        entity
            villager
                ambient
                    test-sound.ogg
```

In the above example, the script would generate a record for the entity.villager.ambient sound event, with `test-sound.ogg` as its only sound.  The JSON might look like this:

```json
{
    "entity.villager.ambient": {
        "sounds": [
            {"name": "mynamespace:entity/villager/ambient/test-sound"}
        ]
    }
}
```

Notice that the sound event name is built from the folder structure under `sounds` and has dot separators, while the `.ogg` file has slashes.  The latter is a path (sort of), while the former is a proprietary string recognized only by Minecraft.  Also notice that the `sounds` folder is nowhere to be found in the `.ogg` file path.  The game adds this automatically when reading the JSON, so it shouldn't be specified.  I said "sort of" a path, because the namespace folder is prepended to the path and separated from it using a colon.  Essentially, the colon is a placeholder for where `/sounds/` would normally go.  Finally, notice that the `.ogg` has been removed from the file name.  Mojang requires this audio format, and therefore doesn't specify it in the JSON

In the above sample JSON, the `{}` represents a [dictionary](https://www.geeksforgeeks.org/python-dictionary/), while the `[]` represents a [list](https://www.geeksforgeeks.org/python-lists/).

The script is smart enough to use the following folder structure as well:

```
some-namespace (can be "minecraft" if you don't want to use a custom namespace)
    sounds
        extra-folder(s)
            entity
                villager
                    ambient
                        test-sound.ogg
```

I needed this because I wanted to keep sounds from different team members separate:
```
team/sounds/{team member name}/entity/villager/ambient/test-sound.ogg
```

It should handle any number of subfolders between `sounds` and the start of the sound event name, but I haven't tried more than one, so if it breaks, submit a [bug report](https://github.com/Kuoxsr/sound-pack-indexer/issues).

I suppose I should mention that sound files themselves can be named anything you like, so long as they contain _only_ the following characters:

1. a-z (lowercase only)
2. 0-9
3. forward slash (/)
4. dot
5. underscore
6. dash

Here is the regular expression this application uses to check file names:

```
^[a-z0-9/._-]+$
```


### defaults.json
In order to speed up the process of setting custom properties on the files in your staging area, you should probably set up a defaults.json file.  It lives in the namespace folder and has the following structure.  I've cut it down a bit for brevity:

```json
{
  "all": {
    "replace": true
  },
  "entity.enderman.scream": {
    "subtitle": "subtitles.entity.enderman.ambient"
  },
  "entity.ghast.warn": {
    "subtitle": "subtitles.entity.ghast.shoot"
  },
  "entity.player.big_fall": {
    "subtitle": "subtitles.entity.generic.big_fall"
  },
  "entity.player.small_fall": {
    "subtitle": "subtitles.entity.generic.small_fall"
  },
  "entity.villager.ambient": {
    "volume": 0.3
  },
  "entity.villager.celebrate": {
    "volume": 0.5
  },
  "entity.witch.ambient": {
    "replace": false,
    "volume": 0.7,
    "weight": 3,
    "pitch": 2.4,
    "stream": false,
    "attenuation_distance": 8,
    "preload": true,
    "type": "sound"
  }
}
```

Things to notice about the above:

- Default values can be defined per sound event, and can contain any of the values listed in the Minecraft Wiki under "sounds.json"
- There is a fallback called "all" that applies to every sound event, unless specified via a specific event name.
- Some of the events specify a subtitle that is different from the event name.  Yep, that's right.  It's the whole reason I designed this method of defaulting.  I couldn't just automatically generate them from the file structure.  Thanks, Mojang!

You can't specify these values per sound, but you can set aside a specific event as having a default volume, pitch, weight, etc.  For example, in the document above, the entity.villager.ambient event will always default to volume 0.3, while pretty much every other villager sound defaults to volume of 0.5.  I found that the ambient sounds were too loud and got on people's nerves after a longer period of time.  Meanwhile, sounds like the trade sounds should be louder, so they can cut through the noise.

The point of the file is customizability, however, so find the default values that work best for you.  Start with the defaults.json in the root of this project, copy it to your staging area, and modify it to your heart's content.  There is plenty of bounds-checking in the app to make sure that the values are correct before it uses them.

If you want a good laugh, take a look at the commit history of this file for what used to be in this spot.

### "replace": true
Much of the time, you will want to have `"replace": true` set for a particular sound event, like so:

```json
{
    "entity.villager.trade": {
        "replace": true,
        "sounds": [
            {"name": "namespace:/entity/villager/trade/ogg-file"}
        ],
        "subtitle": "subtitles.entity.villager.trade"
    }
}
```

What this does is tell Minecraft to stomp on any previous sounds in that event, douse them in gasoline and light them on fire.  With `"replace": true` in your JSON, only your files will be available for the game to choose from when triggering that event. :smiling_imp:

Since this is a harsh and overbearing way to construct a pack, there may be times when you don't want to include that line.

That's where you might want to set a particular event to have "replace": false

## How to run this script
To run the script, you need a [python 3.11 environment](https://www.python.org/downloads/release/python-3110/).  Explaining [how to install](https://duckduckgo.com/?q=how+to+install+python+3.11) that is beyond the scope of this document.

Pass the path to your namespace folder into the script via command-line parameter, like so:

```bash
[you@localhost:~/dev/folder]$ ./sound-pack-indexer -s /path/to/namespace/folder
```

When finished, the script will show the contents it created in the terminal window, and a file called `generated-sounds.json` will be created in your namespace folder.

## Merging the generated file into an existing sound pack
Once `generated-sounds.json` is created, its contents will be shown in the terminal window. If you specified a target folder in the command, like this:

```bash
./sound-pack-indexer -s /path/to/staging-namespace -t /path/to/sound/pack
```

... or, if you put the script in your path, gave it an alias, and executed it from within the source folder, like this:

```bash
[you@localhost:/path/to/staging-namespace]$ packindex -t /path/to/sound/pack
```

...you'll be asked whether you want to copy the files to the target folder.

Answering "y" to this question does two things:

1. All the `.ogg` files in your staging area's folder structure will be copied to the target location's folder structure
    1. The app notifies you of any name collisions and allows you to abort
    2. If you choose not to abort, files in the target folder will be overwritten
2. The JSON data in `generated-sounds.json` will be merged into the `sounds.json` file in your existing sound pack.
    1. Sound event names and sound file names will be sorted alphabetically in their respective contexts.

### Command-line switches
If you run the app with "-h" you'll see an explanation of all the optional switches that are possible:

```
usage: Sound Pack Indexer [-h] [-v] [-i] [-q] [-a] [-s SOURCE] [-t TARGET]

Generates a json index from folders full of .ogg files.
Optionally allows automatic merging of this generated file with an existing pack.

options:
-h, --help            show this help message and exit
-v, --version         show program's version number and exit
-i, --index-only      Only produce the generated-sounds.json file and then exit.
-q, --quiet           Suppress printing of json file contents. Only show warnings.

-a, --abort-warnings  Treat all warnings as fatal errors, and exit as soon as they occur.

-s SOURCE, --source SOURCE
Path to the source folder. Ogg files to be indexed are found here.

-t TARGET, --target TARGET
Path to the target folder. Ogg files will be copied here, if allowed.
```

Those are probably self-explanatory, right?

## This script only works in Linux
I have not tested whether this script runs in a Windows environment, only Linux.  Your mileage may vary.  If you try it in Windows and it doesn't work, fix the problem and submit a pull request.  An issue in the bug tracker for that particular problem will likely go nowhere, because I do not own a copy of Windows in which to test.  If it _does_ work in Windows, let me know so that I can remove this paragraph.

## Final Thoughts
This script should be run only once on a particular data set to generate a JSON file, and then that JSON should be incorporated into your resource pack, either by copying in the entire JSON file (in the case of a new, clean project) or individual lists of sound files should be copy/pasted from the generated file to an existing `sounds.json` file.  Create backups of your resource pack before you do any of this, or use a [git](https://git-scm.com/) repository like a civilized person.

Why did I use the term "indexer?"  I came up with that in my initial planning, and either couldn't think of anything better or just didn't want to bother wasting brain power on a name, so now I'm stuck with it.

Thanks for your interest in my project!