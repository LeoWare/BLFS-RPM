Summary:	A file transfer program to keep remote files in sync
Name:		rsync
Version:	3.0.9
Release:	1
License:	GPLv3
URL:		http://samba.anu.edu.au/rsync/
Group:		BLFS/NetworkingPrograms
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}-%{version}.tar.gz
%description
The rsync package contains the rsync utility. This is useful for 
synchronizing large file archives over a network.
%prep
%setup -q
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir}
#	--with-included-popt
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
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%changelog
*	Thu May 23 2013 baho-utot <baho-utot@columbus.rr.com> 3.0.9-1
-	Initial build.	First version
