#!/bin/bash

cd "$(dirname "$0")"
curwd=$(pwd)
ban_key_dir='banners-keys'
ban_val_dir='banners-values'
NOW=$(date +"%Y%m%d_%H%M%S")
file=$1

if [ -d ${curwd}/${ban_key_dir} ]; then
  rm -rf ${curwd}/${ban_key_dir}
fi
if [ -d ${curwd}/${ban_val_dir} ]; then
  rm -rf ${curwd}/${ban_val_dir}
fi

tar xzf $file

i=0
for file1 in banners-keys/*
do
  i=$((i+1))
  file=`echo $file1 | cut -d'/' -f 2 | cut -d'_' -f 1`
  cp banners-values/${file}_res banners-keys/
  echo "Processing banner ${file}..."
  python cache_loader_banners.py banners-keys/${file}
  rm -f banners-keys/${file}_res
done

echo "Banners load into WDC Riak complete."


