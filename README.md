# retype
A simple tool to secretly manipulate the entered text while someone is typing

# Motivation

The basic idea was to write a programme that listens for keyboard events like a keylogger and then, if necessary, intervenes in a "maliciously correcting" way. The following attack scenario would then be possible: The victim types in the domain `www.domain.de`, `retype.py` recognises it and rewrites it to `www.dornain.com`. This could be used to lure the user to malicious websites. 

## Warning

### DONT USE THE TOOL AT THE MOMENT! THIS IS WORK IN PROGRESS AND WILL NOT WORK! 

This software is for educational and [show hacking purposes](https://www.showhacking.de) only! Do not use it to harm anyone 
(and honestly, any virus scanner or EDR should blow this thing completely to pieces)! By 
using my application you automatically agree to all laws that apply to you and take responsibility 
for your actions! Violation of laws can have serious consequences! As the developer, I do not 
accept any liability and am not responsible for any misuse or damage caused by this program. 

## Target architecture

- Windows

The use of `auto-py-to-exe` is strongly recommended!

