Summary:	A portable, high level programming interface to various calling conventions
Name:		libffi
Version:	3.0.13
Release:	1
License:	MIT
URL:		http://sourceware.org/libffi/
Group:		BLFS/GeneralLibraries
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	ftp://sourceware.org/pub/libffi/%{name}-%{version}.tar.gz
Patch0:		http://www.linuxfromscratch.org/patches/blfs/svn/libffi-3.0.13-includedir-1.patch
%description
The libffi library provides a portable, high level programming interface
to various calling conventions. This allows a programmer to call any 
function specified by a call interface description at run time.
%prep
%setup -q
%patch0 -p1
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datarootdir}/licenses/libffi/LICENSE
%{_mandir}/man3/*
%changelog
*	Wed May 29 2013 baho-utot <baho-utot@columbus.rr.com> 3.0.13-1
-	Initial build.	First version