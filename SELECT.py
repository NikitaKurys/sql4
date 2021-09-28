import concurrent.futures

import sqlalchemy
import psycopg2
from pprint import pprint

conn = psycopg2.connect(dbname='NewDataBase', user='postgres',
                         password='Hjuvfyhjuvfy321', host='localhost')
cursor = conn.cursor()


# количество исполнителей в каждом жанре;
def displaying_artist():
    cursor.execute('''SELECT genre_id, COUNT(artist_id) FROM artist_genre
    GROUP BY genre_id 
    ORDER BY COUNT(artist_id) DESC;
        ''')
    result = cursor.fetchall()
    pprint(f'{result}')


# количество треков, вошедших в альбомы 2019-2020 годов;
def displaying_track():
    cursor.execute('''SELECT COUNT(track.name) FROM track
    JOIN album ON track.album_id = album.id
    WHERE releasedate BETWEEN '2019-01-01' AND '2020-12-31';
        ''')
    result = cursor.fetchall()
    pprint(f'{result}')


# средняя продолжительность треков по каждому альбому;
def displaying_sum_track():
    cursor.execute('''SELECT album.name, SUM(track.tracklength) FROM track
    JOIN album ON track.album_id = album.id
    GROUP BY album.name
    ORDER BY SUM(track.tracklength) DESC
    ;
        ''')
    result = cursor.fetchall()
    pprint(f'{result}')

# все исполнители, которые не выпустили альбомы в 2020 году;
def displaying_artist_2020():
    cursor.execute('''SELECT artist.name FROM album_artist AS aa
    JOIN artist ON aa.artist_id = artist.id
    JOIN album ON aa.album_id = album.id 
    WHERE album.releasedate NOT BETWEEN '2020-01-01' AND '2020-12-30'
    GROUP BY artist.name;
    ''')
    result = cursor.fetchall()
    pprint(f'{result}')


# названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
def displaying_collection_artist():
    cursor.execute('''SELECT collections.name FROM collections_track AS ct
    JOIN collections ON ct.collections_id = collections.id
    JOIN track ON ct.track_id = track.id
    JOIN album ON track.album_id = album.id 
    JOIN album_artist AS aa ON album.id = aa.album_id
    JOIN artist ON artist.id = aa.artist_id
    WHERE artist.name iLIKE '%%artist_6%%'
    GROUP BY collections.name
    ;
    ''')
    result = cursor.fetchall()
    pprint(f'{result}')


# название альбомов, в которых присутствуют исполнители более 1 жанра;
def displaying_album_genre():
    cursor.execute('''SELECT album.name FROM artist_genre AS ag
    JOIN genre ON ag.genre_id = genre.id
    JOIN artist ON ag.artist_id = artist.id
    JOIN album_artist ON album_artist.artist_id = artist.id 
    JOIN album ON album_artist.album_id = album.id
    GROUP BY album.name
    HAVING COUNT(genre.name) > 1
    ORDER BY album.name
    ;
    ''')
    result = cursor.fetchall()
    pprint(f'{result}')


# наименование треков, которые не входят в сборники;
def displaying_track_collections():
    cursor.execute('''SELECT track.name FROM track
    JOIN collections_track AS ct ON ct.collections_id = track.id
    WHERE ct.track_id is NULL
    ;
    ''')
    result = cursor.fetchall()
    pprint(f'{result}')


# исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
def displaying_short_track():
    cursor.execute('''SELECT artist.name, track.tracklength FROM track 
    JOIN album ON track.album_id = album.id 
    JOIN album_artist AS aa ON album.id = aa.album_id
    JOIN artist ON artist.id = aa.artist_id
    GROUP BY artist.name, track.tracklength
    HAVING track.tracklength = (SELECT min(tracklength) FROM track)
    ORDER BY artist.name
    ;
    ''')


#название альбомов, содержащих наименьшее количество треков.
def displaying_album_track():
    cursor.execute('''SELECT album.name FROM album
    JOIN track ON album.id = track.album_id
    WHERE track.album_id IN (
    SELECT album_id
    FROM track
    GROUP BY album_id
    HAVING COUNT(id) = (
        SELECT COUNT(id)
        FROM track
        GROUP BY album_id
        ORDER BY count
        LIMIT 1
    )
)
ORDER BY album.name
    ''')
    result = cursor.fetchall()
    pprint(f'{result}')
