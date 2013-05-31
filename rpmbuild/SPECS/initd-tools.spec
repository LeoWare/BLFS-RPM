Summary:	Programs to install and remove initd bootscripts
Name:		initd-tools
Version:	0.1.3
Release:	1
License:	GPLv2
URL:		http://people.freedesktop.org/~dbn/initd-tools
Group:		BLFS/SystemUtilities
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	http://people.freedesktop.org/~dbn/initd-tools/releases/%{name}-%{version}.tar.gz
%description
The initd-tools package contains programs to install and remove
LSB based bootscripts.
%prep
%setup -q
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/lsb/*
%{_mandir}/man8/*
%changelog
*	Wed May 22 2013 baho-utot <baho-utot@columbus.rr.com> 0.1.3-1
-	Initial build.	First version