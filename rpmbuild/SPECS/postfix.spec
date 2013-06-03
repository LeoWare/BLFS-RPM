Summary:	Fast, easy to administer, secure mail server
Name:		postfix
Version:	2.10.0
Release:	1
License:	Custom
URL:		http://www.postfix.org/
Group:		BLFS/MailServer
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	ftp://ftp.porcupine.org/mirrors/postfix-release/official/%{name}-%{version}.tar.gz
Source1:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20130512.tar.bz2
%description
The Postfix package contains a Mail Transport Agent (MTA). This is 
useful for sending email to other users of your host machine. It can
also be configured to be a central mail server for your domain, a 
mail relay agent or simply a mail delivery agent to your local 
Internet Service Provider.
%prep
%setup -q
tar xf %{SOURCE1}
sed -i 's/.\x08//g' README_FILES/*
%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
make makefiles \
	CCARGS=' \
		-DNO_NIS \
		-DUSE_TLS -I/usr/include/openssl \
		-DUSE_SASL_AUTH -DUSE_CYRUS_SASL -I/usr/include/sasl' \
	AUXLIBS=' \
		-lssl \
		-lcrypto \
		-lsasl2'  \
	OPT="${CFLAGS} "
#	${LDFLAGS}
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
sh postfix-install -non-interactive \
	daemon_directory=%{_libdir}/postfix \
	manpage_directory=%{_mandir} \
	html_directory=%{_datadir}/doc/%{name}-%{version}/html \
	readme_directory=%{_datadir}/doc/%{name}-%{version}/readme \
	install_root="%{buildroot}"
install -vdm 755 %{buildroot}/var/mail
install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
#	daemonize
pushd blfs-bootscripts-20130512
make DESTDIR=%{buildroot} install-postfix
popd
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%pre
if ! getent group postfix >/dev/null; then
	groupadd -g 32 postfix
fi
if ! getent group postdrop >/dev/null; then
	groupadd -g 33 postdrop
fi
if ! getent passwd postfix >/dev/null; then
	useradd -c "Postfix Daemon User" -d /var/spool/postfix -g postfix -s /bin/false -u 32 postfix 
fi
%postun
/sbin/ldconfig
if getent passwd postfix >/dev/null; then
	userdel postfix
fi
if getent group postfix >/dev/null; then
	groupdel postfix
fi
if getent group postdrop >/dev/null; then
	groupdel postdrop
fi
%post
/sbin/ldconfig
chown -v postfix:postfix /var/mail	
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/etc/rc.d/init.d/postfix
/etc/rc.d/rc0.d/K25postfix
/etc/rc.d/rc1.d/K25postfix
/etc/rc.d/rc2.d/K25postfix
/etc/rc.d/rc3.d/S35postfix
/etc/rc.d/rc4.d/S35postfix
/etc/rc.d/rc5.d/S35postfix
/etc/rc.d/rc6.d/K25postfix
%config(noreplace) /etc/%{name}/*
%{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_sbindir}/*
%dir %{_datadir}/doc/%{name}-%{version}
%{_datadir}/doc/%{name}-%{version}/*
%{_datadir}/licenses/postfix/LICENSE
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%changelog
*	Mon Jun 03 2013 baho-utot <baho-utot@columbus.rr.com> 2.10.0-1
-	Initial build.	First version