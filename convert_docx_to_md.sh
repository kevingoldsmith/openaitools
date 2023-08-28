#!/bin/bash

pandoc -c basic.css -f docx "$1" -so "$2"