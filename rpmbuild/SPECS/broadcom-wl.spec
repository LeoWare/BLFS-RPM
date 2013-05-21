Summary:	Firmware for broadcomm wireless devices
Name:		broadcom-wl
Version:	5.100.138
Release:	1
License:	Unknown
URL:		http://linuxwireless.org
Group:		Network/Wireless
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}-%{version}.tar.bz2
%description
Firmware for broadcomm b43 kernel drivers
%prep
%setup -q
#-n %{name}-%{version}
%build
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
FWDIR=%{buildroot}/lib/firmware
install -vdm 755 ${FWDIR}
b43-fwcutter -w ${FWDIR} linux/wl_apsta.o
%{_fixperms} %{buildroot}/*
%check
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/%{_lib}/firmware/b43/*
%changelog
*	Tue May 21 2013 baho-utot <baho-utot@columbus.rr.com> 5.100.138-1
-	Initial build.	First version