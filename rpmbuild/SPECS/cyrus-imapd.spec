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
	--with-cyrus-prefix=%{_bindir}/%{name} \
	--with-sasl \
	--with-perl \
	--with-auth=unix \
	--with-openssl \
	--without-ucdsnmp
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/etc
cp ./master/conf/normal.conf %{buildroot}/etc/cyrus.conf
find %{buildroot}/%{_libdir} -name '*.a'  -delete
install -D -m644 COPYRIGHT %{buildroot}/usr/share/licenses/%{name}/LICENSE
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
%{_bindir}/*
%{_libdir}/perl5/5.16.3/i686-linux/perllocal.pod
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
