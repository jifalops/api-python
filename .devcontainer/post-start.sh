#!/usr/bin/env bash

# Make sure containerd and dockerd are running.
sudo nohup containerd &
sudo nohup dockerd &
