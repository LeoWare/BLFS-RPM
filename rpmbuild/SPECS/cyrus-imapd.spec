Summary:	pop3/imap mail server
Name:		cyrus-imapd
Version:	2.4.17
Release:	1
License:	Custom
URL:		http://cyrusimap.web.cmu.edu
Group:		BLFS/MailServer
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	ftp://ftp.andrew.cmu.edu/pub/cyrus/%{name}-%{version}.tar.gz
%description
Cyrus Imap server
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
#make depend
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/etc
cp ./master/conf/normal.conf %{buildroot}/etc/cyrus.conf
find %{buildroot}/%{_libdir} -name '*.a'  -delete
install -D -m644 COPYRIGHT %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/var/imap
install -vdm 755 %{buildroot}/var/spool/imap
cat >> %{buildroot}/etc/imapd.conf <<- "EOF"
configdirectory:	/var/imap
partition-default:	/var/spool/imap
admins:			cryus
sasl_pwcheck_method:	saslauthd
EOF
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
find %{buildroot}/usr/lib -name 'perllocal.pod' -delete
rm %{buildroot}%{_mandir}/man8/master.8
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
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
%defattr(-,root,root)
%config(noreplace) /etc/cyrus.conf
%config(noreplace) /etc/imapd.conf
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
%ghost /var/log/auth.log
%ghost /var/log/imapd.log
%dir %attr(750,cyrus,mail)	/var/imap
%dir %attr(750,cyrus,mail)	/var/spool/imap
%changelog
*	Mon Jun 10 2013 baho-utot <baho-utot@columbus.rr.com> 2.4.17-1
-	Initial build.	First version
