Summary:	A high-performance mail server with IMAP, POP3, NNTP and SIEVE support
Name:		cyrus-imapd
Version:	2.4.17
Release:	1
License:	Custom
URL:		http://www.cyrusimap.org/
Group:		BLFS/MailServer
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	ftp://ftp.cyrusimap.org/cyrus-imapd/%{name}-%{version}.tar.gz
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
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--with-sasl \
	--with-perl \
	--with-auth=unix \
	--with-openssl \
	--without-ucdsnmp
#	--with-cryus-prefix=%{_bindir}/%{name}
make depend
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} mandir=%{_mandir}
make -C man install DESTDIR=%{buildroot} PREFIX=%{_prefix} mandir=%{_mandir}
install -vdm 755 %{buildroot}/etc
cp ./master/conf/normal.conf %{buildroot}/etc/cyrus.conf
install -D -m644 COPYRIGHT %{buildroot}/usr/share/licenses/%{name}/LICENSE
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
#	Kill files not packaged
find %{buildroot} -name "perllocal.pod" -exec rm -f {} \;
find %{buildroot} -name ".packlist" -exec rm -f {} \;
find %{buildroot}/%{_libdir} -name '*.a' -delete
rm %{buildroot}%{_mandir}/man8/master.8
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%config(noreplace) /etc/cyrus.conf
%attr(755,root,root) /etc/rc.d/init.d/imapd
/etc/rc.d/rc0.d/K50imapd
/etc/rc.d/rc1.d/K50imapd
/etc/rc.d/rc2.d/S35imapd
/etc/rc.d/rc3.d/S35imapd
/etc/rc.d/rc4.d/S35imapd
/etc/rc.d/rc5.d/S35imapd
/etc/rc.d/rc6.d/K50imapd
%dir /usr/cyrus/bin
/usr/cyrus/bin/*
%{_bindir}/*
#%{_libdir}/perl5/5.16.3/i686-linux/perllocal.pod
%{_libdir}/perl5/site_perl/5.16.3/*
%{_includedir}/*
%{_datadir}/licenses/%{name}/LICENSE
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%changelog
*	Mon Jun 10 2013 baho-utot <baho-utot@columbus.rr.com> 2.4.17-1
-	Initial build.	First version
