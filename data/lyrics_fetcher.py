import lyricsgenius

genius = lyricsgenius.Genius("HSdEZC5GCcxjUQu3mcNxNTfBDn5xtcxOYLfmQOC1efnkdcqNyWMODFTo9zC3K93C")

rappers = ["Drake", "Lil Wayne", "Migos", "Kendrick Lamar", "Jay Z", "Tupac", "Snoop Dogg", "Meek Mill", "Pusha T", "21 Savage"]

output = {}

for rapper in rappers:

    artist = genius.search_artist(rapper, max_songs=200, sort="title")

    for i, song in enumerate(artist.songs[1:]):

        filename = "{}_{}.txt".format(rapper.lower(), i)

        with open(filename, "w", encoding='utf-8') as lyrics_file:

            for line in song.lyrics.splitlines():

                # Removing empty lines, and ones that indicate [Chorus 1], [Verse 2], etc.
                if not line.startswith("[") and len(line.strip()) != 0:

                    lyrics_file.write(line + '\n')



