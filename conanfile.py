from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
import shutil

class SpeexdspConan(ConanFile):
    name = "speexdsp"
    version = "1.2.0"
    license = "BSD"
    author = "Chris Collins <kuroneko@sysadninjas.net>"
    url = "https://git.sysadninjas.net/conan/speexdsp"
    description = "SpeexDSP Audio Processing Library"
    topics = ("audio preprocessing", "audio", "sound")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    generators = "cmake"
    exports_sources = "cmake-build-src/*"

    def source(self):
        tools.get('http://downloads.us.xiph.org/releases/speex/speexdsp-%s.tar.gz'%self.version)
        shutil.copy("cmake-build-src/CMakeLists.txt", "speexdsp-%s/"%self.version)


    def _configure_cmake(self):
        cmake = CMake(self, parallel=False)
        cmake.configure(source_folder="speexdsp-%s"%self.version)
        return cmake

    def build(self):
        if self.settings.os == 'Windows' or self.settings.os == 'Macos':
            cmake = self._configure_cmake()
            cmake.build()
        else:
            autotools = AutoToolsBuildEnvironment(self)
            autotools.fpic = self.options.fPIC
            config_args=['--with-fft=smallft']
            if self.options.shared:
                config_args+=['--enable-shared=true', '--enable-static=false']
            else:
                config_args+=['--enable-shared=false', '--enable-static=true']

            autotools.configure(configure_dir='speexdsp-%s'%self.version, args=config_args)
            autotools.make()

    def package(self):
        self.copy("*.h", dst="include", src="speexdsp-%s/include"%self.version)
        self.copy("speexdsp_config_types.h", dst="include/speex", src="include/speex", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.exp", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["speexdsp"]

