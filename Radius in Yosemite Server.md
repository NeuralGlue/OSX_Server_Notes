####Radius Server on Yosemite

Radius server exists in Yosemite server, but is not configurable using the Server app unless you're using an Airport Base Station. Therefore we will need to configure it using the command line.

Decide which certificate you want to use for the basis of your encrypted sessions. In Server -> Certificates open the certificate you want to use and take a look at the SHA1 fingerprint (it will be at the bottom of the info page). This finger print will be (without spaces) used in the filename for the associated files. Either write down the fingerprint, or leave the window visible.

Open Terminal. Note that almost everything will need to be run as su (sudo is your friend).

Your certificate will be in the folder: /etc/certificates and will have the format hostname.SHA1 fingerprint.xxx.pem
(like /etc/certificates/host.example.com.CD34AF6792E9A2BF9.key.pem). You're interested in three files, the key, the certificate and the chain. Note that you'll need to sudo to ls these directories.

	sudo ls /etc/certificates

Note that these should be kept confidential, so don't make copies. Instead we will import the location in to the radius conf file. The following command will do this. Note that it is all one line and that the order is (probably, I didn't test it) important:

	sudo radiusconfig -installcerts /etc/certificates/hostname.SHA1 fingerprint.key.pem /etc/certificates/hostname.SHA1 fingerprint.cert.pem /etc/certificates/hostname.SHA1 fingerprint.chain.pem

Your key is encrypted (this is a good thing), but we don't know what the password is. Fortunately, your keychain does. Tell radius by having it ask you for the passphrase:

	sudo radiusconfig -setcertpassword

and responding with the magic incantation:

	Apple:UserCertAdmin

(note that there are no spaces in the passphrase).

Now it's time to check your config. Make sure radius is not running (sudo radiusconfig -stop) and start it in foreground mode:

	sudo radiusd -X

If you're happy with it so far, cquit (Ctrl-c) and continue by adding your base station / radius devices:
radiusconfig -addclient BASE_STATION  SHORTNAME TYPE
	radiusconfig -addclient 192.168.2.9 netgear-switch-1 other

make sure it got added correctly
	radiusconfig -naslist


Again, check that all is well...

	radiusd -sfX

Finally launch it using the launchd system:

	sudo launchctl enable system/org.freeradius.radiusd

(did you notice that launchctl has changed again!)

#####if while testing you're banging your head against a wall because your client computer can't authenticate,  remove the 802.1X Password for the Wireless from your login keychain and it should re-ask for username and password.

