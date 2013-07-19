Name:           web-assets
Version:        1
Release:        1%{?dist}
Summary:        A simple framework for bits pushed to browsers
BuildArch:      noarch

License:        MIT
URL:            https://fedoraproject.org/wiki/User:Patches/PackagingDrafts/Web_Assets

Source1:        web-assets-LICENSE
Source2:        macros.web-assets
Source3:        web-assets.conf

%description
%{summary}.

%package filesystem
Summary:        The basic directory layout for Web Assets
#there's nothing copyrightable about a few directories and symlinks
License:        Public Domain

%description filesystem
%{summary}.

%package devel
Summary:        RPM macros for Web Assets packaging
License:        MIT
Requires:       web-assets-filesystem

%description devel
%{summary}.

%package httpd
Summary:        Web Assets aliases for the Apache HTTP daemon
License:        MIT
Requires:       web-assets-filesystem
Requires:       httpd
Requires(post): systemd
Requires(postun): systemd

%description httpd
%{summary}.

%prep
%setup -c -T
cp %{SOURCE2} LICENSE

%build
#nothing to do

%install
mkdir -p %{buildroot}%{_datadir}/assets
mkdir -p %{buildroot}%{_datadir}/javascript

ln -sf ../javascript %{buildroot}%{_datadir}/assets/javascript
ln -sf ../fonts %{buildroot}%{_datadir}/assets/fonts

install -Dpm0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.d/macros.web-assets
install -Dpm0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/web-assets.conf

%post httpd
systemctl reload-or-try-restart httpd.service || :

%postun httpd
systemctl reload-or-try-restart httpd.service || :

%files filesystem
%{_datadir}/assets
%{_datadir}/javascript

%files devel
%{_rpmconfigdir}/macros.d/macros.web-assets
%doc LICENSE

%files httpd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/web-assets.conf
%doc LICENSE

%changelog
* Thu Jul 11 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1-1
- initial package

