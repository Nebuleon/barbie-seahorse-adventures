#!/bin/bash

rm -rf .release
mkdir .release
cp gcw0/* .release/
cp run_game.py .release/
cp icon32.png .release/barbie-seahorse-adventures.png
mkdir .release/data
cp data/{codes.tga,tiles.tga,title.png} .release/data/
mkdir .release/data/bkgr
cp data/bkgr/{1,2,3,4,5,6,7,8}.png .release/data/bkgr/
mkdir .release/data/fonts
cp data/fonts/{04B_20__.TTF,about.gif} .release/data/fonts/
cp -r data/images .release/data/
mkdir .release/data/levels
cp data/levels/{phil_{1,2,5,7,8,10,12,13,14},tim_{2,4},pekuja_{1,3},boss_1}.tga .release/data/levels/
cp -r data/music .release/data/
cp -r data/sfx .release/data/
mkdir .release/lib
cp lib/{__init__,blob,boss,brobo,bubble,capsule,cnst,codes,data,door,fireball,fireguy,frog,init,laser,level,levels,main,menu,panda,parrot,platform,player,points,rendercache,robo,shootbot,spikey,sprite,sprites,tile,tiles,tiles_basic}.py .release/lib/
mkdir .release/lib/pgu
cp lib/pgu/{__init__,engine,timer}.py .release/lib/pgu/
mksquashfs .release barbie-1.1.opk -noappend -no-xattrs -all-root
