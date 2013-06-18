Summary:	A high-performance mail server with IMAP, POP3, NNTP and SIEVE support
Name:		cyrus-imapd
Version:	2.4.17
Release:	1
License:	BSD
URL:		http://www.cyrusimap.org/
Group:		BLFS/MailServer
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	ftp://ftp.cyrusimap.org/cyrus-imapd/%{name}-%{version}.tar.gz
%define _cyrususer cyrus
%define _cyrusgroup mail
%define ssl_pem_file %{_sysconfdir}/pki/%{name}/%{name}.pem
%define _cyrexecdir %{_exec_prefix}/lib/%{name}
%define	_sysconfdir /etc
%description
The %{name} package contains the core of the Cyrus IMAP server.
It is a scaleable enterprise mail system designed for use from
small to large enterprise environments using standards-based
internet mail technologies.

A full Cyrus IMAP implementation allows a seamless mail and bulletin
board environment to be set up across multiple servers. It differs from
other IMAP server implementations in that it is run on "sealed"
servers, where users are not normally permitted to log in and have no
system account on the server. The mailbox database is stored in parts
of the file system that are private to the Cyrus IMAP server. All user
access to mail is through software using the IMAP, POP3 or KPOP
protocols. It also includes support for virtual domains, NNTP,
mailbox annotations, and much more. The private mailbox database design
gives the server large advantages in efficiency, scalability and
administratability. Multiple concurrent read/write connections to the
same mailbox are permitted. The server supports access control lists on
mailboxes and storage quotas on mailbox hierarchies.

The Cyrus IMAP server supports the IMAP4rev1 protocol described
in RFC 3501. IMAP4rev1 has been approved as a proposed standard.
It supports any authentication mechanism available from the SASL
library, imaps/pop3s/nntps (IMAP/POP3/NNTP encrypted using SSL and
TLSv1) can be used for security. The server supports single instance
store where possible when an email message is addressed to multiple
recipients, SIEVE provides server side email filtering.
%prep
%setup -q
# only to update config.* files
automake -a -f -c || :
aclocal -I cmulocal
autoheader
autoconf -f
# Modify docs master --> cyrus-master
%{__perl} -pi -e "s@master\(8\)@cyrus-master(8)@" man/*5 man/*8 lib/imapoptions
sed -i -e 's|\([^-]\)master|\1cyrus-master|g;s|^master|cyrus-master|g;s|Master|Cyrus-master|g;s|MASTER|CYRUS-MASTER|g' man/master.8 doc/man.html
# Modify path in perl scripts
find . -type f -name "*.pl" | xargs %{__perl} -pi -e "s@/usr/local/bin/perl@%{__perl}@"
# modify lmtp socket path in .conf files
%{__perl} -pi -e "s@/var/imap/@%{_var}/lib/imap/@" master/conf/*.conf doc/cyrusv2.mc
# enable idled in .conf files to prevent error messages
%{__perl} -pi -e "s/#  idled/  idled/" master/conf/*.conf
# Fix permissions on perl programs
find . -type f -name "*.pl" -exec chmod 755 {} \;
%build
CPPFLAGS="%{optflags} -fno-strict-aliasing"; export CPPFLAGS
CFLAGS="%{optflags} -fPIC -fno-strict-aliasing"; export CFLAGS
CCDLFLAGS="-rdynamic"; export CCDLFLAGS
LDFLAGS="-Wl,-z,now -Wl,-z,relro"
./configure \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--with-perl=%{__perl} \
	--with-cyrus-prefix=%{_cyrexecdir} \
	--with-service-path=%{_cyrexecdir} \
	--with-sasl \
	--with-perl \
	--with-auth=unix \
	--with-openssl \
	--without-ucdsnmp \
	--without-snmp
#make depend
#make %{?_smp_mflags}
make -C man -f Makefile.dist
make -C doc -f Makefile.dist
make %{?_smp_mflags}
make -C notifyd notifytest
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}
# This is needed to install the perl files correctly
pushd perl/imap
  %{__perl} Makefile.PL PREFIX=%{buildroot}%{_prefix} INSTALLDIRS=vendor
popd
pushd perl/sieve/managesieve
  %{__perl} Makefile.PL PREFIX=%{buildroot}%{_prefix} INSTALLDIRS=vendor
popd
# Do what the regular make install does
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} mandir=%{_mandir}
make -C man install DESTDIR=%{buildroot} PREFIX=%{_prefix} mandir=%{_mandir}
install -m 755 imtest/imtest       %{buildroot}%{_bindir}/
install -m 755 notifyd/notifytest  %{buildroot}%{_bindir}/
install -m 755 perl/imap/cyradm    %{buildroot}%{_bindir}/
# Install tools
for tool in tools/* ; do
  test -f ${tool} && install -m 755 ${tool} %{buildroot}%{_cyrexecdir}/
done
# Create directories
install -d \
	%{buildroot}%{_libdir}/sasl \
	%{buildroot}%{_var}/spool/imap \
	%{buildroot}%{_var}/lib/imap/{user,quota,proc,log,msg,socket,db,sieve,sync,md5,backup,meta} \
	%{buildroot}%{_var}/lib/imap/ptclient \
	%{buildroot}%{_sysconfdir}/pki/%{name} \
	%{buildroot}%{_sysconfdir}/cron.daily/%{name} \
	doc/contrib
# Install additional files
#install -p -m 644 master/conf/prefork.conf %{buildroot}%{_sysconfdir}/cyrus.conf
install -p -m 644 master/conf/normal.conf %{buildroot}%{_sysconfdir}/cyrus.conf
cat >> %{buildroot}%{_sysconfdir}/imapd.conf <<- "EOF"
configdirectory: /var/lib/imap
partition-default: /var/spool/imap
admins: cyrus
sievedir: /var/lib/imap/sieve
sendmail: /usr/sbin/sendmail
hashimapspool: true
sasl_pwcheck_method: saslauthd
sasl_mech_list: PLAIN LOGIN
allowplaintext: no
defaultdomain: mail
tls_cert_file: /etc/pki/cyrus-imapd/cyrus-imapd.pem
tls_key_file: /etc/pki/cyrus-imapd/cyrus-imapd.pem
tls_ca_file: /etc/pki/tls/certs/ca-bundle.crt
# uncomment this if you're operating in a DSCP environment (RFC-4594)
# qosmarking: af13
EOF
cat >>  %{buildroot}%{_sysconfdir}/logrotate.d/%{name} << "EOF"
/var/log/imapd.log /var/log/auth.log {
	missingok
	sharedscripts
	postrotate
		/bin/kill -HUP `cat /var/run/rsyslogd.pid 2> /dev/null` 2> /dev/null || true
	endscript
}
EOF
cat >> %{buildroot}%{_sysconfdir}/cron.daily/%{name} << "EOF"
#!/bin/sh
#
# This file is run on a daily basis to perform a backup of your
# mailbox list which can be used to recreate mailboxes.db from backup.
# Restore is done using ctl_mboxlist after uncompressing the file.
BACKDIR="/var/lib/imap/backup"
MBOXLIST="${BACKDIR}/mboxlist"
ROTATE=6
# fallback to su if runuser not available
if [ -x /sbin/runuser ]; then
	RUNUSER=runuser
else
	RUNUSER=su
fi
# source custom configuration
if [ -f /etc/sysconfig/cyrus-imapd ]; then
	. /etc/sysconfig/cyrus-imapd
fi
[ -x /usr/lib/cyrus-imapd/ctl_mboxlist ] || exit 0
[ -f /var/lib/imap/db/skipstamp ] || exit 0
# rotate mailbox lists
seq $[ $ROTATE - 1 ] -1 1 | while read i; do
	[ -f ${MBOXLIST}.${i}.gz ] && mv -f ${MBOXLIST}.${i}.gz ${MBOXLIST}.$[ $i + 1 ].gz
done
[ -f ${MBOXLIST}.gz ] && mv -f ${MBOXLIST}.gz ${MBOXLIST}.1.gz
# export mailboxes.db
$RUNUSER - cyrus -s /bin/sh -c "umask 077 < /dev/null ; /usr/lib/cyrus-imapd/ctl_mboxlist -d | gzip > ${MBOXLIST}.gz"
exit 0
# EOF
EOF
# Cleanup of doc dir
find doc perl -name CVS -type d -prune -exec rm -rf {} \;
find doc perl -name .cvsignore -type f -exec rm -f {} \;
rm -f doc/Makefile.dist*
rm -f doc/text/htmlstrip.c
rm -f doc/text/Makefile
rm -rf doc/man
# fix permissions on perl .so files
find %{buildroot}%{_libdir}/perl5/ -type f -name "*.so" -exec chmod 755 {} \;
# fix conflicts with uw-imap
mv %{buildroot}%{_mandir}/man8/imapd.8 %{buildroot}%{_mandir}/man8/imapd.8cyrus
mv %{buildroot}%{_mandir}/man8/pop3d.8 %{buildroot}%{_mandir}/man8/pop3d.8cyrus
# Install templates
install -m 755 -d doc/conf
install -m 644 master/conf/*.conf doc/conf/
#############################################
# Generate db config file
( grep '^{' lib/imapoptions | grep _db | cut -d'"' -f 2,4 | \
  sed -e 's/^ *//' -e 's/-nosync//' -e 's/ *$//' -e 's/"/=/'
  echo sieve_version=2.2.3 ) | sort > %{buildroot}%{_datadir}/%{name}/rpm/db.cfg
##############################################
# create the ghost pem file
touch %{buildroot}%{ssl_pem_file}
# Rename 'master' binary and manpage to avoid clash with postfix
mv -f %{buildroot}%{_cyrexecdir}/master         %{buildroot}%{_cyrexecdir}/cyrus-master
mv -f %{buildroot}%{_mandir}/man8/master.8      %{buildroot}%{_mandir}/man8/cyrus-master.8
# Rename 'fetchnews' binary and manpage to avoid clash with leafnode
mv -f %{buildroot}%{_cyrexecdir}/fetchnews      %{buildroot}%{_cyrexecdir}/cyrus.fetchnews
mv -f %{buildroot}%{_mandir}/man8/fetchnews.8   %{buildroot}%{_mandir}/man8/cyrus.fetchnews.8
%{__perl} -pi -e 's|fetchnews|cyrus.fetchnews|g;s|Fetchnews|Cyrus.fetchnews|g;s/FETCHNEWS/CYRUS.FETCHNEWS/g' \
        %{buildroot}%{_mandir}/man8/cyrus.fetchnews.8
#remove executable bit from docs
for ddir in doc perl/imap/examples
do
	find $ddir -type f -exec chmod -x {} \;
done
# Remove installed but not packaged files
rm -f %{buildroot}%{_cyrexecdir}/not-mkdep
rm -f %{buildroot}%{_cyrexecdir}/config2header*
rm -f %{buildroot}%{_cyrexecdir}/config2man
rm -f %{buildroot}%{_cyrexecdir}/pop3proxyd
find %{buildroot} -name "perllocal.pod" -exec rm -f {} \;
find %{buildroot} -name ".packlist" -exec rm -f {} \;
rm -f %{buildroot}%{_mandir}/man8/syncnews.8*
find %{buildroot}%{perl_vendorarch} -name "*.bs" -exec rm -f {} \;
#	daemonize!
install -vdm 755 %{buildroot}/etc/rc.d/{,rc{0,1,2,3,4,5,6}.d,init.d}
cat >> %{buildroot}/etc/rc.d/init.d/imapd <<- "EOF"
#!/bin/sh
### BEGIN INIT INFO
# Provides:            imap
# Required-Start:      $syslog $local_fs $network
# Should-Start:        saslauthd
# Required-Stop:       $network
# Should-Stop:         saslauthd
# Default-Start:       3 4 5
# Default-Stop:        0 1 2 6
# Short-Description:   Cyrus imap MTA
# Description:         Controls the Cyrus Imap Mail Transfer Agent
### END INIT INFO
. /lib/lsb/init-functions
case "$1" in
	start)
		log_info_msg "Starting Cyrus Imap..."
		start_daemon /usr/cyrus/bin/master
		evaluate_retval
		;;
	stop)
		log_info_msg "Stopping Cyrus Imap..."
		killproc /usr/cyrus/bin/master
		evaluate_retval
		;;
	restart)
		$0 stop
		sleep 1
		$0 start
		;;
	*)
		echo "Usage: $0 {start|stop|restart}"
		exit 1
		;;
esac
# End /etc/rc.d/init.d/cyrus-imapd
EOF
ln -sf  ../init.d/imapd %{buildroot}/etc/rc.d/rc0.d/K50imapd
ln -sf  ../init.d/imapd %{buildroot}/etc/rc.d/rc1.d/K50imapd
ln -sf  ../init.d/imapd %{buildroot}/etc/rc.d/rc2.d/S35imapd
ln -sf  ../init.d/imapd %{buildroot}/etc/rc.d/rc3.d/S35imapd
ln -sf  ../init.d/imapd %{buildroot}/etc/rc.d/rc4.d/S35imapd
ln -sf  ../init.d/imapd %{buildroot}/etc/rc.d/rc5.d/S35imapd
ln -sf  ../init.d/imapd %{buildroot}/etc/rc.d/rc6.d/K50imapd

##############################################################
#make install DESTDIR=%{buildroot} PREFIX=%{_prefix} mandir=%{_mandir}
#make -C man install DESTDIR=%{buildroot} PREFIX=%{_prefix} mandir=%{_mandir}
#install -vdm 755 %{buildroot}/etc
#cp ./master/conf/normal.conf %{buildroot}/etc/cyrus.conf
#install -D -m644 COPYRIGHT %{buildroot}/usr/share/licenses/%{name}/LICENSE
#install -vdm 755 %{buildroot}/etc
#install -vdm 755 %{buildroot}/var/imap
#install -vdm 755 %{buildroot}/var/spool/imap
##############################################################

#	Kill files not packaged
find %{buildroot} -name "perllocal.pod" -exec rm -f {} \;
find %{buildroot} -name ".packlist" -exec rm -f {} \;
find %{buildroot}/%{_libdir} -name '*.a' -delete
#%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%pre
# Create 'cyrus' user on target host
getent group saslauth >/dev/null || /usr/sbin/groupadd -g 76 -r saslauth 
getent passwd cyrus >/dev/null || /usr/sbin/useradd -c "Cyrus IMAP Server" -d %{_var}/lib/imap -g mail \
  -G saslauth -s /sbin/nologin -u 76 -r cyrus
%post
/sbin/ldconfig
cat >> /etc/syslog.conf <<- "EOF"
#	Addition for cyrus-impad
local6.debug  /var/log/imapd.log_info_msg
auth.debug /var/log/auth.log
#	End cyrus-imapd
EOF
touch /var/log/auth.log
touch /var/log/imapd.log
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/cyrus.conf
%config(noreplace) %{_sysconfdir}/imapd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/imapd
%{_sysconfdir}/rc.d/rc0.d/K50imapd
%{_sysconfdir}/rc.d/rc1.d/K50imapd
%{_sysconfdir}/rc.d/rc2.d/S35imapd
%{_sysconfdir}/rc.d/rc3.d/S35imapd
%{_sysconfdir}/rc.d/rc4.d/S35imapd
%{_sysconfdir}/rc.d/rc5.d/S35imapd
%{_sysconfdir}/rc.d/rc6.d/K50imapd
%{_sysconfdir}/cron.daily/%{name}
%dir %{_cyrexecdir}
%{_cyrexecdir}/cyr_systemd_helper
%{_cyrexecdir}/arbitron
%{_cyrexecdir}/arbitronsort.pl
%{_cyrexecdir}/chk_cyrus
%{_cyrexecdir}/convert-sieve.pl
%{_cyrexecdir}/cyr_df
%{_cyrexecdir}/ctl_cyrusdb
%{_cyrexecdir}/ctl_deliver
%{_cyrexecdir}/ctl_mboxlist
%{_cyrexecdir}/cvt_cyrusdb
%{_cyrexecdir}/cyr_dbtool
%{_cyrexecdir}/cyr_expire
%{_cyrexecdir}/cyr_sequence
%{_cyrexecdir}/cyr_synclog
%{_cyrexecdir}/cyr_userseen
%{_cyrexecdir}/cyrdump
%{_cyrexecdir}/cyrus-master
%{_cyrexecdir}/deliver
%{_cyrexecdir}/dohash
%{_cyrexecdir}/fud
%{_cyrexecdir}/imapd
%{_cyrexecdir}/ipurge
%{_cyrexecdir}/lmtpd
%{_cyrexecdir}/lmtpproxyd
%{_cyrexecdir}/masssievec
%{_cyrexecdir}/mbexamine
%{_cyrexecdir}/mbpath
%{_cyrexecdir}/migrate-metadata
%{_cyrexecdir}/mkimap
%{_cyrexecdir}/mknewsgroups
%{_cyrexecdir}/notifyd
%{_cyrexecdir}/pop3d
%{_cyrexecdir}/quota
%{_cyrexecdir}/reconstruct
%{_cyrexecdir}/rehash
%{_cyrexecdir}/sievec
%{_cyrexecdir}/sieved
%{_cyrexecdir}/smmapd
%{_cyrexecdir}/squatter
%{_cyrexecdir}/timsieved
%{_cyrexecdir}/tls_prune
%{_cyrexecdir}/translatesieve
%{_cyrexecdir}/undohash
%{_cyrexecdir}/unexpunge
%{_cyrexecdir}/upgradesieve
%{_cyrexecdir}/cvt_cyrusdb_all
%{_cyrexecdir}/idled
%{_cyrexecdir}/mupdate
%{_cyrexecdir}/mupdate-loadgen.pl
%{_cyrexecdir}/proxyd
%{_cyrexecdir}/sync_client
%{_cyrexecdir}/sync_reset
%{_cyrexecdir}/sync_server
%{_cyrexecdir}/cyrfetchnews
%{_cyrexecdir}/nntpd
%{_cyrexecdir}/ptdump
%{_cyrexecdir}/ptexpire
%{_cyrexecdir}/ptloader
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/backup
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/db
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/log
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/meta
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/md5
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/msg
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %{_var}/lib/imap/proc
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %{_var}/lib/imap/ptclient
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/quota
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/rpm
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/sieve
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %{_var}/lib/imap/socket
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/sync
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/lib/imap/user
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{_var}/spool/imap
%dir %{_sysconfdir}/pki/%{name}
%attr(0640,root,%{_cyrusgroup}) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssl_pem_file}
#%dir %{perl_vendorarch}
#%dir %{perl_vendorarch}/auto/Cyrus
##########################
#%{_bindir}/*
#%{_libdir}/perl5/5.16.3/i686-linux/perllocal.pod
#%{_libdir}/perl5/site_perl/5.16.3/*
#%{_includedir}/*
#%{_datadir}/licenses/%{name}/LICENSE
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
#%ghost /var/log/auth.log
#%ghost /var/log/imapd.log
#%dir %attr(750,cyrus,mail)	/var/imap
#%dir %attr(750,cyrus,mail)	/var/spool/imap
%changelog
*	Mon Jun 10 2013 baho-utot <baho-utot@columbus.rr.com> 2.4.17-1
-	Initial build.	First version
