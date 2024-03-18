
+-------------------------+
|      Hit Song Data      |
+-------------------------+

Data from all hit songs who made into Weekly Top 200 Spotify Charts in all considered markets (2017-19). Data collected from Spotify in 2020. For more information on the features, see Spotify Developer API.

+-----------------------------------------------------------------------------------------------+

╔════════════════════════════════════════════════════════════════════════════════════╗
║                                 DATASET DESCRIPTION                                ║
╠═══════════════════════╦════════════════════════════════════════════════════════════╣
║        song_id        ║                  Spotify ID for the song.                  ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║       song_name       ║                         Song name.                         ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║       artist_id       ║            List of Spotify IDs for the artists             ║
║                       ║                   who performed the song.                  ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║      artist_name      ║                    List of artist names.                   ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║       popularity      ║                 Song popularity on Spotify.                ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║        explicit       ║        Whether or not the track has explicit lyrics.       ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║       song_type       ║     Whether the song is a collaboration or not (Solo).     ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║      track_number     ║                   The number of the song.                  ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║      num_artists      ║           Number of artists who perform the song.          ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║ num_available_markets ║              Number of countries in which the              ║
║                       ║                     song can be played.                    ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║      release_date     ║                  Release date of the song.                 ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║      duration_ms      ║         The duration of the track in milliseconds.         ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║          key          ║            The estimated overall key of a song,            ║
║                       ║        mapped as an integer number (e.g. C=0, C#=1).       ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║          mode         ║   The general modality of a song (i.e., major or minor).   ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║     time_signature    ║         The amount of beats in each bar (measure).         ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║      acousticness     ║             Informs the probability of a song              ║
║                       ║                   to be acoustic or not.                   ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║      danceability     ║          Combines tempo, rhythm and other elements         ║
║                       ║        to inform if a song is suitable for dancing.        ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║         energy        ║     Represents the intensity and activity of a song by     ║
║                       ║   combining information such as dynamic range, perceived   ║
║                       ║     loudness, timbre, onset rate, and general entropy.     ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║    instrumentalness   ║          Measures the probability of a song to be          ║
║                       ║         instrumental, that is, not contain vocals.         ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║        liveness       ║       Detects the presence of an audience in a song.       ║
║                       ║       The higher the liveness value, the higher the        ║
║                       ║         probability of a song being performed live.        ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║        loudness       ║       The general loudness measured in decibels (dB).      ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║      speechiness      ║            Measures the probability of a given             ║
║                       ║              song to have spoken words in it.              ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║        valence        ║         Describes the positiveness within a song.          ║
║                       ║        High valence values represent happier songs,        ║
║                       ║        whereas low values characterize the opposite.       ║
╠═══════════════════════╬════════════════════════════════════════════════════════════╣
║         tempo         ║ The speed of the song, measured in beats per minute (BPM). ║
╚═══════════════════════╩════════════════════════════════════════════════════════════╝