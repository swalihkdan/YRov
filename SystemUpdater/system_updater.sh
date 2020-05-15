#!/usr/bin/env bash

wget "https://tinyurl.com/yrov-puppet" -O yrov.pp
puppet apply yrov.pp