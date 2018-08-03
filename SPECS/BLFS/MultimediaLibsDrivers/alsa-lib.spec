#	ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.1.4.1.tar.bz2
Summary:	The ALSA Library package contains the ALSA library used by programs (including ALSA Utilities) requiring access to the ALSA sound interface
Name:		alsa-lib
Version:	1.1.4.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Multimedia
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.bz2
%description
	The Linux kernel now provides ALSA support by default. However, applications need to interface to that capability.
	The following six sections of the book deal with the separate components of ALSA: the libraries, the plugins,
	the utilities, the tools, the firmware and the OSS compatibility libraries. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
	%defattr(-,root,root)
	%{_bindir}/aserver
	%{_includedir}/alsa
	%{_includedir}/sys/asoundlib.h
	%{_libdir}/alsa-lib
	%{_libdir}/libasound.so
	%{_libdir}/libasound.so.2
	%{_libdir}/libasound.so.2.0.0
	%{_libdir}/pkgconfig/alsa.pc
	%{_datarootdir}/aclocal/alsa.m4
	%{_datarootdir}/alsa
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> 1.1.4.1-1
-	Initial build.	First version