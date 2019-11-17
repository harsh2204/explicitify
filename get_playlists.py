import spotipy
import spotipy.util as util
import os
import json
from pprint import pprint

with open('token', 'r') as f:
    entries = f.read().split("\n")

    for e in entries:
        k, v = e[7:].replace('\'', '').split('=')
        os.environ[k] = v

uri = "spotify:playlist:18w7xWsFxlXBJzPE4bIdSu"
# exit(0)
scope = 'user-library-read'

token = util.prompt_for_user_token('harsh2204', scope)

if token:

    if os.path.isfile('track_list.json'):
        exp_vers = []
        not_founds = []
        with open('track_list.json', 'r') as f:
            data = json.loads(f.read())
            sp = spotipy.Spotify(auth=token)
            total = len(data)
            for i, track in enumerate(data):
                track = track.popitem()
                q_string = f"{track[0]} {track[1][0]}"
                results = sp.search(q_string, limit=25)
                found = False
                for r in results['tracks']['items']:
                    if found:
                        break
                    if r['explicit'] and r['name'] == track[0]:
                        exp_vers.append((r['name'], r['uri']))
                        found = True
                if not found:
                    not_founds.append(track[0])
                    print(i, " Explicit track not found for", track[0])
        pprint(exp_vers)
        with open('explicit_links.json', 'w') as outf:
            outf.write(json.dumps(exp_vers, indent=2, sort_keys=True))
        with open('not_founds.json', 'w') as outf:
            outf.write(json.dumps(not_founds, indent=2, sort_keys=True))

        print(f"Found ({len(exp_vers)}/{total}) explicit versions of tracks")

    else:
        track_names = []
        sp = spotipy.Spotify(auth=token)
        # results = sp.current_user_playlists(limit=50)
        results = sp.user_playlist('harsh2204', uri, fields="tracks,next")
        tracks = results['tracks']
        for track in tracks['items']:
            t = track['track']
            track_names.append({t['name']:[a['name'] for a in t['artists']]})
            print(t['name'])
        tracks = sp.next(tracks)
        for track in tracks['items']:
            t = track['track']
            track_names.append({t['name']:[a['name'] for a in t['artists']]})
            print(t['name'])

        with open('track_list.json', 'w') as outf:
            outf.write(json.dumps(track_names, indent=2, sort_keys=True))

else:
    print("Can't get token for", 'harsh2204')