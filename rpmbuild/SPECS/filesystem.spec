Summary:	Default file system
Name:		filesystem
Version:	20130519
Release:	1
License:	GPLv3
Group:		BLFS/AfterLFS
Vendor:		Bildanet
URL:		http://www.linuxfromscratch.org
Distribution:	Octothorpe
BuildArch: noarch
%define		LIBDIR	"/lib"
%description
The filesystem package is one of the basic packages that is installed
on a Linux system. Filesystem contains the basic directory
layout for a Linux operating system, including the correct permissions
for the directories.
%prep
%build
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
#	Kernel required directories
install -vdm 755 %{buildroot}/{dev,proc,sys}
#	Begin
install -vdm 755 %{buildroot}/{bin,boot,etc/{opt,profile.d,skel,sysconfig},home,lib,mnt,opt,run}
install -vdm 755 %{buildroot}/{media/{floppy,cdrom},sbin,srv,var}
install -vdm 0750 %{buildroot}/root
install -vdm 1777 %{buildroot}/tmp %{buildroot}/var/tmp
install -vdm 755 %{buildroot}/usr/{,local/}{bin,include,lib,sbin,src}
install -vdm 755 %{buildroot}/usr/{,local/}share/{doc,info,locale,man}
install -vdm 755 %{buildroot}/usr/{,local/}share/{misc,terminfo,zoneinfo}
install -vdm 755 %{buildroot}/usr/{,local/}share/man/man{1..8}
install -vdm 755 %{buildroot}/var/{log,mail,spool}
install -vdm 755 %{buildroot}/var/{opt,cache,lib/{misc,locate},local}
install -vdm 755 %{buildroot}/%{_libdir}/locale
#	End
%ifarch x86_64
ln -sv lib %{buildroot}/lib64
ln -sv lib %{buildroot}/usr/lib64
%endif
#	Symlinks
install -vdm 755 %{buildroot}/run/lock
ln -sv /run %{buildroot}/var/run
ln -sv /run/lock %{buildroot}/var/lock
ln -sv /proc/self/mounts %{buildroot}/etc/mtab
#	install configuration files
touch %{buildroot}/etc/mtab
touch %{buildroot}/var/log/{btmp,lastlog,wtmp}
#	Configuration files
cat > %{buildroot}/etc/passwd <<- "EOF"
	root::0:0:root:/root:/bin/bash
	bin:x:1:1:bin:/dev/null:/bin/false
	nobody:x:99:99:Unprivileged User:/dev/null:/bin/false
EOF
cat > %{buildroot}/etc/group <<- "EOF"
	root:x:0:
	bin:x:1:
	sys:x:2:
	kmem:x:3:
	tape:x:4:
	tty:x:5:
	daemon:x:6:
	floppy:x:7:
	disk:x:8:
	lp:x:9:
	dialout:x:10:
	audio:x:11:
	video:x:12:
	utmp:x:13:
	usb:x:14:
	cdrom:x:15:
	mail:x:34:
	nogroup:x:99:
EOF
touch %{buildroot}/etc/mtab
cat > %{buildroot}/etc/sysconfig/ifconfig.eth0 <<- "EOF"
	ONBOOT=no
	IFACE=eth0
	SERVICE=ipv4-static
	IP=192.168.1.2
	GATEWAY=192.168.1.1
	PREFIX=24
	BROADCAST=192.168.1.255
EOF
cat > %{buildroot}/etc/resolv.conf <<- "EOF"
#	Begin /etc/resolv.conf
#	domain <Your Domain Name>
#	nameserver <IP address>
#	End /etc/resolv.conf
EOF
cat > %{buildroot}/etc/hosts <<- "EOF"
#	Begin /etc/hosts (network card version)
	127.0.0.1 localhost
#<192.168.1.1> <HOSTNAME.example.org> [alias1] [alias2 ...]
#	End /etc/hosts (network card version)
EOF
cat > %{buildroot}/etc/inittab <<- "EOF"
#	Begin /etc/inittab
	id:3:initdefault:
	si::sysinit:/etc/rc.d/init.d/rc S
	l0:0:wait:/etc/rc.d/init.d/rc 0
	l1:S1:wait:/etc/rc.d/init.d/rc 1
	l2:2:wait:/etc/rc.d/init.d/rc 2
	l3:3:wait:/etc/rc.d/init.d/rc 3
	l4:4:wait:/etc/rc.d/init.d/rc 4
	l5:5:wait:/etc/rc.d/init.d/rc 5
	l6:6:wait:/etc/rc.d/init.d/rc 6
	ca:12345:ctrlaltdel:/sbin/shutdown -t1 -a -r now
	su:S016:once:/sbin/sulogin
	1:2345:respawn:/sbin/agetty --noclear tty1 9600
	2:2345:respawn:/sbin/agetty tty2 9600
	3:2345:respawn:/sbin/agetty tty3 9600
	4:2345:respawn:/sbin/agetty tty4 9600
	5:2345:respawn:/sbin/agetty tty5 9600
	6:2345:respawn:/sbin/agetty tty6 9600
#	End /etc/inittab
EOF
echo "HOSTNAME=lfs" > %{buildroot}/etc/sysconfig/network
cat > %{buildroot}/etc/sysconfig/clock <<- "EOF"
#	Begin /etc/sysconfig/clock
	UTC=1
#	Set this to any options you might need to give to hwclock,
#	such as machine hardware clock type for Alphas.
	CLOCKPARAMS=
#	End /etc/sysconfig/clock
EOF
cat > %{buildroot}/etc/sysconfig/console <<- "EOF"
#	Begin /etc/sysconfig/console
#	KEYMAP="us"
#	FONT="lat1-16 -m utf8"
#	FONT="lat1-16 -m 8859-1"
#	KEYMAP_CORRECTIONS="euro2"
#	UNICODE="1"
#	LEGACY_CHARSET="iso-8859-1"
# End /etc/sysconfig/console
EOF
cat > %{buildroot}/etc/inputrc <<- "EOF"
#	Begin /etc/inputrc
#	Modified by Chris Lynn <roryo@roryo.dynup.net>
#	Allow the command prompt to wrap to the next line
	set horizontal-scroll-mode Off
#	Enable 8bit input
	set meta-flag On
	set input-meta On
#	Turns off 8th bit stripping
	set convert-meta Off
#	Keep the 8th bit for display
	set output-meta On
#	none, visible or audible
	set bell-style none
#	All of the following map the escape sequence of the value
#	contained in the 1st argument to the readline specific functions
	"\eOd": backward-word
	"\eOc": forward-word
#	for linux console
	"\e[1~": beginning-of-line
	"\e[4~": end-of-line
	"\e[5~": beginning-of-history
	"\e[6~": end-of-history
	"\e[3~": delete-char
	"\e[2~": quoted-insert
#	for xterm
	"\eOH": beginning-of-line
	"\eOF": end-of-line
#	for Konsole
	"\e[H": beginning-of-line
	"\e[F": end-of-line
#	End /etc/inputrc
EOF
cat > %{buildroot}/etc/fstab <<- "EOF"
#	Begin /etc/fstab
#	hdparm -I /dev/sda | grep NCQ --> can use barrier
#system		mnt-pt		type		options			dump fsck
#/dev/sdax	/		/ext3	defaults,barrier,noatime,noacl,data=ordered 1 1
/dev/sdxx	/		ext3		defaults		1 1
/dev/sdxx	/boot		ext3		defaults		1 2
#/dev/sdax	swap		swap		pri=1			0 0
proc		/proc		proc		nosuid,noexec,nodev	0 0
sysfs		/sys		sysfs		nosuid,noexec,nodev	0 0
devpts		/dev/pts	devpts		gid=5,mode=620		0 0
tmpfs		/run		tmpfs		defaults		0 0
devtmpfs	/dev		devtmpfs	mode=0755,nosuid	0 0
#	mount points
tmpfs		/tmp		tmpfs		defaults		0 0
#	End /etc/fstab
EOF
echo %{version} > %{buildroot}/etc/lfs-release
cat > %{buildroot}/etc/lsb-release <<- "EOF"
	DISTRIB_ID="Linux From Scratch"
	DISTRIB_RELEASE=%{version}
	DISTRIB_CODENAME="<your name here>"
	DISTRIB_DESCRIPTION="Linux From Scratch"
EOF
#
#	BLFS additions
#
cat > %{buildroot}/etc/profile <<- "EOF"
# Begin /etc/profile
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# modifications by Dagmar d'Surreal <rivyqntzne@pbzpnfg.arg>
#
# System wide environment variables and startup programs.
#
# System wide aliases and functions should go in /etc/bashrc.  Personal
# environment variables and startup programs should go into
# ~/.bash_profile.  Personal aliases and functions should go into
# ~/.bashrc.

# Functions to help us manage paths.  Second argument is the name of the
# path variable to be modified (default: PATH)
pathremove () {
        local IFS=':'
        local NEWPATH
        local DIR
        local PATHVARIABLE=${2:-PATH}
        for DIR in ${!PATHVARIABLE} ; do
                if [ "$DIR" != "$1" ] ; then
                  NEWPATH=${NEWPATH:+$NEWPATH:}$DIR
                fi
        done
        export $PATHVARIABLE="$NEWPATH"
}
pathprepend () {
        pathremove $1 $2
        local PATHVARIABLE=${2:-PATH}
        export $PATHVARIABLE="$1${!PATHVARIABLE:+:${!PATHVARIABLE}}"
}
pathappend () {
        pathremove $1 $2
        local PATHVARIABLE=${2:-PATH}
        export $PATHVARIABLE="${!PATHVARIABLE:+${!PATHVARIABLE}:}$1"
}
# Set the initial path
export PATH=/bin:/usr/bin
if [ $EUID -eq 0 ] ; then
        pathappend /sbin:/usr/sbin
        unset HISTFILE
fi
# Setup some environment variables.
export HISTSIZE=1000
export HISTIGNORE="&:[bf]g:exit"
# Setup a red prompt for root and a green one for users.
NORMAL="\[\e[0m\]"
RED="\[\e[1;31m\]"
GREEN="\[\e[1;32m\]"
if [[ $EUID == 0 ]] ; then
  PS1="$RED\u [ $NORMAL\w$RED ]# $NORMAL"
else
  PS1="$GREEN\u [ $NORMAL\w$GREEN ]\$ $NORMAL"
fi
for script in /etc/profile.d/*.sh ; do
        if [ -r $script ] ; then
                . $script
        fi
done
# Now to clean up
unset pathremove pathprepend pathappend
# End /etc/profile
EOF

cat > %{buildroot}/etc/profile.d/dircolors.sh << "EOF"
# Setup for /bin/ls to support color, the alias is in /etc/bashrc.
if [ -f "/etc/dircolors" ] ; then
        eval $(dircolors -b /etc/dircolors)

        if [ -f "$HOME/.dircolors" ] ; then
                eval $(dircolors -b $HOME/.dircolors)
        fi
fi
alias ls='ls --color=auto'
EOF
cat > %{buildroot}/etc/profile.d/extrapaths.sh << "EOF"
if [ -d /usr/local/lib/pkgconfig ] ; then
        pathappend /usr/local/lib/pkgconfig PKG_CONFIG_PATH
fi
if [ -d /usr/local/bin ]; then
        pathprepend /usr/local/bin
fi
if [ -d /usr/local/sbin -a $EUID -eq 0 ]; then
        pathprepend /usr/local/sbin
fi

if [ -d ~/bin ]; then
        pathprepend ~/bin
fi
#if [ $EUID -gt 99 ]; then
#        pathappend .
#fi
EOF
cat > %{buildroot}/etc/profile.d/readline.sh << "EOF"
# Setup the INPUTRC environment variable.
if [ -z "$INPUTRC" -a ! -f "$HOME/.inputrc" ] ; then
        INPUTRC=/etc/inputrc
fi
export INPUTRC
EOF
cat > %{buildroot}/etc/profile.d/umask.sh << "EOF"
# By default, the umask should be set.
if [ "$(id -gn)" = "$(id -un)" -a $EUID -gt 99 ] ; then
  umask 002
else
  umask 022
fi
EOF
cat > %{buildroot}/etc/profile.d/i18n.sh << "EOF"
# Set up i18n variables
#	export LANG=<ll>_<CC>.<charmap><@modifiers>
EOF
cat > %{buildroot}/etc/bashrc << "EOF"
# Begin /etc/bashrc
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# updated by Bruce Dubbs <bdubbs@linuxfromscratch.org>
#
# System wide aliases and functions.
#
# System wide environment variables and startup programs should go into
# /etc/profile.  Personal environment variables and startup programs
# should go into ~/.bash_profile.  Personal aliases and functions should
# go into ~/.bashrc
#
# Provides a colored /bin/ls command.  Used in conjunction with code in
# /etc/profile.
alias ls='ls --color=auto'
# Provides prompt for non-login shells, specifically shells started
# in the X environment. [Review the LFS archive thread titled
# PS1 Environment Variable for a great case study behind this script
# addendum.]
NORMAL="\[\e[0m\]"
RED="\[\e[1;31m\]"
GREEN="\[\e[1;32m\]"
if [[ $EUID == 0 ]] ; then
  PS1="$RED\u [ $NORMAL\w$RED ]# $NORMAL"
else
  PS1="$GREEN\u [ $NORMAL\w$GREEN ]\$ $NORMAL"
fi
# End /etc/bashrc
EOF
cat > %{buildroot}/etc/skel/.bash_profile << "EOF"
# Begin ~/.bash_profile
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# updated by Bruce Dubbs <bdubbs@linuxfromscratch.org>
# Personal environment variables and startup programs.
# Personal aliases and functions should go in ~/.bashrc.  System wide
# environment variables and startup programs are in /etc/profile.
# System wide aliases and functions are in /etc/bashrc.
append () {
  # First remove the directory
  local IFS=':'
  local NEWPATH
  for DIR in $PATH; do
     if [ "$DIR" != "$1" ]; then
       NEWPATH=${NEWPATH:+$NEWPATH:}$DIR
     fi
  done
  # Then append the directory
  export PATH=$NEWPATH:$1
}
if [ -f "$HOME/.bashrc" ] ; then
  source $HOME/.bashrc
fi
if [ -d "$HOME/bin" ] ; then
  append $HOME/bin
fi
unset append
# End ~/.bash_profile
EOF
cat > %{buildroot}/etc/skel/.bashrc << "EOF"
# Begin ~/.bashrc
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# Personal aliases and functions.
# Personal environment variables and startup programs should go in
# ~/.bash_profile.  System wide environment variables and startup
# programs are in /etc/profile.  System wide aliases and functions are
# in /etc/bashrc.
if [ -f "/etc/bashrc" ] ; then
  source /etc/bashrc
fi
# End ~/.bashrc
EOF
cat > %{buildroot}/etc/skel/.bash_logout <<- "EOF"
# Begin ~/.bash_logout
# Written for Beyond Linux From Scratch	
# by James Robertson <jameswrobertson@earthlink.net>
# Personal items to perform on logout.
# End ~/.bash_logout
EOF
cat > %{buildroot}/etc/skel/.vimrc <<- "EOF"
	" Begin .vimrc
	set columns=80
	set wrapmargin=8
	set ruler
	" End .vimrc
EOF
#	Clear screen at login
clear > %{buildroot}/etc/issue
#
cat > %{buildroot}/etc/shells <<- "EOF"
# Begin /etc/shells
/bin/sh
/bin/bash
# End /etc/shells
EOF
%files
%defattr(-,root,root)
%dir /
%dir /bin
%dir /boot
%dir /dev
%config(noreplace) /etc/fstab
%config(noreplace) /etc/group
%config(noreplace) /etc/hosts
%config(noreplace) /etc/inittab
%config(noreplace) /etc/inputrc
%config(noreplace) /etc/lfs-release
%config(noreplace) /etc/lsb-release
%config(noreplace) /etc/mtab
%config(noreplace) /etc/passwd
%config(noreplace) /etc/profile
%config(noreplace) /etc/resolv.conf
%config(noreplace) /etc/sysconfig/clock
%config(noreplace) /etc/sysconfig/console
%config(noreplace) /etc/sysconfig/ifconfig.eth0
%config(noreplace) /etc/sysconfig/network
%dir /home
%dir %{LIBDIR}
%dir /media
%dir /mnt
%dir /opt
%dir /proc
%dir /root
%dir /run
%dir /run/lock
%dir /sbin
%dir /srv
%dir /sys
%dir /tmp
%dir /usr
%dir %{_libdir}/locale
%dir /var/cache
%dir /var/lib
%dir /var/local
%dir /var/lock
%dir /var/mail
%dir /var/opt
%dir /var/run
%dir /var/spool
%dir /var/tmp
%ghost /var/log/wtmp
%ghost %attr(664,root,utmp)	/var/log/lastlog
%ghost %attr(600,-,-)		/var/log/btmp
%ifarch x86_64
%dir /lib64
%dir /usr/lib64
%endif
#	BLFS Additions
%config(noreplace) /etc/bashrc
%config(noreplace) /etc/issue
%config(noreplace) /etc/profile.d/dircolors.sh
%config(noreplace) /etc/profile.d/extrapaths.sh
%config(noreplace) /etc/profile.d/i18n.sh
%config(noreplace) /etc/profile.d/readline.sh
%config(noreplace) /etc/profile.d/umask.sh
%config(noreplace) /etc/shells
%config(noreplace) /etc/skel/.bash_logout
%config(noreplace) /etc/skel/.bash_profile
%config(noreplace) /etc/skel/.bashrc
%config(noreplace) /etc/skel/.vimrc
%clean
rm -rf %{buildroot}
%post
if [ -e /bin/mknod ]; then
	[ -e /dev/console ] || /bin/mknod -m 600 /dev/console c 5 1
	[ -e /dev/null ]    || /bin/mknod -m 666 /dev/null c 1 3
fi
%changelog
*	Sun May 19 2013 baho-utot <baho-utot@columbus.rr.com> 20130519-1
-	Initial version
