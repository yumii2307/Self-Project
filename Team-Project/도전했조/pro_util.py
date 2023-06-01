import numpy as np
import pandas as pd
import os, re, string, joblib

def search_songs(key_title, key_artist, app):

    filename = os.path.join(app.static_folder, 'data/melon_song_v3.csv')

    try:
        df = pd.read_csv(filename)
    except:
        return []
    
    df.date.fillna(0, inplace=True)
    df['date'] = df.date.astype(int).astype(str)
    df.fillna('', inplace=True)
    df.songId = df.songId.astype(str)
    
    key_title = re.sub('['+string.punctuation+']', '', key_title)
    key_artist = re.sub('['+string.punctuation+']', '', key_artist)

    songIds =  df[df.title.str.replace('['+string.punctuation+']','', regex=True).str.contains(key_title, case=False) 
                  & df.artist.str.replace('['+string.punctuation+']','', regex=True).str.contains(key_artist, case=False)][['songId', 'title', 'artist', 'album', 'date', 'img']].to_dict('records')

    return songIds

def propose(find_songId, app):

    def get_recommendation(songId, cos_sim):
        index = indices[songId]
        sim_scores = pd.Series(cos_sim[index])
        song_indices = sim_scores.sort_values(ascending=False).head(31).tail(30).index
        return df.songId.iloc[song_indices]
    
    try:
        filename = os.path.join(app.static_folder, 'data/melon_song_v3.csv')
        plist_filename1 = os.path.join(app.static_folder, 'data/melon_playlist1.csv')
        plist_filename2 = os.path.join(app.static_folder, 'data/melon_playlist2_v2.csv')
        cosine_sim_filename = os.path.join(app.static_folder, 'data/melon_cosine_sim.sim')
 
        df = pd.read_csv(filename)
        plist1 = pd.read_csv(plist_filename1)
        plist2 = pd.read_csv(plist_filename2)
        cosine_sim = joblib.load(cosine_sim_filename)

    except:
        return print(app.static_folder), {}, [], [], []
    
    plist1.plylstSeq = plist1.plylstSeq.astype(str)
    plist2.songId = plist2.songId.astype(str)

    df.date.fillna(0, inplace=True)
    df['date'] = df.date.astype(int).astype(str)
    df.fillna('', inplace=True)
    df['comment_like_total'] = df.comment + df.like
    df['songId'] = df.songId.astype(str)
    df.lyric = df.lyric.str.replace('\r', '')

    self_song = df[df.songId == find_songId][['title', 'artist', 'album', 'date', 'img', 'genre', 'ly_summary']].to_dict('records')[0]
    
    indices = pd.Series(df.index, index=df.songId)

    a = get_recommendation(find_songId, cosine_sim).to_frame()
    pro_contents = df[df['songId'].isin(a.songId[1:6])][['songId', 'title', 'artist', 'img']].to_dict('records')
    
    numbers = df['comment_like_total']
    sorted_numbers = np.sort(numbers)
    q1 = np.percentile(sorted_numbers, 25)
    q2 = np.percentile(sorted_numbers, 50)
    filtered_data = df[(df['comment_like_total'] >= q1) & (df['comment_like_total'] < q2)]
    filtered_data = filtered_data[['songId', 'comment_like_total']]
    
    d = a[a['songId'].isin(filtered_data.songId.values)].head(5)
    pro_meong = df[df['songId'].isin(d.songId.values[:5])][['songId', 'title', 'artist', 'img']].to_dict('records')

    tags = np.unique(' '.join(plist1[plist1.songIds.str.contains(find_songId)]['tag'].values).split(), return_counts=True)

    if len(tags[0]) :
        re_count = np.argsort(-tags[1]) 
        if len(re_count) > 2:
            pro_tags = f"{tags[0][re_count][0].strip('#')}, {tags[0][re_count][1].strip('#')} 그리고 {tags[0][re_count][2].strip('#')}"
        elif len(re_count) == 2:
            pro_tags = f"{tags[0][re_count][0].strip('#')} 그리고 {tags[0][re_count][1].strip('#')}"
        else:
            pro_tags = f"{tags[0][re_count][0].strip('#')}"

    else:
        pro_tags = ''

    songs = np.unique(' '.join(plist1[plist1.songIds.str.contains(find_songId)]['songIds'].values).replace(find_songId + ' ', '').split(), return_counts=True)

    cnt = 0
    song_list = []

    for s_id in songs[0][np.argsort(-songs[1])]:    
        if not df[df.songId.isin([s_id])].empty :
            cnt += 1
            song_list.append(s_id)
        if cnt == 5 : break
    
    pro_psongs = df[df.songId.isin(song_list)][['songId', 'title', 'artist', 'img']]

    if pro_psongs.empty:
        pro_psongs = plist2[plist2.songId.isin(song_list)]

    pro_psongs = pro_psongs.to_dict('records')

    print(find_songId)

    return pro_tags, self_song, pro_contents, pro_meong, pro_psongs
