####Radius Server on Yosemite

Radius server exists in Yosemite server, but is not configurable using the Server app unless you're using an Airport Base Station. Therefore we need to use the command line.

Open Terminal. Note that almost everything will need to be run as su (sudo is your friend).

Choose the certificate you want to use for the basis of your encrypted sessions. **hint** In Server -> Certificates take a look at the SHA1 fingerprint. It will be (without spaces) used in the filename for the associated files.

Your certificate will be in the folder: /etc/certificates and will have the format hostname.SHA1 fingerprint.xxx.pem
(like /etc/certificates/host.example.com.CD34AF6792E9A2BF9.key.pem). You're interested in three files, the key, the certificate and the chain.

Note that these should be kept confidential, so don't make copies. Instead we will import the location in to the radius conf file. The followinf command will do this. Note that it is all one line and that the order is (proably, I didn't test it) important:

sudo radiusconfig -installcerts /etc/certificates/hostname.SHA1 fingerprint.key.pem /etc/certificates/hostname.SHA1 fingerprint.cert.pem /etc/certificates/hostname.SHA1 fingerprint.chain.pem

Your key is encrypted (this is a good thing, but we don't know what the password is. Fortunately, your keychain does. Tell radius by having it ask you for the password:

sudo radiusconfig -setcertpassword

and responding with the magic incantation:
Apple:UserCertAdmin

(note that there are no spaces).

Now it's time to check your config. Make sure radius is not running (sudo radiusconfig -stop) and start it in foreground mode:

sudo radiusd -X

If you're happy with it so far, cquit (Ctrl-c) and continue by adding your base station / radis devices:

#####radiusconfig -addclient BASE_STATION  SHORTNAME
	radiusconfig -addclient 192.168.2.9 netgear-switch-1 other

##### make sure it got added correctly
	radiusconfig -naslist


Again, check that all is well...
	radiusd -sfX

#####Finally launch it using the launchd 
	launchctl load /System/Library/LaunchDaemons/org.freeradius.radiusd.plist


#####if while testing you're banging your head against a wall because your client computer can't authenticate,  remove the 802.1X Password for the Wireless from your login keychain and it should re-ask for username and password.

