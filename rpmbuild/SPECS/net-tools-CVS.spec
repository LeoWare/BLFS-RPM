Summary:	Collection of programs for controlling the network system.
Name:		net-tools-CVS
Version:	20101030
Release:	1
License:	GPLv2
URL:		http://anduin.linuxfromscratch.org/sources/BLFS/svn/n
Group:		BLFS/Networking
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}_%{version}.tar.gz
%description
The Net-tools package is a collection of programs for controlling
the network subsystem of the Linux kernel.
%prep
%setup -q -n %{name}_%{version}
%build
sed -i -e '/Token/s/y$/n/'        config.in
sed -i -e '/HAVE_HWSTRIP/s/y$/n/' config.in
yes "" | make config
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make BASEDIR=%{buildroot} update
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/bin/*
/sbin/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%changelog
*	Wed May 22 2013 baho-utot <baho-utot@columbus.rr.com> 20101030-1
-	Initial build.	First version