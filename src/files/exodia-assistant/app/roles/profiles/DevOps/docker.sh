#!/bin/bash

sudo systemctl start docker.service
sudo systemctl start containerd.service
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
