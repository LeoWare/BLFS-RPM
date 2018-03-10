#	https://github.com/apple/cups/releases/download/v2.2.4/cups-2.2.4-source.tar.gz
Summary:	The Common Unix Printing System (CUPS) is a print spooler and associated utilities
Name:		cups
Version:	2.2.4
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires(pre): /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Source0:	%{name}-%{version}-source.tar.gz
Source1:	http://anduin.linuxfromscratch.org/BLFS/blfs-bootscripts/blfs-bootscripts-20170731.tar.xz
%description
	The Common Unix Printing System (CUPS) is a print spooler and associated utilities.
	It is based on the "Internet Printing Protocol" and provides printing services to
	most PostScript and raster printers. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%setup -q -T -D -a 1 -n %{name}-%{version}
%build
	sed -i 's#@CUPS_HTMLVIEW@#firefox#' desktop/cups.desktop.in
	sed -i '2062,2069d' cups/dest.c
	sed -i 's:444:644:' Makedefs.in
	sed -i '/MAN.EXT/s:.gz::' configure config-scripts/cups-manpages.m4
	sed -i '/LIBGCRYPTCONFIG/d' config-scripts/cups-ssl.m4
	aclocal  -I config-scripts
	autoconf -I config-scripts
	CC=gcc \
		./configure \
			--libdir=/usr/lib \
			--disable-systemd \
			--with-rcdir=/tmp/cupsinit \
			--with-system-groups=lpadmin \
			--with-docdir=%{_datarootdir}/%{name}/doc-%{version}
	make %{?_smp_mflags}
%install
	make BUILDROOT=$RPM_BUILD_ROOT install
	rm -rf %{buildroot}/tmp/cupsinit
	install -vdm 755 %{buildroot}%{_datarootdir}/doc
	ln -svnf ../cups/doc-2.2.4 %{buildroot}%{_datarootdir}/doc/cups-2.2.4
	install -vdm 755 %{buildroot}%{_sysconfdir}/cups
	echo "ServerName /var/run/cups/cups.sock" > %{buildroot}%{_sysconfdir}/cups/client.conf
	#
	#	Boot scripts
	#	
	cd ${RPM_BUILD_DIR}/${RPM_PACKAGE_NAME}-${RPM_PACKAGE_VERSION}/blfs-bootscripts-20170731
	make DESTDIR=%{buildroot} install-cups
	cd ${RPM_BUILD_DIR}/${RPM_PACKAGE_NAME}-${RPM_PACKAGE_VERSION}
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	#	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	#	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%pre
	/usr/bin/getent group  lpadmin	|| groupadd -g 19 lpadmin
	/usr/bin/getent passwd lp	|| useradd -c "Print Service User" -d /var/spool/cups -g lp -s /bin/false -u 9 lp
%post
	/sbin/ldconfig
	#	gtk-update-icon-cache needs GTK+-2.24.31 or GTK+-3.22.18
%postun	
	/sbin/ldconfig
	/usr/sbin/userdel
%files
	%defattr(-,root,root,-)
	%{_sysconfdir}/cups
	%{_sysconfdir}/dbus-1/system.d/cups.conf
	%{_sysconfdir}/rc.d/init.d/cups
	%{_sysconfdir}/rc.d/rc0.d/K00cups
	%{_sysconfdir}/rc.d/rc1.d/K00cups
	%{_sysconfdir}/rc.d/rc2.d/S25cups
	%{_sysconfdir}/rc.d/rc3.d/S25cups
	%{_sysconfdir}/rc.d/rc4.d/S25cups
	%{_sysconfdir}/rc.d/rc5.d/S25cups
	%{_sysconfdir}/rc.d/rc6.d/K00cups
	%{_bindir}/cancel
	%{_bindir}/cups-config
	%{_bindir}/cupstestdsc
	%{_bindir}/cupstestppd
	%{_bindir}/ipptool
	%{_bindir}/lp
	%{_bindir}/lpoptions
	%{_bindir}/lpq
	%{_bindir}/lpr
	%{_bindir}/lprm
	%{_bindir}/lpstat
	%{_bindir}/ppdc
	%{_bindir}/ppdhtml
	%{_bindir}/ppdi
	%{_bindir}/ppdmerge
	%{_bindir}/ppdpo
	%{_includedir}/cups
	%{_libdir}/libcups.so
	%{_libdir}/libcups.so.2
	%{_libdir}/libcupscgi.so
	%{_libdir}/libcupscgi.so.1
	%{_libdir}/libcupsimage.so
	%{_libdir}/libcupsimage.so.2
	%{_libdir}/libcupsmime.so
	%{_libdir}/libcupsmime.so.1
	%{_libdir}/libcupsppdc.so
	%{_libdir}/libcupsppdc.so.1
	%{_libdir}/cups
	%{_sbindir}/accept
	%{_sbindir}/cupsaccept
	%{_sbindir}/cupsaddsmb
	%{_sbindir}/cupsctl
	%{_sbindir}/cupsd
	%{_sbindir}/cupsdisable
	%{_sbindir}/cupsenable
	%{_sbindir}/cupsfilter
	%{_sbindir}/cupsreject
	%{_sbindir}/lpadmin
	%{_sbindir}/lpc
	%{_sbindir}/lpinfo
	%{_sbindir}/lpmove
	%{_sbindir}/reject
	%{_datarootdir}/applications/cups.desktop
	%{_datarootdir}/cups
	%{_datarootdir}/doc/cups-2.2.4
	%{_datarootdir}/icons/hicolor/128x128/apps/cups.png
	%{_datarootdir}/icons/hicolor/16x16/apps/cups.png
	%{_datarootdir}/icons/hicolor/32x32/apps/cups.png
	%{_datarootdir}/icons/hicolor/64x64/apps/cups.png
	%{_datarootdir}/locale/ca/cups_ca.po
	%{_datarootdir}/locale/cs/cups_cs.po
	%{_datarootdir}/locale/de/cups_de.po
	%{_datarootdir}/locale/es/cups_es.po
	%{_datarootdir}/locale/fr/cups_fr.po
	%{_datarootdir}/locale/it/cups_it.po
	%{_datarootdir}/locale/ja/cups_ja.po
	%{_datarootdir}/locale/pt_BR/cups_pt_BR.po
	%{_datarootdir}/locale/ru/cups_ru.po
	%{_datarootdir}/locale/zh_CN/cups_zh_CN.po
	%{_mandir}/man1/*.gz
	%{_mandir}/man5/*.gz
	%{_mandir}/man7/*.gz
	%{_mandir}/man8/*.gz
%changelog
*	Thu Mar 01 2018 baho-utot <baho-utot@columbus.rr.com> 2.2.4-1
-	Initial build.	First version