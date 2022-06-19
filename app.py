from unicodedata import name
from flask import Flask, jsonify, render_template, Response
import flask
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://admin:admin@cluster0.n5ow2vn.mongodb.net/streaming?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route("/AllUsers", methods=['GET'])
def getAllUsers():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route("/AllMusics", methods=['GET'])
def getAllMusics():
    musicas = mongo.db.musics.find()
    response = json_util.dumps(musicas)
    return Response(response, mimetype='application/json')

@app.route("/PlaylistsByUser/<userId>", methods=['GET'])
def getAllPlaylistsByUser(userId):
    playlist = mongo.db.playlists.find({'userId': ObjectId(userId)})
    response = json_util.dumps(playlist)
    return Response(response, mimetype='application/json')

@app.route("/MusicsByPlaylist/<playlistids>", methods=['GET'])
def getAllMusicsByPlaylist(playlistids):
    playlistid = mongo.db.musics.find({'playlistIds': ObjectId(playlistids)}, {'playlistIds': 0})
    response = json_util.dumps(playlistid)
    return Response(response, mimetype='application/json')

@app.route("/PlaylistsByMusic/<id_music>", methods=['GET'])
def getAllPlaylistsByMusic(id_music):
    music = mongo.db.musics.find_one({'_id': ObjectId(id_music)})
    playlists = mongo.db.playlists.find({"_id":{"$in": music['playlistIds']}})
    response = json_util.dumps(playlists)
    return Response(response, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)