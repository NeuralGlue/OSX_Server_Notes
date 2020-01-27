# Dovecot and Master Passwords (OSX Server 5.2)
Dovecot allows a master user to login to someone else's mail account. This is particularly useful when migrating servers or for backup scripts to live backups.

Should you need to be able to authenticate using a master password for all (or some) users on your OSX Server do the following:

1. In /Library/Server/Mail/Config/dovecot/conf.d/10-auth.conf uncomment and set the following lines: 
```
auth_master_user_separator = *
!include auth-master.conf.ext
```
2. Ensure that the auth-master.conf.ext (in the same directory) is set to the defaults:
```
passdb {
  driver = passwd-file
  master = yes
  args = /Library/Server/Mail/Config/dovecot/master-users

  # Unless you're using PAM, you probably still want the destination user to
  # be looked up from passdb that it really exists. pass=yes does that.
  pass = yes
}
```
3. Create a passdb file in the path above. Replace the "my master user" and "my master password" placeholders in the line below with a new username and password. The user can not be an existing user. I generally make it something like 'administrative-access'.
```
htpasswd -b -c -s /Library/Server/Mail/Config/dovecot/master-users <my master user> <my master password>
```
4. OSX Server uses ACLs to control access to user's folders. You will need to create a global override for the folders you want access to. For most purposes you will want this to be read and list everything. Add a file to
/Library/Server/Mail/Config/dovecot/global-acls:
```
sudo echo "user=<my master user> lr" > /Library/Server/Mail/Config/dovecot/global-acls/.DEFAULT
```
Note above that the user must be whatever is in your master-users file and the filename in the global-acls directory must named for the folder for which you want access. For example, if you just wanted access to INBOX then the file name would be INBOX. If you wanted access to current, then it would be INBOX.cur.
The .DEFAULT name is a special one that means all folders.

5. Reload your dovecot configuration. I generally do this and set the log level to debug at the same time (serveradmin does a reload conf if you change a setting) so I can see if I've made any mistakes. *Don't forget to turn debug logging off again once you've verified it works*
```
sudo serveradmin settings mail:imap:log_level=debug
```
6. Verify the connections using the following set of commands:
```
openssl s_client -crlf -connect <your mail server>:993
tag login <target user>*<my master user> <my master password>
tag STATUS INBOX (MESSAGES UNSEEN RECENT)
tag logout
```

**Only leave master password enabled when you absolutely need it**

