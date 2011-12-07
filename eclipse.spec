# TODO:
# - see why about.html isn't being copied on ppc
# - fix ant libs
Epoch:  1

%global eclipse_major   3
%global eclipse_minor   5
%global eclipse_majmin  %{eclipse_major}.%{eclipse_minor}
%global eclipse_micro   2
%global initialize      1
%global download_url    http://download.eclipse.org/technology/linuxtools/eclipse-build/
%global bootstrap 0

# All arches line up between Eclipse and Linux kernel names except i386 -> x86
%ifarch %{ix86}
%define eclipse_arch    x86
%else
%define eclipse_arch   %{_arch}
%endif

# FIXME:  update java packaging guidelines for this.  See
# fedora-devel-java-list discussion in September 2008.
#
# Prevent brp-java-repack-jars from being run.
%define __jar_repack 0

Summary:        An open, extensible IDE
Name:           eclipse
Version:        %{eclipse_majmin}.%{eclipse_micro}
Release:        5%{?dist}
License:        EPL
Group:          Text Editors/Integrated Development Environments (IDE)
URL:            http://www.eclipse.org/
Source0:        %{download_url}eclipse-build-0.5.0.tar.bz2
Source1:        %{download_url}eclipse-3.5.2-src.tar.bz2
Source2:        eclipse.sh.in
Source17:       efj.sh.in
# This file contains the types of files we'd like to extract from the jars
# when using the FileInitializer
Source19:       %{name}-filenamepatterns.txt
# This script copies the platform sub-set of the SDK for generating metadata
Source28:       %{name}-mv-Platform.sh

# Make sure the shipped target platform templates are looking in the
# correct location for source bundles (see RHBZ # 521969). This does not
# need to go upstream.
Patch0:        %{name}-target-platform-template.patch
# make o.e.swt.gtk.linux.ppc64 version to match ppc 
Patch1:        %{name}-swt-ppc64-version.patch
Patch2:        %{name}-rhel-deps.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ant ant-nodeps
BuildRequires:  jpackage-utils >= 0:1.5, make, gcc
BuildRequires:  gnome-vfs2-devel
BuildRequires:  gtk2-devel
BuildRequires:  glib2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  gcc-c++
BuildRequires:  gecko-devel >= 1.9
BuildRequires:  nspr-devel
BuildRequires:  libXtst-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  cairo >= 1.0
BuildRequires:  unzip
BuildRequires:  desktop-file-utils
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  java-javadoc
BuildRequires:  libXt-devel
BuildRequires:  xulrunner-devel

%if !%{bootstrap}
BuildRequires:  icu4j-eclipse >= 1:4.0.1-3
BuildRequires:  apache-jasper >= 5.5.28
BuildRequires:  apache-tomcat-apis
BuildRequires: ant-antlr ant-apache-bcel ant-apache-log4j ant-apache-oro ant-apache-regexp ant-apache-resolver ant-commons-logging ant-apache-bsf ant-commons-net
BuildRequires: ant-javamail ant-jdepend ant-junit ant-swing ant-trax ant-jsch
BuildRequires: jsch >= 0:0.1.41
BuildRequires: jakarta-commons-el >= 1.0-9
BuildRequires: jakarta-commons-logging >= 1.0.4-6jpp.3
BuildRequires: jakarta-commons-codec
BuildRequires: jakarta-commons-httpclient
BuildRequires: jetty-eclipse >= 6.1.21-1
BuildRequires: lucene >= 2.3.1-3.4
BuildRequires: lucene-contrib >= 2.3.1-3.4
BuildRequires: junit >= 3.8.1-3jpp
BuildRequires: junit4
BuildRequires: hamcrest >= 0:1.1-9.2
BuildRequires: sat4j >= 2.1.1-1
BuildRequires: objectweb-asm
%endif

%if 0%{?rhel} >= 6
ExclusiveArch: i686 x86_64
%endif

%description
The Eclipse platform is designed for building integrated development
environments (IDEs), server-side applications, desktop applications, and
everything in between.

%package     swt
Summary:        SWT Library for GTK+-2.0
Group:          Text Editors/Integrated Development Environments (IDE)
# %{_libdir}/java directory owned by jpackage-utils
Requires:       jpackage-utils
Requires:       gtk2
Requires:       gecko-libs >= 1.9
Conflicts:      mozilla
Provides:       libswt3-gtk2 = 1:%{version}-%{release}
# The 20 is more than the currently (2008-06-25) latest 3.3.2 package
# but I want to leave some room in case we need to do an F9 update.
Obsoletes:       libswt3-gtk2 < 1:3.3.2-20

%description swt
SWT Library for GTK+-2.0.

%package        rcp
Summary:        Eclipse Rich Client Platform
Group:          Development/Languages
Requires:       %{name}-swt = %{epoch}:%{version}-%{release}
%if ! %{bootstrap}
Requires:       icu4j-eclipse >= 1:4.0.1-3
%endif
Requires:       java >= 1.6.0

%description    rcp
Eclipse Rich Client Platform

%package        platform
Summary:        Eclipse platform common files
Group:          Text Editors/Integrated Development Environments (IDE)
Requires:   %{name}-rcp = %{epoch}:%{version}-%{release}
%if ! %{bootstrap}
Requires: ant-antlr ant-apache-bcel ant-apache-log4j ant-apache-oro ant-apache-regexp ant-apache-resolver ant-commons-logging ant-apache-bsf ant-commons-net
Requires: ant-javamail ant-jdepend ant-junit ant-nodeps ant-swing ant-trax ant-jsch
Requires: jakarta-commons-el >= 1.0-9
Requires: jakarta-commons-logging >= 1.0.4-6jpp.3
Requires: jakarta-commons-codec
Requires: apache-jasper >= 5.5.28
Requires: apache-tomcat-apis
Requires: jetty-eclipse >= 6.1.21-1
Requires: jsch >= 0.1.41
Requires: lucene >= 2.3.1-3.4
Requires: lucene-contrib >= 2.3.1-3.4
Requires: sat4j >= 2.1.1-1
%endif
Provides: eclipse-cvs-client = 1:%{version}-%{release}
Obsoletes: eclipse-cvs-client < 1:3.3.2-20

%description    platform
The Eclipse Platform is the base of all IDE plugins.  This does not include the
Java Development Tools or the Plugin Development Environment.

%package        jdt
Summary:        Eclipse Java Development Tools
Group:          Text Editors/Integrated Development Environments (IDE)
Requires:       %{name}-platform = %{epoch}:%{version}-%{release}
Requires:       %{name}-cvs-client = %{epoch}:%{version}-%{release}
%if ! %{bootstrap}
Requires:       junit >= 3.8.1-3jpp
Requires:       junit4
Requires:       jakarta-commons-httpclient
%endif
Requires:       java-javadoc
Requires:       java-devel

%description    jdt
Eclipse Java Development Tools.  This package is required to use Eclipse for
developing software written in the Java programming language.

%package        pde
Summary:        Eclipse Plugin Development Environment
Group:          Text Editors/Integrated Development Environments (IDE)
Provides:       eclipse = %{epoch}:%{version}-%{release}
Provides:       eclipse-sdk = %{epoch}:%{version}-%{release}
Requires:       %{name}-platform = %{epoch}:%{version}-%{release}
Requires:       %{name}-jdt = %{epoch}:%{version}-%{release}
%if ! %{bootstrap}
Requires:       objectweb-asm
Requires:       hamcrest >= 0:1.1-9.2
%endif
# For PDE Build wrapper script
Requires:       bash
Provides:       %{name}-pde-runtime = 1:%{version}-%{release}
Obsoletes:      %{name}-pde-runtime < 1:3.3.2-20

%description    pde
Eclipse Plugin Development Environment.  This package is required for
developing Eclipse plugins.

%prep
%setup -q -n eclipse-build-0.5.0
cp %{SOURCE1} .
ant -DbuildArch=%{eclipse_arch} applyPatches
pushd build/eclipse-%{version}-src

# Use our system-installed javadocs, reference only what we built, and
# don't like to osgi.org docs (FIXME:  maybe we should package them?)
sed -i -e "s|http://java.sun.com/j2se/1.4.2/docs/api|%{_datadir}/javadoc/java|" \
   -e "/osgi\.org/d" \
   -e "s|-breakiterator|;../org.eclipse.equinox.util/@dot\n;../org.eclipse.ecf.filetransfer_3.0.0.v20090302-0803.jar\n;../org.eclipse.ecf_3.0.0.v20090302-0803.jar\n-breakiterator|" \
    plugins/org.eclipse.platform.doc.isv/platformOptions.txt
sed -i -e "s|http://java.sun.com/j2se/1.5/docs/api|%{_datadir}/javadoc/java|" \
   -e "s/win32.win32.x86/gtk.linux.%{eclipse_arch}/" \
   plugins/org.eclipse.jdt.doc.isv/jdtaptOptions.txt \
   plugins/org.eclipse.jdt.doc.isv/jdtOptions.txt
sed -i -e "s|http://java.sun.com/j2se/1.4/docs/api|%{_datadir}/javadoc/java|" \
   -e "s/motif.linux.x86/gtk.linux.%{eclipse_arch}/" \
   plugins/org.eclipse.pde.doc.user/pdeOptions.txt \
   plugins/org.eclipse.pde.doc.user/pdeOptions.txt

# Remove signatures for JARs
find -iname \*.sf | xargs rm
find -iname \*.rsa | xargs rm

# FIXME:  do this as part of Linux distros project
#
# the swt version is set to HEAD on s390x but shouldn't be
# get swt version
SWT_MAJ_VER=$(grep maj_ver plugins/org.eclipse.swt/Eclipse\ SWT/common/library/make_common.mak | cut -f 2 -d =)
SWT_MIN_VER=$(grep min_ver plugins/org.eclipse.swt/Eclipse\ SWT/common/library/make_common.mak | cut -f 2 -d =)
SWT_VERSION=$SWT_MAJ_VER$SWT_MIN_VER
swt_frag_ver=$(grep v$SWT_VERSION plugins/org.eclipse.swt.gtk.linux.x86/build.xml | sed "s:.*<.*\"\(.*\)\" />:\1:")
swt_frag_ver_s390x=$(grep "version\.suffix\" value=" plugins/org.eclipse.swt.gtk.linux.s390x/build.xml | sed "s:.*<.*\"\(.*\)\" />:\1:")
sed --in-place "s|$swt_frag_ver_s390x|$swt_frag_ver|g" plugins/org.eclipse.swt.gtk.linux.s390x/build.xml \
                                                      plugins/org.eclipse.swt.gtk.linux.s390x/META-INF/MANIFEST.MF

%if ! %{bootstrap}
# make sure there are no jars left
JARS=""
for j in $(find -name \*.jar); do
  if [ ! -L $j ]; then
    JARS="$JARS `echo $j`"
  fi
done
if [ ! -z "$JARS" ]; then
    echo "These jars should be deleted and symlinked to system jars: $JARS"
   #FIXME: enable  exit 1
fi
%endif

# target platform template patch
%patch0 -p0
# make o.e.swt.gtk.linux.ppc64 version to match ppc 
#%patch1
popd
%patch2 -b .sav

%build
export JAVA_HOME=%{java_home}
./build.sh

%install
rm -rf $RPM_BUILD_ROOT
# Get swt version
SWT_MAJ_VER=$(grep maj_ver build/eclipse-%{version}-src/plugins/org.eclipse.swt/Eclipse\ SWT/common/library/make_common.mak | cut -f 2 -d =)
SWT_MIN_VER=$(grep min_ver build/eclipse-%{version}-src/plugins/org.eclipse.swt/Eclipse\ SWT/common/library/make_common.mak | cut -f 2 -d =)
SWT_VERSION=$SWT_MAJ_VER$SWT_MIN_VER

ant -DdestDir=$RPM_BUILD_ROOT -Dprefix=/usr -DbuildArch=%{eclipse_arch} -Dmultilib=true install

pushd $RPM_BUILD_ROOT%{_libdir}/%{name}
rm -f eclipse.ini
ln -s $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
popd

# Set GDK_NATIVE_WINDOWS=true
# https://bugzilla.redhat.com/531675 (https://bugs.eclipse.org/290395)
rm $RPM_BUILD_ROOT/%{_bindir}/%{name}
install -p -D -m0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/%{name}
sed --in-place "s:/usr/lib:%{_libdir}:" \
  $RPM_BUILD_ROOT%{_bindir}/%{name}

cp $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini eclipse.ini-real
# Some directories we need
sdkDir=$RPM_BUILD_ROOT%{_libdir}/%{name}
# FIXME:  We can probably get rid of the links directory (for the
# datadir.link file) when we ensure all plugins are installing into
# dropins (either in libdir or datadir).
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/java

# FIXME:  Please don't install stuff to these directories.  They're only
# still here for legacy plugins (which probably won't function in 3.4).
# We'll remove these later.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/features
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins

rm -fr $RPM_BUILD_ROOT%{_libdir}/eclipse/p2

LAUNCHERVERSION=$(ls $sdkDir/plugins | grep equinox.launcher_ | sed 's/org.eclipse.equinox.launcher_//')

installDir=$sdkDir-Platform
metadataDir=$installDir/metadata-Platform
provisionDir=$installDir-provisioned
profileId=PlatformProfile

# Copy just the platform
mkdir $installDir
pushd $installDir
sh %{SOURCE28} $sdkDir
mv plugins/*.source* $sdkDir/plugins
popd

# Generate metadata for the platform
java \
-cp $installDir/plugins/org.eclipse.equinox.launcher_$LAUNCHERVERSION \
org.eclipse.core.launcher.Main \
-application \
org.eclipse.equinox.p2.metadata.generator.EclipseGenerator \
-metadataRepository file:$metadataDir \
-artifactRepository file:$metadataDir \
-source $installDir \
-root "Eclipse Platform" \
-rootVersion %{version} \
-flavor tooling \
-publishArtifacts \
-append \
-artifactRepositoryName "Eclipse Platform" \
-metadataRepositoryName "Eclipse Platform" \
-debug -consolelog

# JDT
jdtDir=$sdkDir-JDT
jdtMetadata=$jdtDir/metadata-JDT

mkdir $jdtDir
pushd $jdtDir
mkdir features plugins
mv $sdkDir/features/org.eclipse.jdt_* features
for plugin in org.eclipse.jdt \
  org.eclipse.ant.ui \
  org.eclipse.jdt.apt.core \
  org.eclipse.jdt.apt.ui \
  org.eclipse.jdt.apt.pluggable.core \
  org.eclipse.jdt.compiler.apt \
  org.eclipse.jdt.compiler.tool \
  org.eclipse.jdt.core \
  org.eclipse.jdt.core.manipulation \
  org.eclipse.jdt.debug.ui \
  org.eclipse.jdt.debug \
  org.eclipse.jdt.junit \
  org.eclipse.jdt.junit.runtime \
  org.eclipse.jdt.junit4.runtime \
  org.eclipse.jdt.launching \
  org.eclipse.jdt.ui \
  org.eclipse.jdt.doc.user \
  org.hamcrest.core \
  org.junit \
  org.junit4 ; do
  mv $sdkDir/plugins/${plugin}_* plugins
done
popd

# Debugging?  Add -debug and -consolelog
# Provision with director
java \
-Declipse.p2.data.area=file:$provisionDir/p2 \
-Declipse.p2.MD5Check=false \
-cp $installDir/plugins/org.eclipse.equinox.launcher_$LAUNCHERVERSION \
org.eclipse.core.launcher.Main \
-application \
org.eclipse.equinox.p2.director \
-debug -consolelog \
-flavor tooling \
-installIU "Eclipse Platform" \
-p2.os linux \
-p2.ws gtk \
-p2.arch %{eclipse_arch} \
-roaming \
-profile $profileId \
-profileProperties org.eclipse.update.install.features=true \
-metadataRepository file:$metadataDir \
-artifactRepository file:$metadataDir \
-destination $provisionDir \
-bundlepool $provisionDir

# Stuff in JDT, PDE, SDK
for f in about.html about_files \.eclipseproduct epl-v10.html notice.html readme; do
    if [ -e $installDir/$f ]; then
      mv $installDir/$f $provisionDir
    fi
done
# FIXME:  should add artifacts.xml here
dropins=$provisionDir/dropins
mkdir -p $dropins/jdt $dropins/sdk
mv $jdtDir/features $dropins/jdt
mv $jdtDir/plugins $dropins/jdt

mv $sdkDir/features $dropins/sdk
mv $sdkDir/plugins $dropins/sdk
rm -rf $metadataDir $jdtDir $sdkDir $installDir

mv $provisionDir $sdkDir

# Fix paths in p2 data
rm -rf $sdkDir/p2/org.eclipse.equinox.p2.core/cache
rm -rf $sdkDir/p2/org.eclipse.equinox.p2.director/rollback/content.xml
sed -i "s|file\:$provisionDir/\ -\ bundle\ pool|Eclipse Platform|g" \
  $sdkDir/artifacts.xml
profileDir=$sdkDir/p2/org.eclipse.equinox.p2.engine/profileRegistry
pushd $profileDir
  sed -i "s|$provisionDir|%{_libdir}/%{name}|g" \
    PlatformProfile.profile/*
  sed -i "s|$RPM_BUILD_ROOT||g" PlatformProfile.profile/*
  sed -i "s|eclipse-Platform|eclipse|g" PlatformProfile.profile/*
popd

sed --in-place "s|SDKProfile|PlatformProfile|" \
  $RPM_BUILD_ROOT%{_libdir}/%{name}/configuration/config.ini

# Add a compatibility symlink to startup.jar
pushd $sdkDir
LAUNCHERNAME=$(ls plugins | grep equinox.launcher_)
ln -s plugins/$LAUNCHERNAME startup.jar
popd

# Remove the unnecessary configuration data
rm -r $sdkDir/configuration/org.eclipse.update

%if %{initialize}
# FIXME: investigate why it doesn't work to set this -- configuration data is
# always written to /usr/share/eclipse/configuration, even with
#     -Dosgi.sharedConfiguration.area=$RPM_BUILD_ROOT%{_libdir}/%{name}/configuration
# Note (2006-12-05):  upon looking at this again, we (bkonrath, overholt) don't
# know what we're doing with $libdir_path :)  It requires some investigation.
#
# Extract .so files
# https://bugs.eclipse.org/bugs/show_bug.cgi?id=90535
pushd $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_libdir}/eclipse/dropins  $RPM_BUILD_ROOT/dropins
mkdir $RPM_BUILD_ROOT%{_libdir}/eclipse/dropins
libdir_path=$(echo %{_libdir}/%{name} | sed -e 's/^\///')
java -Dosgi.sharedConfiguration.area=$RPM_BUILD_ROOT$libdir_path/configuration \
     -cp $libdir_path/startup.jar \
     org.eclipse.core.launcher.Main \
     -debug -consolelog \
     -metadataRepository file:$metadataDir \
     -artifactRepository file:$metadataDir \
     -application org.eclipse.equinox.initializer.configInitializer \
     -fileInitializer %{SOURCE19}
popd
rm -fr $RPM_BUILD_ROOT%{_libdir}/eclipse/dropins
mv $RPM_BUILD_ROOT/dropins $RPM_BUILD_ROOT%{_libdir}/eclipse/dropins

# Do this again after we've run the file initializer
rm -rf $sdkDir/p2/org.eclipse.equinox.p2.core/cache
rm -rf $sdkDir/p2/org.eclipse.equinox.p2.director/rollback/content.xml
rm -rf $sdkDir/p2/org.eclipse.equinox.p2.engine/.settings/org.eclipse.equinox.p2.artifact.repository.prefs
rm -rf $sdkDir/p2/org.eclipse.equinox.p2.engine/profileRegistry/PlatformProfile.profile/.data/.settings
pushd $profileDir
  sed -i "s|$RPM_BUILD_ROOT||g" *.profile/*
popd

# Remove the unnecessary configuration data
rm -r $sdkDir/configuration/org.eclipse.core.runtime
rm -r $sdkDir/configuration/org.eclipse.equinox.app
rm -rf $sdkDir/configuration/*.log
dataDirs=$(find $sdkDir/configuration \
  -type d -name data)
for dataDir in $dataDirs; do
    rm -rf `dirname $dataDir`
done

pushd $sdkDir
# Create file listings for the extracted shared libraries
echo -n "" > %{_builddir}/%{buildsubdir}/%{name}-platform.install;
for id in `ls configuration/org.eclipse.osgi/bundles`; do
  if [ "Xconfiguration" = $(echo X`find configuration/org.eclipse.osgi/bundles/$id -name libswt\*.so` | sed "s:/.*::") ]; then
    echo "%{_libdir}/%{name}/configuration/org.eclipse.osgi/bundles/$id" > %{_builddir}/%{buildsubdir}/%{name}-swt.install;
  else
    echo "%{_libdir}/%{name}/configuration/org.eclipse.osgi/bundles/$id" >> %{_builddir}/%{buildsubdir}/%{name}-platform.install;
  fi
done
popd

# Install symlinks to the SWT JNI shared libraries in %%{_libdir}/eclipse
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}
for lib in $(find configuration -name libswt\*.so); do
  ln -s $lib `basename $lib`
done
popd

# Ensure the shared libraries have the correct permissions
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}
for lib in `find configuration -name \*.so`; do
   chmod 755 $lib
done
popd
%endif

cp -p eclipse.ini-real \
  $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini

sed -i "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini

# Temporary fix until https://bugs.eclipse.org/294877 is resolved
sed -i "s|-Xms40m|-Xms128m|g" $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
sed -i "s|-Xmx256m|-Xmx512m|g" $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
echo "" >> $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
echo "-XX:CompileCommand=exclude,org/eclipse/core/internal/dtree/DataTreeNode,forwardDeltaWith" >> $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
echo "-XX:CompileCommand=exclude,org/eclipse/jdt/internal/compiler/lookup/ParameterizedMethodBinding,<init>" >> $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
echo "-XX:CompileCommand=exclude,org/eclipse/cdt/internal/core/dom/parser/cpp/semantics/CPPTemplates,instantiateTemplate" >> $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
echo "-XX:CompileCommand=exclude,org/eclipse/cdt/internal/core/pdom/dom/cpp/PDOMCPPLinkage,addBinding" >> $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
echo "-XX:CompileCommand=exclude,org/python/pydev/editor/codecompletion/revisited/PythonPathHelper,isValidSourceFile" >> $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini
echo "-XX:CompileCommand=exclude,org/python/pydev/ui/filetypes/FileTypesPreferencesPage,getDottedValidSourceFiles" >> $RPM_BUILD_ROOT/%{_sysconfdir}/eclipse.ini

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/links
# FIXME:  We can probably get rid of the links file when we ensure all
# plugins are installing into dropins (either in libdir or datadir).
# Set up an extension location and a link file for the arch-independent dir
echo "path:%{_datadir}" > \
  $sdkDir/links/datadir.link

# Ensure the launcher binary has the correct permissions
chmod 755 $RPM_BUILD_ROOT/%{_libdir}/%{name}/%{name}

# Install the SWT jar symlinks in libdir
SWTJARVERSION=$(grep %{version} build/eclipse-%{version}-src/plugins/org.eclipse.swt.gtk.linux.%{eclipse_arch}/build.xml | sed "s:.*<.*\"\(.*\)\" />:\1:")
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s plugins/org.eclipse.swt.gtk.linux.%{eclipse_arch}_$SWTJARVERSION.jar swt-gtk-%{eclipse_majmin}.%{eclipse_micro}.jar
ln -s swt-gtk-%{eclipse_majmin}.%{eclipse_micro}.jar swt-gtk-%{eclipse_majmin}.jar
ln -s swt-gtk-%{eclipse_majmin}.%{eclipse_micro}.jar swt.jar
ln -s ../%{name}/swt-gtk-%{eclipse_majmin}.%{eclipse_micro}.jar ../java/swt.jar
popd

# Install the efj wrapper script
install -p -D -m0755 %{SOURCE17} $RPM_BUILD_ROOT%{_bindir}/efj
sed --in-place "s:startup.jar:%{_libdir}/%{name}/startup.jar:" \
  $RPM_BUILD_ROOT%{_bindir}/efj

rm -rf $installDir

# A sanity check.
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# Create a script that can be used to make a symlink tree of the
# eclipse platform.
cp -p pdebuild/eclipse-copy-platform.sh copy-platform
(
  cd $RPM_BUILD_ROOT%{_libdir}/%{name}
  ls -d * | egrep -v '^(plugins|features|about_files|dropins)$'
  ls -d plugins/* features/*
) |
sed -e's,^\(.*\),[ ! -e \1 ] \&\& ln -s $eclipse/\1 \1,' >> copy-platform
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/buildscripts
mv copy-platform $RPM_BUILD_ROOT%{_libdir}/%{name}/buildscripts
copyPlatform=$RPM_BUILD_ROOT%{_libdir}/%{name}/buildscripts/copy-platform
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}
for p in $(ls -d dropins/jdt/plugins/*); do
    plugin=$(basename $p)
    echo $p | sed -e"s,^\(.*\),[ ! -e plugins/$plugin ] \&\& ln -s \$eclipse/\1 plugins/$plugin," >> $copyPlatform
done
for p in $(ls -d dropins/sdk/plugins/*); do
    plugin=$(basename $p)
    echo $p | sed -e"s,^\(.*\),[ ! -e plugins/$plugin ] \&\& ln -s \$eclipse/\1 plugins/$plugin," >> $copyPlatform
done
popd

sed --in-place "s|$RPM_BUILD_ROOT%{_libdir}/eclipse-Platform/p2/|%{_libdir}/eclipse/p2/|" \
  $RPM_BUILD_ROOT%{_libdir}/%{name}/configuration/config.ini
sed --in-place "s|file\\\:%{_libdir}/eclipse/p2/|@config.dir/../p2/|" \
  $RPM_BUILD_ROOT%{_libdir}/%{name}/configuration/config.ini

# Install the PDE Build wrapper script.
install -p -D -m0755 pdebuild/eclipse-pdebuild.sh \
  $RPM_BUILD_ROOT%{_libdir}/%{name}/buildscripts/pdebuild
PDEBUILDVERSION=$(ls $RPM_BUILD_ROOT%{_libdir}/%{name}/dropins/sdk/plugins \
  | grep org.eclipse.pde.build_ | \
  sed 's/org.eclipse.pde.build_//')
sed -i "s/@PDEBUILDVERSION@/$PDEBUILDVERSION/g" \
  $RPM_BUILD_ROOT%{_libdir}/%{name}/buildscripts/pdebuild

%if ! %{bootstrap}
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}

pushd dropins/jdt
build-jar-repository -s -p plugins/org.junit_* junit

JUNIT4VERSION=$(ls plugins | grep org.junit4_ | sed 's/org.junit4_//')
rm plugins/org.junit4_$JUNIT4VERSION/junit.jar
ln -s %{_javadir}/junit4.jar plugins/org.junit4_$JUNIT4VERSION/junit.jar
popd

# link to the icu4j stuff
ICUVERSION=$(ls plugins | grep com.ibm.icu_ | sed 's/com.ibm.icu_//')
rm plugins/com.ibm.icu_*.jar

SAT4JVERSION=$(ls plugins | grep org.sat4j.core_ | \
  sed 's/org.sat4j.core_//')
rm plugins/org.sat4j*
ln -s %{_javadir}/org.sat4j.core* plugins/org.sat4j.core_$SAT4JVERSION
ln -s %{_javadir}/org.sat4j.pb* plugins/org.sat4j.pb_$SAT4JVERSION

ASMPLUGINVERSION=$(ls dropins/sdk/plugins | grep org.objectweb.asm_ | \
  sed 's/org.objectweb.asm_//')
rm dropins/sdk/plugins/org.objectweb.asm_$ASMPLUGINVERSION
ln -s %{_javadir}/objectweb-asm/asm-all.jar \
  dropins/sdk/plugins/org.objectweb.asm_$ASMPLUGINVERSION

# Duplicate junit4
rm -rf dropins/sdk/plugins/org.junit4

# link to hamcrest-core
HAMCRESTCOREVERSION=$(ls dropins/jdt/plugins | grep org.hamcrest.core_ | \
  sed 's/org.hamcrest.core_//')
rm dropins/jdt/plugins/org.hamcrest.core_$HAMCRESTCOREVERSION
ln -s %{_javadir}/hamcrest/core.jar \
  dropins/jdt/plugins/org.hamcrest.core_$HAMCRESTCOREVERSION

JETTYPLUGINVERSION=$(ls plugins | grep org.mortbay.jetty.server_6 | sed 's/org.mortbay.jetty.server_//')
rm plugins/org.mortbay.jetty.server_$JETTYPLUGINVERSION
ln -s %{_datadir}/jetty-eclipse/lib/jetty-6.1.21.jar plugins/org.mortbay.jetty.server_$JETTYPLUGINVERSION

JETTYUTILVERSION=$(ls plugins | grep org.mortbay.jetty.util_6 | sed 's/org.mortbay.jetty.util_//')
rm plugins/org.mortbay.jetty.util_$JETTYUTILVERSION
ln -s %{_datadir}/jetty-eclipse/lib/jetty-util-6.1.21.jar plugins/org.mortbay.jetty.util_$JETTYUTILVERSION

JSCHVERSION=$(ls plugins | grep com.jcraft.jsch_ | sed 's/com.jcraft.jsch_//')
rm plugins/com.jcraft.jsch_$JSCHVERSION
ln -s %{_javadir}/jsch.jar plugins/com.jcraft.jsch_$JSCHVERSION

# link to lucene
LUCENEVERSION=$(ls plugins | grep org.apache.lucene_ | \
  sed 's/org.apache.lucene_//')
rm plugins/org.apache.lucene_*
ln -s %{_javadir}/lucene.jar plugins/org.apache.lucene_$LUCENEVERSION
rm plugins/org.apache.lucene.analysis_*
ln -s %{_javadir}/lucene-contrib/lucene-analyzers.jar \
  plugins/org.apache.lucene.analysis_$LUCENEVERSION

# link to commons-logging
COMMONSLOGGINGVERSION=$(ls plugins | grep commons.logging_ | \
  sed 's/org.apache.commons.logging_//')
rm plugins/org.apache.commons.logging_$COMMONSLOGGINGVERSION
ln -s %{_javadir}/commons-logging.jar \
  plugins/org.apache.commons.logging_$COMMONSLOGGINGVERSION

# link to commons-el
COMMONSELVERSION=$(ls plugins | grep commons.el_ | \
  sed 's/org.apache.commons.el_//')
rm plugins/org.apache.commons.el_$COMMONSELVERSION
ln -s %{_javadir}/commons-el.jar \
  plugins/org.apache.commons.el_$COMMONSELVERSION

# link to commons-codec
COMMONSCODECVERSION=$(ls plugins | grep commons.codec_ | \
  sed 's/org.apache.commons.codec_//')
rm plugins/org.apache.commons.codec_$COMMONSCODECVERSION
ln -s %{_javadir}/commons-codec.jar \
  plugins/org.apache.commons.codec_$COMMONSCODECVERSION

# link to commons-httpclient
COMMONSHTTPVERSION=$(ls plugins | grep commons.httpclient_ | \
  sed 's/org.apache.commons.httpclient_//')
rm plugins/org.apache.commons.httpclient_$COMMONSHTTPVERSION
ln -s %{_javadir}/commons-httpclient.jar \
  plugins/org.apache.commons.httpclient_$COMMONSHTTPVERSION

# link to jasper
JASPERVERSION=$(ls plugins | grep org.apache.jasper_ | \
  sed 's/org.apache.jasper_//')
rm plugins/org.apache.jasper_*.jar
ln -s %{_javadir}/apache-jasper-5.5.28.jar \
   plugins/org.apache.jasper_$JASPERVERSION

# link to servlet-api
SERVLETAPIVERSION=$(ls plugins | grep javax.servlet_ | \
  sed 's/javax.servlet_//')
rm plugins/javax.servlet_*
ln -s %{_javadir}/apache-tomcat-apis/tomcat-servlet2.5-api.jar \
  plugins/javax.servlet_$SERVLETAPIVERSION

# link to jsp-api
JSPAPIVERSION=$(ls plugins | grep javax.servlet.jsp_ | \
  sed 's/javax.servlet.jsp_//')
rm plugins/javax.servlet.jsp_*
ln -s %{_javadir}/apache-tomcat-apis/tomcat-jsp2.0-api.jar \
  plugins/javax.servlet.jsp_$JSPAPIVERSION

## BEGIN ANT ##
ANTDIR=plugins/$(ls plugins | grep org.apache.ant_)
rm $ANTDIR/lib/*
ANTDIR=$ANTDIR/lib
ln -s %{_javadir}/ant/ant-antlr.jar $ANTDIR/ant-antlr.jar
ln -s %{_javadir}/ant/ant-apache-bcel.jar $ANTDIR/ant-apache-bcel.jar
ln -s %{_javadir}/ant/ant-apache-bsf.jar $ANTDIR/ant-apache-bsf.jar
ln -s %{_javadir}/ant/ant-apache-log4j.jar $ANTDIR/ant-apache-log4j.jar
ln -s %{_javadir}/ant/ant-apache-oro.jar $ANTDIR/ant-apache-oro.jar
ln -s %{_javadir}/ant/ant-apache-regexp.jar $ANTDIR/ant-apache-regexp.jar
ln -s %{_javadir}/ant/ant-apache-resolver.jar $ANTDIR/ant-apache-resolver.jar
ln -s %{_javadir}/ant/ant-commons-logging.jar $ANTDIR/ant-commons-logging.jar
ln -s %{_javadir}/ant/ant-commons-net.jar $ANTDIR/ant-commons-net.jar
#ln -s %{_javadir}/ant/ant-jai.jar $ANTDIR/ant-jai.jar
ln -s %{_javadir}/ant.jar $ANTDIR/ant.jar
ln -s %{_javadir}/ant/ant-javamail.jar $ANTDIR/ant-javamail.jar
ln -s %{_javadir}/ant/ant-jdepend.jar $ANTDIR/ant-jdepend.jar
#ln -s %{_javadir}/ant/ant-jmf.jar $ANTDIR/ant-jmf.jar
ln -s %{_javadir}/ant/ant-jsch.jar $ANTDIR/ant-jsch.jar
ln -s %{_javadir}/ant/ant-junit.jar $ANTDIR/ant-junit.jar
ln -s %{_javadir}/ant-launcher.jar $ANTDIR/ant-launcher.jar
#ln -s %{_javadir}/ant/ant-netrexx.jar $ANTDIR/ant-netrexx.jar
ln -s %{_javadir}/ant/ant-nodeps.jar $ANTDIR/ant-nodeps.jar
#ln -s %{_javadir}/ant/ant-starteam.jar $ANTDIR/ant-starteam.jar
#ln -s %{_javadir}/ant/ant-stylebook.jar $ANTDIR/ant-stylebook.jar
ln -s %{_javadir}/ant/ant-swing.jar $ANTDIR/ant-swing.jar
ln -s %{_javadir}/ant/ant-trax.jar $ANTDIR/ant-trax.jar
#ln -s %{_javadir}/ant/ant-weblogic.jar $ANTDIR/ant-weblogic.jar
## END ANT ##

popd
%endif

# Be sure that we have a symlink to /etc/eclipse.ini
pushd $RPM_BUILD_ROOT%{_libdir}/%{name}
rm -f eclipse.ini
ln -s %{_sysconfdir}/eclipse.ini
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post platform
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%postun platform
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%if %{initialize}
%files swt -f %{name}-swt.install
%else
%files swt
%endif
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%if %{initialize}
%dir %{_libdir}/%{name}/libswt-*.so
%dir %{_libdir}/%{name}/configuration
%dir %{_libdir}/%{name}/configuration/org.eclipse.osgi
%dir %{_libdir}/%{name}/configuration/org.eclipse.osgi/bundles
%endif
%{_libdir}/%{name}/plugins/org.eclipse.swt_*
%{_libdir}/%{name}/plugins/org.eclipse.swt.gtk.linux.%{eclipse_arch}_*
%{_libdir}/%{name}/swt-gtk*.jar
%{_libdir}/%{name}/swt.jar
%{_libdir}/java/swt.jar

%files rcp
%defattr(-,root,root)
%dir %{_libdir}/%{name}/features
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/features
%dir %{_datadir}/%{name}/plugins
%if %{initialize}
%{_libdir}/%{name}/configuration/org.eclipse.osgi/.bundledata*
%{_libdir}/%{name}/configuration/org.eclipse.osgi/.lazy*
%{_libdir}/%{name}/configuration/org.eclipse.osgi/.manager
%{_libdir}/%{name}/configuration/org.eclipse.osgi/.state*
%endif
%if %{bootstrap}
%{_libdir}/%{name}/plugins/com.ibm.icu_*
%endif
%config %{_libdir}/%{name}/configuration
%config %{_libdir}/%{name}/configuration/config.ini
%config %{_libdir}/%{name}/configuration/org.eclipse.equinox.simpleconfigurator/bundles.info
%dir %{_libdir}/%{name}/configuration/org.eclipse.equinox.simpleconfigurator
%{_libdir}/%{name}/notice.html
%{_libdir}/%{name}/epl-v10.html
%{_libdir}/%{name}/links
%ifnarch ppc ppc64
%{_libdir}/%{name}/about.html
%endif
%ifarch x86_64
%{_libdir}/%{name}/about_files
%endif
%{_libdir}/%{name}/readme
%{_libdir}/%{name}/startup.jar
%{_libdir}/%{name}/features/org.eclipse.rcp_*
%{_libdir}/%{name}/plugins/org.eclipse.core.commands_*
%{_libdir}/%{name}/plugins/org.eclipse.core.contenttype_*
%{_libdir}/%{name}/plugins/org.eclipse.core.databinding_*
%{_libdir}/%{name}/plugins/org.eclipse.core.databinding.beans_*
%{_libdir}/%{name}/plugins/org.eclipse.core.databinding.observable_*
%{_libdir}/%{name}/plugins/org.eclipse.core.databinding.property_*
%{_libdir}/%{name}/plugins/org.eclipse.core.expressions_*
%{_libdir}/%{name}/plugins/org.eclipse.core.jobs_*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime_*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime.compatibility.auth_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.app_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.common_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.ds_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.launcher_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.launcher.gtk.linux.%{eclipse_arch}_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.preferences_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.registry_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.util_*
%{_libdir}/%{name}/plugins/org.eclipse.help_*
%{_libdir}/%{name}/plugins/org.eclipse.jface_*
%{_libdir}/%{name}/plugins/org.eclipse.jface.databinding_*
%{_libdir}/%{name}/plugins/org.eclipse.osgi_*
%{_libdir}/%{name}/plugins/org.eclipse.rcp_*
%{_libdir}/%{name}/plugins/org.eclipse.ui_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench_*
%{_libdir}/%{name}/plugins/org.eclipse.update.configurator_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.simpleconfigurator_*

%if %{initialize}
%files platform -f %{name}-platform.install
%else
%files platform
%endif
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/%{name}
%config %{_libdir}/%{name}/eclipse.ini
%config %{_sysconfdir}/eclipse.ini
%ifnarch ppc ppc64
%{_libdir}/%{name}/about_files
%endif
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/*/*/apps/*
%{_libdir}/%{name}/eclipse
%dir %{_libdir}/%{name}/dropins
%dir %{_datadir}/%{name}/dropins
%{_libdir}/%{name}/features/org.eclipse.platform_*
%{_libdir}/%{name}/plugins/com.jcraft.jsch_*
%{_libdir}/%{name}/plugins/javax.servlet_*
%{_libdir}/%{name}/plugins/javax.servlet.jsp_*
%{_libdir}/%{name}/plugins/org.apache.ant_*
%{_libdir}/%{name}/plugins/org.apache.commons.el_*
%{_libdir}/%{name}/plugins/org.apache.commons.logging_*
%{_libdir}/%{name}/plugins/org.apache.lucene_*
%{_libdir}/%{name}/plugins/org.apache.lucene.analysis_*
%{_libdir}/%{name}/plugins/org.eclipse.ant.core_*
%{_libdir}/%{name}/plugins/org.eclipse.compare_*
%{_libdir}/%{name}/plugins/org.eclipse.compare.core_*
%{_libdir}/%{name}/plugins/org.eclipse.core.boot_*
%{_libdir}/%{name}/plugins/org.eclipse.core.filebuffers_*
%{_libdir}/%{name}/plugins/org.eclipse.core.filesystem_*
%{_libdir}/%{name}/plugins/org.eclipse.core.filesystem.linux.%{eclipse_arch}_*
%{_libdir}/%{name}/plugins/org.eclipse.core.net_*
%ifarch %{ix86}
%{_libdir}/%{name}/plugins/org.eclipse.core.net.linux.x86_*
%{_libdir}/%{name}/plugins/org.eclipse.update.core.linux_*
%endif
%{_libdir}/%{name}/plugins/org.eclipse.core.resources_*
%{_libdir}/%{name}/plugins/org.eclipse.core.resources.compatibility_*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime.compatibility_*
%{_libdir}/%{name}/plugins/org.eclipse.core.runtime.compatibility.registry_*
%{_libdir}/%{name}/plugins/org.eclipse.core.variables_*
%{_libdir}/%{name}/plugins/org.eclipse.debug.core_*
%{_libdir}/%{name}/plugins/org.eclipse.debug.ui_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.http.jetty_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.http.registry_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.http.servlet_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.jsp.jasper_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.jsp.jasper.registry_*
%{_libdir}/%{name}/plugins/org.eclipse.help.appserver_*
%{_libdir}/%{name}/plugins/org.eclipse.help.base_*
%{_libdir}/%{name}/plugins/org.eclipse.help.ui_*
%{_libdir}/%{name}/plugins/org.eclipse.help.webapp_*
%{_libdir}/%{name}/plugins/org.eclipse.jface.text_*
%{_libdir}/%{name}/plugins/org.eclipse.jsch.core_*
%{_libdir}/%{name}/plugins/org.eclipse.jsch.ui_*
%{_libdir}/%{name}/plugins/org.eclipse.ltk.core.refactoring_*
%{_libdir}/%{name}/plugins/org.eclipse.ltk.ui.refactoring_*
%{_libdir}/%{name}/plugins/org.eclipse.osgi.services_*
%{_libdir}/%{name}/plugins/org.eclipse.osgi.util_*
%{_libdir}/%{name}/plugins/org.eclipse.platform_*
%{_libdir}/%{name}/plugins/org.eclipse.platform.doc.user_*
%{_libdir}/%{name}/plugins/org.eclipse.search_*
%{_libdir}/%{name}/plugins/org.eclipse.team.core_*
%{_libdir}/%{name}/plugins/org.eclipse.team.ui_*
%{_libdir}/%{name}/plugins/org.eclipse.text_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.browser_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.cheatsheets_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.console_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.editors_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.externaltools_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.forms_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.ide_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.ide.application_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.intro_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.intro.universal_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.navigator_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.navigator.resources_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.net_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.presentations.r21_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.views_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.views.properties.tabbed_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench.compatibility_*
%{_libdir}/%{name}/plugins/org.eclipse.ui.workbench.texteditor_*
%{_libdir}/%{name}/plugins/org.eclipse.update.core_*
%{_libdir}/%{name}/plugins/org.eclipse.update.scheduler_*
%{_libdir}/%{name}/plugins/org.eclipse.update.ui_*
%{_libdir}/%{name}/plugins/org.mortbay.jetty.util_*
%{_libdir}/%{name}/plugins/org.mortbay.jetty.server_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.initializer_*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.core_*
%{_libdir}/%{name}/plugins/org.eclipse.cvs_*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ssh2_*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ssh_*
%{_libdir}/%{name}/plugins/org.eclipse.team.cvs.ui_*
%{_libdir}/%{name}/features/org.eclipse.cvs_*
%{_libdir}/%{name}/features/org.eclipse.help_*
%{_libdir}/%{name}/plugins/org.apache.jasper_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.frameworkadmin_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.frameworkadmin.equinox_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.simpleconfigurator.manipulator_*
%{_libdir}/%{name}/features/org.eclipse.equinox.p2.user.ui_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.director_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.core_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.engine_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.jarprocessor_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.metadata_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.metadata.repository_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.artifact.repository_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.exemplarysetup_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.touchpoint.eclipse_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.touchpoint.natives_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.console_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.ui_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.ui.sdk_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.ui.sdk.scheduler_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.updatechecker_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.garbagecollector_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.directorywatcher_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.publisher_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.repository_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.repository.tools_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.reconciler.dropins_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.metadata.generator_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.updatesite_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.security_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.security.ui_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.extensionlocation_*
%{_libdir}/%{name}/plugins/org.eclipse.equinox.p2.director.app_*
%{_libdir}/%{name}/plugins/org.eclipse.ecf.provider.filetransfer_*
%{_libdir}/%{name}/plugins/org.eclipse.ecf.provider.filetransfer.httpclient_*
%{_libdir}/%{name}/plugins/org.eclipse.ecf.provider.filetransfer.httpclient.ssl_*
%{_libdir}/%{name}/plugins/org.eclipse.ecf.provider.filetransfer.ssl_*
%{_libdir}/%{name}/plugins/org.eclipse.ecf.ssl_*
%{_libdir}/%{name}/plugins/org.eclipse.ecf_*
%{_libdir}/%{name}/plugins/org.eclipse.ecf.filetransfer_*
%{_libdir}/%{name}/plugins/org.eclipse.ecf.identity_*
%{_libdir}/%{name}/plugins/org.apache.commons.codec_*
%{_libdir}/%{name}/plugins/org.apache.commons.httpclient_*
%{_libdir}/%{name}/plugins/org.sat4j.core_*
%{_libdir}/%{name}/plugins/org.sat4j.pb_*
# Put this in -platform since we're putting the p2 stuff here
%{_libdir}/%{name}/artifacts.xml
# FIXME: should we ship content.xml for the platform?
#%{_libdir}/%{name}/metadata
%{_libdir}/%{name}/p2

%files jdt
%defattr(-,root,root)
%{_bindir}/efj
%{_libdir}/%{name}/dropins/jdt

%files pde
%defattr(-,root,root)
%{_libdir}/%{name}/buildscripts
%{_libdir}/%{name}/dropins/sdk
# FIXME:  where should this go?
#%{_libdir}/%{name}/configuration/org.eclipse.equinox.source

%changelog
* Thu Jun 10 2010 Andrew Overholt <overholt@redhat.com> 1:3.5.2-5
- Re-symlink after provisioning (rhbz#601902).
- Move hamcrest to dropins/jdt (rhbz#602866).

* Tue Mar 23 2010 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.2-3.2
- Fix rhel dependencies patch.

* Tue Mar 23 2010 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.2-3.1
- Rebase to Galileo SR2.

* Mon Mar 08 2010 Jeff Johnston <jjohnstn@redhat.com> 1:3.5.1-24.6
- Resolves: #569939
- Replace jetty requirement with jetty-eclipse package.

* Wed Mar 03 2010 Andrew Overholt <overholt@redhat.com> 1:3.5.1-24.5
- Bring over o.e.jdt.junit dropins fix from Fedora.

* Tue Feb 02 2010 Andrew Overholt <overholt@redhat.com> 1:3.5.1-24.4
- Move to Tomcat-less Jasper and Servlet/JSP API packages.
- Use latest jetty which uses above packages.

* Thu Jan 07 2010 Andrew Overholt <overholt@redhat.com> 1:3.5.1-24.2
- Version Provides for "eclipse" and "eclipse-sdk" (-pde).

* Fri Dec 11 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.1-24.2
- Revert to using xulrunner-devel-unstable and gecko-libs.

* Tue Dec  8 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:3.5.1-24.1
- Only build on x86 and x86_64 for RHEL 6

* Fri Dec 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-24
- Replace gecko BR/Rs with xulrunner.
- Drop xulrunner-devel-unstable now that it's merged in xulrunner-devel.

* Thu Dec 3 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-23
- Remove old manipulations to bundles.info.
- Update to eclipse-build 0.4 release.

* Mon Nov 30 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.1-22
- Move ant-nodeps out of bootstrap.

* Tue Nov 17 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.1-21
- Fix typo in memory settings.

* Tue Nov 17 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-20
- Fix ppc64 swt jar version.

* Mon Nov 16 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.1-19
- Temporarily patch for e.o#294877.
- Fix some whitespace.

* Fri Nov 13 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-18
- No about files on ppc64 too.

* Wed Nov 11 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-17
- Update to eclipse-build 0.4 RC4 (fixes pdebuild escaping).

* Tue Nov 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-16
- Specify -DbuildArch when running ant applyPatches.

* Tue Nov 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-15
- Update to eclipse-build 0.4 RC3.

* Fri Nov 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-14
- Fix build with commons-codec 1.4.

* Fri Oct 30 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.1-13
- Make /usr/bin/eclipse a wrapper script due to rhbz#531675 (e.o#290395).

* Mon Oct 26 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.1-12
- Remove old TODO items.

* Fri Oct 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-12
- No need to invoke desktop-file-install, it's handled by e-b install now. 

* Thu Oct 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-11
- Remove ppc64 files copying and sedding. Supported by eclipse-build now.

* Tue Oct 20 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-10
- Remove old/not needed BR/Rs.

* Mon Oct 19 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-9
- New e-b snapshot that contains fragments for ppc64.

* Thu Oct 15 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-8
- Add bootstrap flag.

* Mon Oct 12 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-7
- Put back JAVA_HOME.

* Mon Oct 12 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-6
- New eclipse-build snapshot. Pdebuild and ecf compilation are part of it.

* Thu Oct 8 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-5
- Fix install call.

* Thu Oct 8 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-4
- New eclipse-build snapshot. Remove parts included in it.

* Wed Oct 07 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.1-3
- Add patch for bugs.eclipse.org/287307

* Mon Oct 5 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-2
- Add /usr/share/eclipse/dropins to dropins locations.

* Fri Oct 2 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.1-1
- Update to 3.5.1.

* Tue Sep 29 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-4
- Symlink to unversioned jetty jars.

* Tue Sep 29 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-3
- Build with eclipse-build 0.4.0 RC0.

* Wed Sep 23 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.0-2
- Move jakarta-commons-codec requirement from jdt to platform.

* Tue Sep 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-1
- Fix help toolbar jsp problem.

* Fri Sep 18 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.13
- Update ecf-filetransfer and build it.

* Tue Sep 15 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.12
- Build with system jetty.

* Mon Sep 14 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.0-0.11
- Add /usr/share/eclipse/dropins to list of dropins locations
  (rhbz#522117).

* Wed Sep 09 2009 Mat Booth <fedora@matbooth.co.uk> 1:3.5.0-0.10
- Patch the target platform templates so they find all the required
  source bundles (see RHBZ # 521969).

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.9
- Remove all testframework sources, patches, build and etc.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.8
- Use system hamcrest.

* Mon Aug 17 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.7
- Use o.e.equinox.initializer from SOURCE1 instead of separate one.

* Fri Aug 14 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.6
- Do not use the provided eclipse.ini but the one from build.

* Thu Aug 13 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.5
- Add epoch to icu4j Requires/BuildRequires.

* Tue Aug 11 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.4.0
- Fix sources url.
- Make it use system icu4j and sat4j.

* Fri Aug 7 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.35
- Another missing ppc64 fragment.

* Fri Aug 7 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.34
- Fix missing fragment on ppc64.

* Thu Aug 6 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.33
- Fix missing launcher for ppc64.

* Wed Aug 5 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.32
- Manually enable o.e.core.runtime and o.e.equinox.ds because it's not enabled on ppc64.

* Wed Aug 5 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.31
- Revert initialize call path changes.

* Wed Aug 5 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.30
- Additional output to debug ppc64 build failures.

* Wed Aug 5 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.29
- Reenable initialize.
- Fix paths in initializer call.

* Wed Aug 5 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.28
- Disable initialize.

* Tue Aug 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.27
- No need to copy eclipse.ini for secondary archs.

* Tue Aug 4 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.26
- eclipse/about_files are not installed on ppc for some reason.

* Mon Aug 3 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.3.25
- Swith to eclipse-build for building.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.0-0.3.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.2.9
- Fix package-build template to add target for -Dconfigs.

* Tue May 19 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.0-0.2.8
- Remove Fedora branding.

* Thu May 7 2009 Andrew Overholt <overholt@redhat.com> 1:3.5.0-0.2.7
- Update patch to tests' library.xml to allow for easy debugging of tests.

* Wed Apr 29 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.2.6
- Fix initializer run (sed again).

* Wed Apr 29 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.2.5
- Bump tomcat6 BR.
- Fix director run to not require sed on bundles.info.

* Wed Apr 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.2.4
- Update to newer I-build.
- Update fedora customization.
- Bump dependencies minimal versions.
- Fix update site functionality.
- Simplify jdt %%files section.

* Tue Apr 14 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.2.3
- Rediff patch30.

* Tue Apr 14 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.2.2
- Fix version of source bundles.

* Mon Apr 13 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.2.1
- Create org.eclipse.swt.gtk.linux.* based on the ppc version.

* Mon Apr 13 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.2
- Remove patches for the ecj package and others already applied upstream.
- Rediff some ppc64 patches.

* Mon Apr 13 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.1.12
- o.e.update.core.linux is x86 only.

* Mon Apr 13 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.1.11
- Remove more p2 generated files.

* Mon Apr 13 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.1.10
- Do not install p2 generatad file.

* Fri Apr 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.1.9
- BR/R jakarta-commons-codec and jakarta-commons-httpclient.

* Thu Apr 9 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.1.8
- Add patch for xulrunner compilation.

* Tue Apr 7 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.1.7
- Fix patch name.

* Thu Apr 2 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.5.0-0.1.6
- First try for 3.5 build.
