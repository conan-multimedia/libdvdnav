from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from shutil import copyfile
import os

class LibdvdnavConan(ConanFile):
    name = "libdvdnav"
    version = "5.0.1"
    description = "libdvdnav is a library for developers of multimedia applications. "
    "It allows easy use of sophisticated DVD navigation features such as DVD menus, multiangle playback and even interactive DVD games"
    url = "https://github.com/conan-multimedia/libdvdnav"
    homepage = "http://dvdnav.mplayerhq.hu/"
    license = "GPLv2Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = "libdvdread/5.0.0@conanos/dev"

    source_subfolder = "source_subfolder"

    download_url = 'http://www.videolan.org/pub/videolan/libdvdnav/5.0.1/libdvdnav-5.0.1.tar.bz2'

    def source(self):
        tools.get('http://www.videolan.org/pub/videolan/{name}/{version}/{name}-{version}.tar.bz2'.format(name=self.name,version=self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            with tools.environment_append({
                'PKG_CONFIG_PATH' : "%s/lib/pkgconfig"%(self.deps_cpp_info["libdvdread"].rootpath)
                }):
                #self.run('autoreconf -f -i')
                _args = ["--prefix=%s/builddir"%(os.getcwd())]
                autotools = AutoToolsBuildEnvironment(self)
                autotools.configure(args=_args)
                autotools.make(args=["-j4"])
                autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                excludes="*.a" if self.options.shared else  "*.so*"
                self.copy("*", src="%s/builddir"%(os.getcwd()), excludes=excludes)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

