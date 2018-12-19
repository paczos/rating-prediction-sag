# rating-prediction-sag
Predict movie score using contents of its review.

## setup
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

