#		https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-1.12.2.tar.xz
Summary:	gstreamer is a streaming media framework that enables applications to share a common set of plugins for things like video encoding and decoding
Name:		gstreamer
Version:	1.12.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	glib, gobject-introspection
Source0:	%{name}-%{version}.tar.xz
%description
	gstreamer is a streaming media framework that enables applications to share a common set
	of plugins for things like video encoding and decoding, audio encoding and decoding, audio
	and video filters, audio visualisation, web streaming and anything else that streams in
	real-time or otherwise. This package only provides base functionality and libraries. You
	may need at least gst-plugins-base-1.12.2 and one of Good, Bad, Ugly or Libav plugins
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		 --with-package-name="GStreamer 1.12.2 BLFS" \
		--with-package-origin="http://www.linuxfromscratch.org/blfs/view/svn/"
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}/usr/share/locale" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f filelist.rpm
	%defattr(-,root,root)
#	%%{buildroot}%%{_datarootdir}/licenses/%%{name}/LICENSE
	%{_bindir}/gst-inspect-1.0
	%{_bindir}/gst-launch-1.0
	%{_bindir}/gst-stats-1.0
	%{_bindir}/gst-typefind-1.0
	%{_includedir}/gstreamer-1.0
	%{_libdir}/girepository-1.0
	%{_libdir}/gstreamer-1.0
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/pkgconfig/*.pc
	%{_libexecdir}/gstreamer-1.0
	%{_datarootdir}/aclocal/gst-element-check-1.0.m4
	%{_datarootdir}/bash-completion/completions/gst-inspect-1.0
	%{_datarootdir}/bash-completion/completions/gst-launch-1.0
	%{_datarootdir}/bash-completion/helpers/gst
	%{_datarootdir}/gir-1.0/*.gir
	%{_datarootdir}/gtk-doc/html/gstreamer-1.0
	%{_datarootdir}/gtk-doc/html/gstreamer-libs-1.0
	%{_datarootdir}/gtk-doc/html/gstreamer-plugins-1.0
	%{_mandir}/man1/*.gz
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.12.2-1
-	Initial build.	First version