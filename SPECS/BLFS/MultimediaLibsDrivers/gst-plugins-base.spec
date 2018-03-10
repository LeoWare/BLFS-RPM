#		https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-1.12.2.tar.xz
Summary:	The GStreamer Base Plug-ins is a well-groomed and well-maintained collection of GStreamer plug-ins and elements
Name:		gst-plugins-base
Version:	1.12.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.xz
%description
	The GStreamer Base Plug-ins is a well-groomed and well-maintained collection of GStreamer
	plug-ins and elements, spanning the range of possible types of elements one would want to
	write for GStreamer. You will need at least one of Good, Bad, Ugly or Libav plugins for
	GStreamer applications to function properly. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--with-package-name="GStreamer Base Plugins 1.12.2 BLFS" \
		--with-package-origin="http://www.linuxfromscratch.org/blfs/view/svn/"
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
	sed -i '/man1/d' filelist.rpm
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f filelist.rpm
	%defattr(-,root,root)
#	%%{buildroot}%%{_datarootdir}/licenses/%%{name}/LICENSE
	%{_mandir}/man1/*.gz
 
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.12.2-1
-	Initial build.	First version