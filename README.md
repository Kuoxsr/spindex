# Sound Pack Indexer
This is a tool designed to auto-generate a `sounds.json` for a Minecraft resource pack given a folder structure containing a specific set of file types.

The project wasn't intended for public consumption.  Lots of things are non-optimal at the moment.  Please consider this a work in progress.  Why, then, am I writing this document as if explaining it to someone who has never seen it before?  Because I have a #$%^ memory, and I will likely forget all of this in a matter of weeks.  You benefit from my early senility.

## Why build this?
Since my plans for the future involve hundreds (perhaps _thousands_) of sound files (and their corresponding records in JSON), I needed some way of making the job faster.  Automating the creation of JSON is one way to do that, since it saves me from having to switch to a text editor over and over again while I edit sound files.

## How to set up a sound pack staging area
I do not recommend running this script on a production folder containing previously created JSON and `.ogg` files, because the existing JSON might contain changes you made manually that are not covered by this script (and various other issues), however, the file that is created uses the prefix `generated_` to avoid collisions, just in case.

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

```
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

Here is a regular expression to check file names:

```
^[a-z0-9/._-]+$
```

Ironically, I did not include any file name compliance checking in this script as of this writing.  The pack checker script has it, but this one does not... yet.

### Subtitles files
If your JSON doesn't include a "subtitle" specification for a sound event you will not see text like "villager mumbles" on the right-hand side of the screen when the noise occurs (provided you have "show subtitles" on.)  To cover that, the script auto-generates this for you with exactly the same name as the sound event by default.  I say "by default," because in several places throughout the vanilla `sounds.json` file, the subtitle _does not match_ the sound event name (Thanks, Mojang!)

There were too many of these to put into the script as exceptions (and that felt like a hack anyway,) so I decided that I would let the file structure handle that too.

To create a subtitle that does not match the sound event name, you put a file into the folder with the `.ogg` files, which is named using the following format:

```
.{name of subtitle string}.subtitles
```

Note the initial dot.  This is to make the file invisible under normal file browsing (at least under Linux), and to make it easy to exclude these files from the copy commands I haven't written yet.  The extension of `.subtitles` ensures that the script knows what it's for.  In the output, the word "subtitles" is moved to the start of the name.  Here's a real-world example:

A file in this folder:
```
assets/{namespace}/sounds/entity/ghast/warn/
```

... with this name:
```
.entity.ghast.shoot.subtitles
```

... results in this JSON:
```
{
    "entity.ghast.warn": {
        "subtitle": "subtitles.entity.ghast.shoot"
    }
}
```

Again, thanks Mojang for making these names different for no apparent reason :rage:

When the staging area folder structure is copied (without `.ogg` files) for the next team member, the subtitles for each sound event that needs them will be copied as well (using a command I haven't written yet.)  This means, once you tag an event folder with the proper subtitle string, you should never have to do it again.

### Ogg file metadata
I didn't want to stop there, however, because you can alter the volume, pitch, selection weight and a bunch of other things for each file by specifying these in the JSON.  I tend to make villager sounds `0.5` in volume, because fully normalized files sound _really loud_ when spoken by a villager.  Other sounds, particularly monster noises, I would like to keep at full volume if possible, or at any level I find appropriate.  But how would I do this without causing more work than it would take to just edit the JSON manually?  I used `.ogg` file metadata.

I edit clips in an audio editor called [Tenacity](https://codeberg.org/tenacityteam/tenacity), which is a fork of [Audacity](https://github.com/audacity/audacity).  Both are open source and do the job well.  When I export a finished edit, it asks me for metadata - things like Artist, track number, album title, etc.  I decided to use "album title" for my custom JSON string, since I'm already using other tags for their intended purposes.  Now when I export a file to `.ogg`, I can set a tentative volume level right in Tenacity without ever reaching for my text editor, and this script can detect that and add it to the final `generated_sounds.json`.

I also figured that since I was in the process, I might as well make it easy to add any of the other potential directives as well, and that turned out to be much easier to do than I expected.

Here's the text to enter into Album Title to just set the volume:
```
{"volume": 0.5}
```

If you want to include other properties, it would look something like this:
```
{"volume": 0.5, "pitch": 5.3, "stream": true, "weight": 5}
```

There's a good document explaining what all these directives do [here](https://minecraft.fandom.com/wiki/Sounds.json).

When the script encounters a sound clip with an album title, it assumes that this string will be in the above format, which means here is where I admit that I haven't written any error handling for what happens when you use a clip that has a string like "Fear of a Blank Planet" instead of JSON.  "Work in progress," remember?

### "replace": true
Much of the time, you will want to have `"replace": true` set for a particular sound event, like so:

```
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

Well, tough darts, farmer... because I haven't coded a way to do that automatically yet!  As of this writing, it _always_ generates `"replace": true` and you're just going to have to live with it! :boom:

Seriously, though... I haven't decided how to handle this.  Do I want a command-line switch to change the default to `"replace": false` or do I want a solution like the above with dotfiles like `.false.replace`?  If you can think of the best way to handle this, I'm all ears.

## How to run this script
To run the script, you need a [python 3.11 environment](https://www.python.org/downloads/release/python-3110/).  Explaining [how to install](https://duckduckgo.com/?q=how+to+install+python+3.11) that is beyond the scope of this document.  Also out of scope is an explanation of how to set up the external modules it requires.  The script imports several modules that are not in the standard set, such as `TinyTag` and `CompactJSONEncoder`, so it won't be easy to set this up for anyone who doesn't understand Python.  I may update this document to include instructions if I get enough requests (and I figure out how to do it myself without [PyCharm](https://www.jetbrains.com/pycharm/).)  One of the problems is that `TinyTag` is installed into a virtual environment for this project, and PyCharm tells git to ignore this by default.  It needs to be manually installed.

If this giant set of instructions hasn't deterred you, and the previous paragraph doesn't scare you away, pass the path to your namespace folder into the script via command-line parameter, like so:

```
[you@localhost:~/dev/folder]$ ./sound-pack-indexer /path/to/namespace/folder
```

When finished, the script will show the contents it created in the terminal window, and a file called `generated-sounds.json` will be created in your namespace folder.

I have not tested whether this script runs in a Windows environment, only Linux.  Your mileage may vary.  If you try it in Windows and it doesn't work, fix the problem and submit a pull request.  An issue in the bug tracker for that particular problem will likely go nowhere, because I do not own a copy of Windows in which to test.  If it _does_ work in Windows, let me know so that I can remove this paragraph.

## Final Thoughts
This script should be run only once on a particular data set to generate a JSON file, and then that JSON should be incorporated into your resource pack, either by copying in the entire JSON file (in the case of a new, clean project) or individual lists of sound files should be copy/pasted from the generated file to an existing `sounds.json` file.  Create backups of your resource pack before you do any of this, or use a [git](https://git-scm.com/) repository like a civilized person.

Why did I use the term "indexer?"  I came up with that in my initial planning, and either couldn't think of anything better or just didn't want to bother wasting brain power on a name, so now I'm stuck with it.

## Future plans
My notes currently contain the idea to create code that automatically copies `.ogg` files into an existing resource pack and automatically incorporate JSON records into an existing `sounds.json` file.  I have been procrastinating on that, because it seems difficult to do, and because I'm already procrastinating on editing sound clips by writing this script (and this document.)  If you know Python and would like to help out, feel free to code a solution for this and submit a pull request.  I can't explain how to submit a pull request, because I've never actually done it myself, so you're on your own.  Have fun!

Thanks for your interest in my project!