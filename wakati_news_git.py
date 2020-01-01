# -+- coding:utf-8 -*-
import MeCab
import re
import glob

#空白で分かち書きをする
def wakati(text):
    #neologd
    tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')#mecabのパス
    tagger.parse('')
    node = tagger.parseToNode(text)
    word_list = []
    while node:
        pos = node.feature.split(",")
        if pos[0] in ["名詞", "動詞", "形容詞"]:
            if pos[0] == "動詞": #動詞は標準型に直す
                word = pos[6]
                word_list.append(word)
            else:
                word = node.surface.lower() #英語は全て小文字に変換
                word_list.append(word)
        node = node.next
    return " ".join(word_list)

#tfidfベクトルを計算してファイル出力
def write_wakati(name_list):
    docs = []
    title = ""
    for n in name_list:
        with open(n, 'r') as rfile:
            lines = rfile.readlines()
            lines = lines[2:] #3行目から本文
            docs.append(wakati("".join(lines)))
            title += re.findall('./data/news/.*/(.*).txt', n)[0]+"\n"

    with open("./data/news_ma/news_wakati.txt", 'w') as wfile:
        #ファイル名を記録
        wfile.write("\n".join(docs))

    return

if __name__=='__main__':
    #テキストファイル名を取得
    movie_name = glob.glob("./data/news/movie-enter/movie-enter-*.txt")
    sports_name = glob.glob("./data/news/sports-watch/sports-watch-*.txt")
    movie_name.extend(sports_name) #配列を統合
    write_wakati(movie_name)
    print("映画関連の記事数: {0}\nスポーツ関連の記事数: {1}".format(len(movie_name)-len(sports_name), len(sports_name)))
