# FIXME:
%global debug_package %{nil}

# https://github.com/jstaf/onedriver
%global goipath		github.com/jstaf/onedriver
%global forgeurl	https://github.com/jstaf/onedriver
Version:			0.14.1

%gometa

Summary:	A native Linux filesystem for Microsoft Onedrive
Name:		onedriver

Release:	1
License:	GPLv3+
Group:		Network
Source0:	https://github.com/jstaf/onedriver/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		onedriver-0.14.1-install_path.patch
URL:		https://github.com/jstaf/onedriver
BuildRequires:	compiler(go-compiler)
BuildRequires:	imagemagick

%if ! %{with bootstrap2}
BuildRequires:	golang(github.com/coreos/go-systemd/v22)
BuildRequires:	golang(github.com/godbus/dbus/v5)
BuildRequires:	golang(github.com/gotk3/gotk3/gtk)
BuildRequires:	golang(github.com/hanwen/go-fuse/v2)
BuildRequires:	golang(github.com/imdario/mergo)
BuildRequires:	golang(github.com/rs/zerolog)
BuildRequires:	golang(github.com/rs/zerolog/log)
BuildRequires:	golang(github.com/spf13/pflag)
BuildRequires:	golang(github.com/stretchr/testify)
BuildRequires:	golang(gopkg.in/yaml.v3)
BuildRequires:	golang(go.etcd.io/bbolt)
BuildRequires:	pkgconfig(webkitgtk-3.0)
BuildRequires:	pkgconfig(webkit2gtk-4.1)
%endif

%description
Onedriver is a native Linux filesystem for Microsoft Onedrive. Files and
metadata are downloaded on-demand instead of syncing the entire drive to
your local computer.

NOTE: OneDrive is not a free software based service.

%files
%license LICENSE
%doc README.md pkg/resources/config-example.yml
%{_bindir}/%{name}
%{_bindir}/%{name}-launcher
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/applications/%{name}.desktop
%{_userunitdir}/%{name}@.service
%{_mandir}/man1/%{name}.1*

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%gobuildroot
export LDFLAGS+=" -X github.com/jstaf/onedriver/cmd/common.commit=%{version}"
for bin in onedriver onedriver-launcher ; do
	%gobuild -o _bin/$bin ./cmd/$bin
done

%install
#goinstall
for bin in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$bin %{buildroot}%{_bindir}/$bin
done

# icons
for d in 16 32 48 64 72 128 256
do
	install -dpm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -size "${d}x${d}" pkg/resources/%{name}.svg \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dpm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -size 32x32 pkg/resources/%{name}.svg \
	%{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# .desktop
desktop-file-install \
	--set-icon=%{name} \
	--dir=%{buildroot}%{_datadir}/applications/ \
	pkg/resources/%{name}.desktop

# manpage
install -dpm 0755 %{buildroot}%{_mandir}/man1/
install -Dpm 0644 pkg/resources/%{name}.1 %{buildroot}%{_mandir}/man1/

# systemd
install -dpm 0755 %{buildroot}%{_userunitdir}/
install -Dpm 0644 pkg/resources/%{name}@.service %{buildroot}%{_userunitdir}/

