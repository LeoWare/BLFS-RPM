# Notes:
#	requires vi
#	requires fcron user and group to be present
#	pid direcory wrong
#	fifo pidfile wrong
#	CFLAGS are not used
#

Summary:	Cron daemon
Name:		fcron
Version:	3.1.2
Release:	1
License:	GPLv2
URL:		http://fcron.free.fr
Group:		BLFS/SystemUtilities
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	http://fcron.free.fr/archives/%{name}-%{version}.src.tar.gz
Source1:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20130512.tar.bz2
%description
The Fcron package contains a periodical command scheduler which aims
at replacing Vixie Cron.
%prep
%setup -q -n %{name}-%{version}
tar xf %{SOURCE1}
%build
export CFLAGS="%{optflags}" 
export CXXFLAGS="%{optflags}" 
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--sysconfdir=/etc/fcron \
	--localstatedir=/var \
	--with-editor=/usr/bin/vim \
	--with-sendmail=no \
	--with-piddir=/run \
	--with-answer-all=no \
	--with-boot-install=no \
	--with-username=fcron \
	--with-groupname=fcron
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
install -vdm 755 %{buildroot}/usr/sbin
install -vdm 775 %{buildroot}/var/spool/fcron
make DESTDIR=%{buildroot} install-staged
#	Install daemon script
pushd blfs-bootscripts-20130512
make DESTDIR=%{buildroot} install-fcron
popd
#	Cleanup
rm -rf %{buildroot}/usr/share/man/fr
rm -rf %{buildroot}/usr/share/doc/%{name}-%{version}/fr
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post
/sbin/ldconfig
cat >> /etc/syslog.conf <<- "EOF"
# Begin fcron addition to /etc/syslog.conf
	cron.* -/var/log/cron.log
# End fcron addition
EOF
%pre
if ! getent group fcron >/dev/null; then
	groupadd -g 22 fcron
fi
if ! getent passwd fcron >/dev/null; then
	useradd -d /dev/null -c "Fcron User" -g fcron -s /bin/false -u 22 fcron
fi
%postun
/sbin/ldconfig
if getent passwd fcron >/dev/null; then
	userdel fcron
fi
if getent group fcron >/dev/null; then
	groupdel fcron
fi
#/etc/rc.d/init.d/sysklogd reload`
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root,-)
%dir %attr(770,fcron,fcron) /var/spool/fcron
%ghost /var/run/fcron.pid
%config(noreplace) %attr(644,root,fcron) /etc/fcron/fcron.allow
%config(noreplace) %attr(644,root,fcron) /etc/fcron/fcron.conf
%config(noreplace) %attr(644,root,fcron) /etc/fcron/fcron.deny
/etc/rc.d/init.d/fcron
/etc/rc.d/rc0.d/K08fcron
/etc/rc.d/rc1.d/K08fcron
/etc/rc.d/rc2.d/S40fcron
/etc/rc.d/rc3.d/S40fcron
/etc/rc.d/rc4.d/S40fcron
/etc/rc.d/rc5.d/S40fcron
/etc/rc.d/rc6.d/K08fcron
%{_bindir}/fcrondyn
%attr(04754,root,fcron) %{_bindir}/fcronsighup
%attr(06755,fcron,fcron) %{_bindir}/fcrontab
%{_sbindir}/*
%{_docdir}/%{name}-%{version}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%changelog
*	Wed May 22 2013 baho-utot <baho-utot@columbus.rr.com> 3.1.2-1
-	Initial build.	First version
