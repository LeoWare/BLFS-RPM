Summary:	Supplies a random number generator
Name:		random.number.generator
Version:	20130519
Release:	1
License:	GPLv2
URL:		http://www.linuxfromscratch.org
Group:		BLFS/AfterLFS
Vendor:		Bildanet
Distribution:	Octothorpe
BuildArch:	noarch
Source0:	http://www.linuxfromscratch.org/blfs/downloads/svn/blfs-bootscripts-20130512.tar.bz2
%description
The Linux kernel supplies a random number generator which is accessed
through /dev/random and /dev/urandom. Programs that utilize the 
random and urandom devices, such as OpenSSH, will benefit from these
instructions.
%prep
%setup -q -n blfs-bootscripts-20130512
%build
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install-random
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%clean
rm -rf %{buildroot}
%files
%defattr(-,root,root)
#
/etc/rc.d/init.d/random
/etc/rc.d/rc0.d/K45random
/etc/rc.d/rc1.d/S25random
/etc/rc.d/rc2.d/S25random
/etc/rc.d/rc3.d/S25random
/etc/rc.d/rc4.d/S25random
/etc/rc.d/rc5.d/S25random
/etc/rc.d/rc6.d/K45random
%changelog
*	Sun May 19 2013 baho-utot <baho-utot@columbus.rr.com> 20130519-1
-	Initial build.	First version