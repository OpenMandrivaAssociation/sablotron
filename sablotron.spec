%define	altname Sablot
%define builddir $RPM_BUILD_DIR/%{altname}-%{version}
%define libname_orig libsablotron

%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%define jscript 1
%define readline 0
%define GPL 0

Summary:	XSLT, XPath and DOM processor
Name:		sablotron
Version:	1.0.3
Release:	14
%if %{GPL} 
License:	GPL
%else
License:	MPL/GPL
%endif
Group:		Development/Other
URL:		http://www.gingerall.cz
Source0:	http://download-1.gingerall.cz/download/sablot/%{altname}-%{version}.tar.bz2
Source1:	http://download-1.gingerall.cz/download/sablot/SabTest-%{version}.tar.bz2
Patch0:		Sablot-linkage_fix.diff
Patch1:		sablot-automake-1.13.patch
BuildRequires:	expat-devel >= 1.95.2
BuildRequires:	perl-XML-Parser
BuildRequires:	ncurses-devel
BuildRequires:	libstdc++-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.9 >= 1.9.2
BuildRequires:	libtool
%if %{jscript}
BuildRequires:	js-devel >= 1.5
BuildRequires:	pkgconfig
%endif 
%if %{readline}
BuildRequires:	readline-devel
%endif

%description
Sablotron is a fast, compact and portable XML toolkit
implementing XSLT, DOM and XPath.

The goal of this project is to create a lightweight,
reliable and fast XML library processor conforming to the W3C
specification, which is available for public and can be used as a base
for multi-platform XML applications.

%package -n	%{libname}
Summary:	Main library for sablotron
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n	%{libname}
Contains the library for sablotron.

%package -n	%{develname}
Summary:	The development libraries and header files for Sablotron
Requires:	sablotron = %{version}
Group:		Development/C
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	sablotron-devel = %{version}
Obsoletes:	%{mklibname %{name} -d 0}

%description -n	%{develname}
These are the development libraries and header files for Sablotron

%prep

%if %{readline} && !%{GPL}
echo "The readline library may not be linked to non GPL'ed programs, so if you want to have readline support in the debugger, you have to choose the GPL from Sablotron license model."
exit 1
%endif

%setup -q -n %{altname}-%{version} -a1
%patch0 -p0
%patch1 -p1 -b .am113~

perl -pi -e 's,SABLOT_LIBS="-L\$sab_base/lib",SABLOT_LIBS="-L\$sab_base/%{_lib}",' SabTest-%{version}/configure{.in,}

%if %{jscript}
JS_INCLUDE_PATH=`pkg-config --cflags libjs|sed -e 's/-I\/usr//'`
perl -pi -e "s|/include/js\b|$JS_INCLUDE_PATH|g" configure*
%endif
touch NEWS AUTHORS ChangeLog
autoreconf -fi
pushd SabTest-%{version}
touch NEWS AUTHORS ChangeLog
autoreconf -fi
popd

%build

export CXXFLAGS="%{optflags}"

%if %{jscript}
export CPLUS_INCLUDE_PATH=`pkg-config --cflags libjs|sed -e 's/-I//'`
%endif

%if %{GPL}
export SABLOT_GPL=1
%endif

%configure2_5x \
%if %{jscript}
    --enable-javascript=%{_prefix} \
%endif
%if %{GPL} && %{readline}
    --with-readline \
%endif
    --enable-debugger

%make

%check
# make and run the test suite
make DESTDIR=`pwd`/SabTest-%{version} install
pushd SabTest-%{version}
touch NEWS AUTHORS ChangeLog
libtoolize --copy --force; aclocal; autoconf; automake --add-missing --copy
%configure2_5x --with-sablot=`pwd`/usr
%make
make test
make test-js
popd

%install
rm -rf %{buildroot}

%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/sablot-config

# nuke installed docs
rm -rf %{buildroot}%{_datadir}/doc

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(0755,root,root)
%{_bindir}/sabcmd
%_mandir/man1/*

%files -n %{libname}
%defattr(-,root,root)
%doc README RELEASE doc/misc/NOTES doc/misc/DEBUGGER
%{_libdir}/libsablot.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/apidoc/sablot doc/apidoc/jsdom-ref doc/apidoc/sxp
%{_bindir}/sablot-config
%{multiarch_bindir}/sablot-config
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_includedir}/*.h


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-10mdv2011.0
+ Revision: 661750
- multiarch fixes

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-9mdv2011.0
+ Revision: 607486
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-8mdv2010.1
+ Revision: 519068
- rebuild

* Mon Sep 28 2009 Olivier Blin <oblin@mandriva.com> 1.0.3-7mdv2010.0
+ Revision: 450337
- use autoreconf -fi to get rid of libtool errors
  (from Arnaud Patard)

* Sun Sep 27 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.3-6mdv2010.0
+ Revision: 449822
- fix tests

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-6mdv2009.1
+ Revision: 317636
- rebuild

* Fri Jul 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-5mdv2009.0
+ Revision: 231772
- added P0 to fix linkage (-lexpat)
- fix devel package naming
- fix build (partly)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 25 2008 Olivier Blin <oblin@mandriva.com> 1.0.3-4mdv2008.1
+ Revision: 190045
- fix build by removing conditional defines
- use Development/C group for devel package (thanks pterjan)
- restore BuildRoot

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jun 07 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.3-2mdv2008.0
+ Revision: 36950
- rebuild for expat


* Tue Feb 13 2007 Olivier Blin <oblin@mandriva.com> 1.0.3-1mdv2007.0
+ Revision: 120628
- use a perl one-liner to replace previous patch for lib64 tests
- don't require expat package
- 1.0.3 (and drop now useless patches)
- Import sablotron

* Wed Aug 24 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.0.2-2mdk
- lib64 fixes

* Sun May 22 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdk
- 1.0.2
- rediffed P0
- added the test suite
- use new rpm-4.4.x pre,post magic

* Wed Mar 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.1-7mdk
- make it find the headers
- fix deps and conditional %%multiarch

* Sat Jul 17 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.0.1-6mdk
- add BuildRequires: perl-XML-Parser

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.1-5mdk
- rebuild

* Wed Jun 09 2004 Götz Waschk <waschk@linux-mandrake.com> 1.0.1-4mdk
- patch for new g++

* Sun May 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.1-3mdk
- might as well let it provide sablotron-devel

* Sun May 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.1-2mdk
- disable readline support

* Fri May 21 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0.1-1mdk
- use the %%configure2_5x macro
- sync with the spec file by Petr Cimpricg <petr@gingerall.cz>
- spec file cleanups

