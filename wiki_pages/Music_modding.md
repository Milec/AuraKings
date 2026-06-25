# Music modding

It is possible to mod custom music into the game, as well as script when and where said tracks will play.

It is also possible to add music to the game without having to edit the games .bank (a kind of specialised file format for storing sounds) files.


- [Showing them in the Music Player](#showing-them-in-the-music-player)
- [Where to put the Music](#where-to-put-the-music)


## Showing them in the Music Player

To add the Music tracks we wish to put into the Music Player into categories. To do this they must be implemented with the following files structure:

```
game
└ music
  ├ music_categories
  │ └ music_categories.txt
  └ music.txt
```


The **music.txt** files contain information on the tracks themselves, and in order to have them localized they all must have a *name = loc_key* field. 
Example:

```
mx_raid = {
    music = "event:/DLC/FP1/MUSIC/cuetracks/mx_raid"
     name = fp1_soundtrack_01_the_raid
    pause_factor = 35
}
```


The **music_category.txt** files contains information on the categories and tracks contained within them:

```
category = {
     id = "mx_category_10"
     name = "fp2_cue_soundtrack"
     tracks = {
         "mx_IberiaWar"
         "mx_Struggle_ending_compromise"
         "mx_Struggle_ending_conciliation"
         "mx_Struggle_ending_hostility"
         "mx_Struggle_Opening"
     }
 }
```


It is important to note that the **id** field in these categories ***must*** be unique.

Finally to get the art in, they'll be put into following structure, if using the above category as an example:

```
game
└ gfx
  └ interface
    └ illustrations
      └ music_player
        └ fp2_cue_soundtrack.dds
```


## Where to put the Music

Put the .ogg or .wav file in a directory and link to that from the **music.txt** file. (root is your mod folder). 

For example:
```
mx_raid = {
    music = "file:/music/my_new_song.ogg"
    name = some_name_for_loc_key
    pause_factor = 2
}
```


Category:Modding

---

*Source: https://ck3.paradoxwikis.com/Music_modding*
