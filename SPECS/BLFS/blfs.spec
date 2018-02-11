Summary:	After LFS Configuration Issues 
Name:		blfs
Version:	8.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Configure
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	 blfs-bootscripts-20170731
%description
	The intention of LFS is to provide a basic system which you can build upon.
	There are several things about tidying up the system which many people wonder
	about once they have done the base install. We hope to cover these issues in
	this chapter. 
%prep
%setup -q -n blfs-bootscripts-20170731
%build
	#
	#	/etc/profile
	#
	cat > %{buildroot}/etc/profile <<- "EOF"
		# Begin /etc/profile
		# Written for Beyond Linux From Scratch
		# by James Robertson <jameswrobertson@earthlink.net>
		# modifications by Dagmar d'Surreal <rivyqntzne@pbzpnfg.arg>

		# System wide environment variables and startup programs.

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
			xport $PATHVARIABLE="$NEWPATH"
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

		export -f pathremove pathprepend pathappend

		# Set the initial path
		export PATH=/bin:/usr/bin

		if [ $EUID -eq 0 ] ; then
			pathappend /sbin:/usr/sbin
			unset HISTFILE
		fi

		# Setup some environment variables.
		export HISTSIZE=1000
		export HISTIGNORE="&:[bf]g:exit"

		# Set some defaults for graphical systems
		export XDG_DATA_DIRS=/usr/share/
		export XDG_CONFIG_DIRS=/etc/xdg/
		export XDG_RUNTIME_DIR=/tmp/xdg-$USER

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

		unset script RED GREEN NORMAL

		# End /etc/profile
	EOF
	install --directory --mode=0755 --owner=root --group=root %{buildroot}/etc/profile.d
	#
	#	Bash completion
	#
	cat > %{buildroot}/etc/profile.d/bash_completion.sh <<- "EOF"
		# Begin /etc/profile.d/bash_completion.sh
		# Import bash completion scripts

		for script in /etc/bash_completion.d/*.sh ; do
			if [ -r $script ] ; then
				. $script
			fi
		done
		# End /etc/profile.d/bash_completion.sh
	EOF
	install --directory --mode=0755 --owner=root --group=root %{buildroot}/etc/bash_completion.d
	#
	#	Directory colours
	#
	cat > %{buildroot}/etc/profile.d/dircolors.sh <<- "EOF"
		# Setup for /bin/ls and /bin/grep to support color, the alias is in /etc/bashrc.
		#	run the following as root to use directory colours
		#	dircolors -p > /etc/dircolors
		if [ -f "/etc/dircolors" ] ; then
			eval $(dircolors -b /etc/dircolors)
		fi

		if [ -f "$HOME/.dircolors" ] ; then
			eval $(dircolors -b $HOME/.dircolors)
		fi

		alias ls='ls --color=auto'
		alias grep='grep --color=auto'
	EOF
	#
	#	Extra paths
	#
	cat > %{buildroot}/etc/profile.d/extrapaths.sh <<- "EOF"
		if [ -d /usr/local/lib/pkgconfig ] ; then
			pathappend /usr/local/lib/pkgconfig PKG_CONFIG_PATH
		fi
		if [ -d /usr/local/bin ]; then
			pathprepend /usr/local/bin
		fi
		if [ -d /usr/local/sbin -a $EUID -eq 0 ]; then
			pathprepend /usr/local/sbin
		fi

		# Set some defaults before other applications add to these paths.
		pathappend /usr/share/man  MANPATH
		pathappend /usr/share/info INFOPATH
	EOF
	#
	#	Readline
	#
	cat > %{buildroot}/etc/profile.d/readline.sh <<- "EOF"
		# Setup the INPUTRC environment variable.
		if [ -z "$INPUTRC" -a ! -f "$HOME/.inputrc" ] ; then
			INPUTRC=/etc/inputrc
		fi
		export INPUTRC
	EOF
	#
	#	umask
	#
	cat > %{buildroot}/etc/profile.d/umask.sh <<- "EOF"
		# By default, the umask should be set.
		if [ "$(id -gn)" = "$(id -un)" -a $EUID -gt 99 ] ; then
			umask 002
		else
			umask 022
		fi
	EOF
	#
	#	International
	#
	cat > %{buildroot}/etc/profile.d/i18n.sh <<- "EOF"
		# Set up i18n variables
		#	export LANG=<ll>_<CC>.<charmap><@modifiers>
	EOF
	#
	#	Bash
	#
	cat > %{buildroot}/etc/bashrc <<- "EOF"
		# Begin /etc/bashrc
		# Written for Beyond Linux From Scratch
		# by James Robertson <jameswrobertson@earthlink.net>
		# updated by Bruce Dubbs <bdubbs@linuxfromscratch.org>

		# System wide aliases and functions.

		# System wide environment variables and startup programs should go into
		# /etc/profile.  Personal environment variables and startup programs
		# should go into ~/.bash_profile.  Personal aliases and functions should
		# go into ~/.bashrc

		# Provides colored /bin/ls and /bin/grep commands.  Used in conjunction
		# with code in /etc/profile.

		alias ls='ls --color=auto'
		alias grep='grep --color=auto'

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

		unset RED GREEN NORMAL

		# End /etc/bashrc
	EOF
	#
	#	/etc/skel
	#
	install --directory --mode=0755 --owner=root --group=root %{buildroot}/etc/skel
	cat > %{buildroot}/etc/skel/.bash_profile <<- "EOF"
		# Begin ~/.bash_profile
		# Written for Beyond Linux From Scratch
		# by James Robertson <jameswrobertson@earthlink.net>
		# updated by Bruce Dubbs <bdubbs@linuxfromscratch.org>

		# Personal environment variables and startup programs.

		# Personal aliases and functions should go in ~/.bashrc.  System wide
		# environment variables and startup programs are in /etc/profile.
		# System wide aliases and functions are in /etc/bashrc.

		if [ -f "$HOME/.bashrc" ] ; then
			source $HOME/.bashrc
		fi

		if [ -d "$HOME/bin" ] ; then
			pathprepend $HOME/bin
		fi

		# Having . in the PATH is dangerous
		#	if [ $EUID -gt 99 ]; then
			#	pathappend .
		#	fi

		# End ~/.bash_profile
	EOF
	cat > %{buildroot}/etc/skel/.profile <<- "EOF"
		# Begin ~/.profile
		# Personal environment variables and startup programs.

		if [ -d "$HOME/bin" ] ; then
			pathprepend $HOME/bin
		fi

		# Set up user specific i18n variables
		#	export LANG=<ll>_<CC>.<charmap><@modifiers>

		# End ~/.profile
	EOF
	cat > %{buildroot}/etc/skel/.bashrc <<- "EOF"
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

		# Set up user specific i18n variables
		#	export LANG=<ll>_<CC>.<charmap><@modifiers>

		# End ~/.bashrc
	EOF
	cat > %{buildroot}/etc/skel/.bash_logout <<- "EOF"
		# Begin ~/.bash_logout
		# Written for Beyond Linux From Scratch
		# by James Robertson <jameswrobertson@earthlink.net>

		# Personal items to perform on logout.

		# End ~/.bash_logout
	EOF
	cat > %{buildroot}/etc/skel/dircolors.sh <<- "EOF"
		# Setup for /bin/ls and /bin/grep to support color, the alias is in /etc/bashrc.
		#	run the following as a user
		#	dircolors -p > ~/.dircolors to use directory colours
		if [ -f "/etc/dircolors" ] ; then
			eval $(dircolors -b /etc/dircolors)
		fi

		if [ -f "$HOME/.dircolors" ] ; then
			eval $(dircolors -b $HOME/.dircolors)
		fi

		alias ls='ls --color=auto'
		alias grep='grep --color=auto'
	EOF
	#
	#	vim
	#
	cat > %{buildroot}/etc/vimrc <<- "EOF"
		" Begin .vimrc

		set columns=80
		set wrapmargin=8
		set ruler

		" End .vimrc
	EOF
	cat > %{buildroot}/etc/skel/vimrc <<- "EOF"
		" Begin .vimrc

		set columns=80
		set wrapmargin=8
		set ruler

		" End .vimrc
	EOF
	install --directory --mode=0755 --owner=root --group=root %{buildroot}/usr/bin
	cat > %{buildroot}/usr/bin/which <<- "EOF"
		#!/bin/bash
		type -pa "$@" | head -n 1 ; exit ${PIPESTATUS[0]}
	EOF
	chmod -v 755 %{buildroot}/usr/bin/which
	chown -v root:root %{buildroot}/usr/bin/which
%install
	make DESTDIR=%{buildroot} install-random
	#	Create file list
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Jan 09 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version