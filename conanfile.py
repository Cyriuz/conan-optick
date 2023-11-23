from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import copy, get, rm, rmdir, export_conandata_patches, apply_conandata_patches
import os

required_conan_version = ">=1.55.0"


class OptickConan(ConanFile):
    name = "optick"
    description = (
        "Optick is a super-lightweight C++ profiler for Games."
        "It provides access for all the necessary tools required for efficient performance analysis and optimization:"
        "instrumentation, switch-contexts, sampling, GPU counters."
    )
    url = "https://github.com/bombomby/optick"
    homepage = "https://github.com/bombomby/optick"
    license = "MIT"
    topics = ("profiler")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
    }
    default_options = {
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        pass

    def configure(self):
        pass

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        pass

    def validate(self):
        pass

    def build_requirements(self):
        self.tool_requires("cmake/3.25.2")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        VirtualBuildEnv(self).generate()
        tc = CMakeToolchain(self)
        tc.generate()
        CMakeDeps(self).generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rm(self, "*pdb", os.path.join(self.package_folder, "bin"))

    def package_info(self):
        debug_suffix = "d" if self.settings.build_type == "Debug" else ""
        self.cpp_info.set_property("cmake_file_name", "optick")
        self.cpp_info.set_property("cmake_target_name", "optick::optick")
        self.cpp_info.libs = [f"OptickCore{debug_suffix}"]

        # TODO: to remove in conan v2 once cmake_find_package* generators removed
        self.cpp_info.names["cmake_find_package"] = "optick"
        self.cpp_info.names["cmake_find_package_multi"] = "optick"