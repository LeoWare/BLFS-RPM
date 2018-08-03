#	libpng-1.6.31.tar.xz
Summary:	The libpng package contains libraries used by other programs for reading and writing PNG files.
Name:		libpng
Version:	1.6.31
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.xz
Source1:	libpng-1.6.31-apng.patch.gz
%description
	The libpng package contains libraries used by other programs for reading and writing PNG files.
	The PNG format was designed as a replacement for GIF and, to a lesser extent, TIFF, with many
	improvements and extensions and lack of patent problems.

%prep
%setup -q -n %{NAME}-%{VERSION}
gzip -cd %{_sourcedir}/libpng-1.6.31-apng.patch.gz | patch -p0
%build

LIBS=-lpthread ./configure --prefix=%{_prefix} --disable-static 
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

%post
pushd /usr/share/info
rm -v dir
for f in *
	do install-info $f dir 2>/dev/null
done
popd

%files -f filelist.rpm
	%defattr(-,root,root)

%changelog
*	Thu Feb 15 2018 baho-utot <baho-utot@columbus.rr.com> libpng-1.6.31-1
-	Initial build.	First version