#!/bin/bash

sudo systemctl restart NetworkManager

systemctl status NetworkManager > restartnm.log
