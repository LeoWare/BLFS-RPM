Summary:	Firmware cutter
Name:		b43-fwcutter
Version:	017
Release:	1
License:	CUSTOM
URL:		http://linuxwireless.org
Group:		Network/Wireless
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	http://bues.ch/b43/fwcutter/%{name}-%{version}.tar.bz2
%description
A firmware cutter for broadcomm wireless devices
%prep
%setup -q
%build
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
install -D -m755 b43-fwcutter	%{buildroot}/usr/bin/b43-fwcutter
install -D -m644 b43-fwcutter.1	%{buildroot}/usr/share/man/man1/b43-fwcutter.1
%{_fixperms} %{buildroot}/*
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/b43-fwcutter
%{_mandir}/man1/b43-fwcutter.1.gz
%changelog
*	Tue May 21 2013 baho-utot <baho-utot@columbus.rr.com> 017-1
-	Initial build.	First version