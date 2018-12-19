# Multi-agent movie rating prediction
Predict movie score using contents of its review.

## Prosody 
It's an xmpp server that will be used by SPADE to coordinate message exchange between agents

## Project setup
* pip install -r requirements.txt
* install prosody `apt install prosody`
* place `prosody.cfg.lua` in `/etc/prosody/`
* make sure current user has access to it: 
```bash
chown `whoami` /etc/prosody -R
```
* restart prosody `systemctl restart prosody`
* add exemplary user to prosody using 
`prosodyctrl adduser <name>@localhost`
* in my case restart was required for everything to work, so maybe you should also try it in case of any problems :)

## Conceptual requirements
* system should work when some of the agents are disabled
* knowledge must be distributed among agents

