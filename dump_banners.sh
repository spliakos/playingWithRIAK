#!/bin/bash

cd "$(dirname "$0")"
curwd=$(pwd)
ban_key_dir='banners-keys'
ban_val_dir='banners-values'
NOW=$(date +"%Y%m%d_%H%M%S")

if [ -d ${curwd}/${ban_key_dir} ]; then
  rm -rf ${curwd}/${ban_key_dir}
fi
if [ -d ${curwd}/${ban_val_dir} ]; then
  rm -rf ${curwd}/${ban_val_dir}
fi

python cache_dumper_banners.py int-api-sports-sb-riak:8098

tar cvzf riak.banners.$NOW.tar.gz $ban_key_dir $ban_val_dir

find $curwd -name '*.tar.gz' -type f -mtime +10 -exec rm {} \;

