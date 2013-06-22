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
%define	_cyrususer	cyrus
%define	_cyrusgroup	mail
%define	_sysconfdir	/etc
%define	maildir		%{_var}/spool/imap
%define	workdir		%{_var}/lib/imap
%define	sievedir	%{_var}/lib/sieve
%define	perldir		/usr/lib/perl5
%define cyrusbindir	/usr/cyrus/bin
%define	cyrusdir	/usr/cyrus
#%define ssl_pem_file %{_sysconfdir}/pki/%{name}/%{name}.pem
#%define _cyrexecdir %{_exec_prefix}/lib/%{name}
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
%build
export CPPFLAGS="%{optflags} -fno-strict-aliasing"
export CFLAGS="%{optflags} -fPIC -fno-strict-aliasing"
export CCDLFLAGS="-rdynamic"
export LDFLAGS="-Wl,-z,now -Wl,-z,relro"
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--with-sasl \
	--with-perl \
	--with-openssl \
	--without-ucdsnmp \
	--without-snmp
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} mandir=%{_mandir}
# Install tools
install -vdm755 %{buildroot}/%{cyrusdir}/tools
for tool in tools/* ; do
	test -f ${tool} && install -m 755 ${tool} %{buildroot}%{cyrusdir}/tools
done
# Create directories
install -vdm 755 \
	%{buildroot}%{workdir}/{backup,db,log,md5,meta,msg,proc,ptclient,quota,sieve,socket,sync,user} \
	%{buildroot}%{maildir}/{stage.,sync.} \
	%{buildroot}%{cyrusdir}/tools
# Install additional files
install -D -p -m 644 master/conf/normal.conf %{buildroot}%{_sysconfdir}/cyrus.conf
cat >> %{buildroot}%{_sysconfdir}/imapd.conf << "EOF"
admins:			cyrus
configdirectory:	%{workdir}
partition-default:	%{maildir}
sasl_pwcheck_method:	auxprop
sasl_auxprop_plugin:	sasldb	
EOF
# Install templates
install -vdm 755 			%{buildroot}/%{_sysconfdir}/cyrus-imapd
install -m 644 master/conf/*.conf	%{buildroot}/%{_sysconfdir}/cyrus-imapd
# Rename 'master' binary and manpage to avoid clash with postfix
mv -f %{buildroot}%{cyrusbindir}/master         %{buildroot}%{cyrusbindir}/cyrus-master
mv -f %{buildroot}%{_mandir}/man8/master.8      %{buildroot}%{_mandir}/man8/cyrus-master.8
# Remove installed but not packaged files
rm -f %{buildroot}%{cyrusdir}/tools/not-mkdep
rm -f %{buildroot}%{cyrusdir}/tools/config2header*
rm -f %{buildroot}%{cyrusdir}/tools/config2man
rm -f %{buildroot}%{cyrusbindir}/pop3proxyd
#	daemonize!
install -vdm 755 %{buildroot}/etc/rc.d/{,rc{0,1,2,3,4,5,6}.d,init.d}
cat >> %{buildroot}/etc/rc.d/init.d/imapd << "EOF"
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
		start_daemon /usr/cyrus/bin/cyrus-master & > /dev/null 2>&1 
		evaluate_retval
		;;
	stop)
		log_info_msg "Stopping Cyrus Imap..."
		killproc /usr/cyrus/bin/cyrus-master
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
install -D -m644 COPYRIGHT %{buildroot}/usr/share/licenses/%{name}/LICENSE
#	Kill files not packaged
find %{buildroot}/%{_libdir}	-name '*.a'		-delete
find %{buildroot}%{perldir}	-name '*.bs'		-delete
find %{buildroot}%{perldir}	-name '.packlist'	-delete
find %{buildroot}%{perldir}	-name 'perllocal.pod'	-delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%pre
# Create 'cyrus' user on target host
getent group saslauth >/dev/null || /usr/sbin/groupadd -g 76 -r saslauth 
getent passwd cyrus >/dev/null || /usr/sbin/useradd -c "Cyrus IMAP Server" -d %{_var}/lib/imap -g mail -G saslauth -s /sbin/nologin -u 76 -r cyrus
%post
/sbin/ldconfig
#cat >> /etc/syslog.conf <<- "EOF"
#	Addition for cyrus-impad
#local6.debug  /var/log/imapd.log
#auth.debug /var/log/auth.log
#	End cyrus-imapd
#EOF
#touch /var/log/auth.log
#touch /var/log/imapd.log
/etc/rc.d/init/sysklogd restart
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root,-)
#	configuration templates
%{_sysconfdir}/cyrus-imapd/cmu-backend.conf
%{_sysconfdir}/cyrus-imapd/cmu-frontend.conf
%{_sysconfdir}/cyrus-imapd/normal.conf
%{_sysconfdir}/cyrus-imapd/prefork.conf
%{_sysconfdir}/cyrus-imapd/small.conf
%config(noreplace) %{_sysconfdir}/cyrus.conf
%config(noreplace) %{_sysconfdir}/imapd.conf
#%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}.conf
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/imapd
%{_sysconfdir}/rc.d/rc0.d/K50imapd
%{_sysconfdir}/rc.d/rc1.d/K50imapd
%{_sysconfdir}/rc.d/rc2.d/S35imapd
%{_sysconfdir}/rc.d/rc3.d/S35imapd
%{_sysconfdir}/rc.d/rc4.d/S35imapd
%{_sysconfdir}/rc.d/rc5.d/S35imapd
%{_sysconfdir}/rc.d/rc6.d/K50imapd
%dir %{cyrusbindir}
%{cyrusbindir}/arbitron
%{cyrusbindir}/chk_cyrus
%{cyrusbindir}/cyr_df
%{cyrusbindir}/ctl_cyrusdb
%{cyrusbindir}/ctl_deliver
%{cyrusbindir}/ctl_mboxlist
%{cyrusbindir}/cvt_cyrusdb
%{cyrusbindir}/cyr_dbtool
%{cyrusbindir}/cyr_expire
%{cyrusbindir}/cyr_sequence
%{cyrusbindir}/cyr_synclog
%{cyrusbindir}/cyr_userseen
%{cyrusbindir}/cyrdump
%{cyrusbindir}/cyrus-master
%{cyrusbindir}/deliver
%{cyrusbindir}/fud
%{cyrusbindir}/imapd
%{cyrusbindir}/ipurge
%{cyrusbindir}/lmtpd
%{cyrusbindir}/lmtpproxyd
%{cyrusbindir}/mbexamine
%{cyrusbindir}/mbpath
%{cyrusbindir}/notifyd
%{cyrusbindir}/pop3d
#%{cyrusbindir}/pop3proxyd
%{cyrusbindir}/proxyd
%{cyrusbindir}/quota
%{cyrusbindir}/reconstruct
%{cyrusbindir}/sievec
%{cyrusbindir}/sieved
%{cyrusbindir}/smmapd
%{cyrusbindir}/squatter
%{cyrusbindir}/timsieved
%{cyrusbindir}/tls_prune
%{cyrusbindir}/unexpunge
#	tools
%dir %{cyrusdir}/tools
%{cyrusdir}/tools/arbitronsort.pl
#%{cyrusdir}/tools/config2header
#%{cyrusdir}/tools/config2man
%{cyrusdir}/tools/convert-sieve.pl
%{cyrusdir}/tools/dohash
%{cyrusdir}/tools/masssievec
%{cyrusdir}/tools/migrate-metadata
%{cyrusdir}/tools/mkimap
%{cyrusdir}/tools/mknewsgroups
%{cyrusdir}/tools/mupdate-loadgen.pl
#%{cyrusdir}/tools/not-mkdep
%{cyrusdir}/tools/rehash
%{cyrusdir}/tools/translatesieve
%{cyrusdir}/tools/undohash
%{cyrusdir}/tools/upgradesieve
#	end tools
%{_bindir}/cyradm
%{_bindir}/imtest
%{_bindir}/installsieve
%{_bindir}/lmtptest
%{_bindir}/mupdatetest
%{_bindir}/nntptest
%{_bindir}/pop3test
%{_bindir}/sivtest
%{_bindir}/sieveshell
%{_bindir}/smtptest
%{_bindir}/synctest
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{maildir}
#%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{maildir}/stage.
#%attr(0750,%{_cyrususer}.%{_cyrusgroup}) %dir %{maildir}/sync.
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/backup
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/db
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/log
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/meta
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/md5
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/msg
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/proc
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/ptclient
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/quota
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/sieve
%attr(0750,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/socket
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/sync
%attr(0700,%{_cyrususer},%{_cyrusgroup}) %dir %{workdir}/user
%dir %{_includedir}/cyrus
%{_includedir}/cyrus/*
%{perldir}/*
%{_datadir}/licenses/%{name}/LICENSE
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%changelog
*	Mon Jun 10 2013 baho-utot <baho-utot@columbus.rr.com> 2.4.17-1
-	Initial build.	First version
