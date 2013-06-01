Summary:	The whois client
Name:		whois
Version:	5.0.25
Release:	1
License:	GPLv2
URL:		http://www.linux.it/~md/software/
Group:		BLFS/NetworkingUtilities
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	http://ftp.debian.org/debian/pool/main/w/whois/%{name}_%{version}.tar.xz
%description
Whois is a client-side application which queries the whois directory
service for information pertaining to a particular domain name.
%prep
%setup -q -n %{name}-%{version}
%build
make %{?_smp_mflags} prefix=/usr CFLAGS="%{optflags}"
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make prefix=/usr BASEDIR=%{buildroot} install-whois
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%changelog
*	Fri May 31 2013 baho-utot <baho-utot@columbus.rr.com> 5.0.25-1
-	Initial build.	First version