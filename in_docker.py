#!/usr/local/bin/python3
import json
import sys
import os
import string
import random
import sqlite3
import docker
import importlib
import copy
from db import PydoiDB

def main():
    ( conf, files ) = parseInput()
    inputConf = copy.deepcopy(conf)
    conf['files'] = files
    
    # Log the run
    
    if not 'lang' in conf:
        raise Exception("Language is not specified")
    
    lang = conf['lang']
    
    conf['langMod'] = langMod = importlib.import_module( 'lang.' + lang + '.main' )
    conf['langCls'] = langCls = getattr( langMod, 'Lang' + lang.capitalize() )
    db = PydoiDB()
    conf['langInst'] = langCls(conf,db,inputConf)
    
    uid = conf['uid'] = gen_random_id()
    
    print( "UID: " + uid + "\n" )
    
    # Sets conf.folder and conf.mount
    build_folders( conf )
    
    handleGeneric( conf )
    #if lang == 'python3':
    #    handlePython3( code, conf, folder, mount )
        
    cleanup( conf )
    sys.exit(0)

# ===== Functions ==========

def handleGeneric( conf ):
    lang = conf['langInst']
    imgName = lang.get_image()
    lang.write_files()
    docker_run( conf, imgName )

def parseInput():
    rawJson = ""
    files = {}
    code = ""
    filename = ""
    inFiles = False
    for line in sys.stdin:
        if line.startswith( "--" ):
            if filename != "":
                files[filename] = code
            filename = line[2:-1]
            if filename == "":
                filename = "main"
            code = ""
            inFiles = True
            continue
        if inFiles:
            code += line
        else:
            rawJson += line

    files[filename] = code
        
    try:
        conf = json.loads( rawJson )
    except JSONDecodeError as err:
        print( "Could not decode JSON: %s" % err )
        sys.exit(0)
        
    return ( conf, files )

def gen_random_id():
    chars = string.ascii_lowercase + string.digits
    char1 = random.choice(string.ascii_lowercase)
    uid = char1 + ''.join( random.choice(chars) for i in range(6) )
    return uid

def build_folders( conf ):
    uid = conf['uid']
    
    if not os.path.exists('tmp/'):
        try:
            os.mkdir('tmp/')
        except OSError:
            print ("Creation of the directory 'tmp/' failed")
            raise
    
    folder = conf['folder'] = "tmp/" + uid
    mount = conf['mount'] = folder + '/mount'
    try:
        os.mkdir( folder )
    except OSError:
        print ("Creation of the directory %s failed" % folder )
        raise
        
    try:
        os.mkdir( mount )
    except OSError:
        print ("Creation of the directory %s failed" % mount )
        raise
        
#def teardown_folders( uid ):
#    pass
    # todo

# Search through our local list of prebuilt containers; use appropriate one if available



# Run the container

def docker_run( conf, imgName ):
    # Docker API is buggy; for whatever reason it doesn't know about image CMDs right after they are build
    client = docker.from_env()
    folder = os.path.abspath( conf['folder'] )
    client.containers.run( imgName, None, volumes = {
        ( folder + '/mount' ) : {'bind': '/mnt/scripts/', 'mode': 'rw'},
        ( folder + '/logs' ) : {'bind': '/mnt/logs/', 'mode': 'rw'}
    } )
    #cmd = "docker run -v '%s/mount:/mnt/scripts/' -v '%s/logs:/mnt/logs' %s" % ( folder, folder, imgName )
    #print( "Cmd: " + cmd )
    #os.system(cmd)

# === Cleanup ===

def cleanup( folder ):
    # Delete files in folder
    
    # os.rmdir( folder )
    pass

# ======== CODE ========

if __name__ == '__main__':
    main()