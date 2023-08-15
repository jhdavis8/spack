# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xsbench(MakefilePackage, CudaPackage):
    """XSBench is a mini-app representing a key computational
    kernel of the Monte Carlo neutronics application OpenMC.
    A full explanation of the theory and purpose of XSBench
    is provided in docs/XSBench_Theory.pdf."""

    homepage = "https://github.com/ANL-CESAR/XSBench/"
    url = "https://github.com/ANL-CESAR/XSBench/archive/v13.tar.gz"

    tags = ["proxy-app", "ecp-proxy-app"]

    version("20", sha256="3430328267432b4c29605f248809caec3e8b0e3442d4dcd672fa09b8bb9aa1b6")
    version("19", sha256="57cc44ae3b0a50d33fab6dd48da13368720d2aa1b91cde47d51da78bf656b97e", deprecated=True)
    version("18", sha256="a9a544eeacd1be8d687080d2df4eeb701c04eda31d3806e7c3ea1ff36c26f4b0", deprecated=True)
    version("14", sha256="595afbcba8c1079067d5d17eedcb4ab0c1d115f83fd6f8c3de01d74b23015e2d", deprecated=True)
    version("13", sha256="b503ea468d3720a0369304924477b758b3d128c8074776233fa5d567b7ffcaa2", deprecated=True)

    variant("mpi", default=False, description="Build with MPI support")
    variant("openmp-threading", default=False, description="Build with OpenMP Threading support")

    depends_on("mpi", when="+mpi")
    
    @property
    def build_directory(self):
        spec = self.spec
        
        if "+openmp-threading" in spec:
            return "openmp-threading"

        if "+cuda" in spec:
            return "cuda"

    @property
    def build_targets(self):
        targets = []
        cflags = ""

        if "+cuda" in self.spec:
            return ["SM_VERSION={0}".format(self.spec.variants["cuda_arch"].value[0])]

        if not self.spec.satisfies("%nvhpc@:20.11"):
            cflags = "-std=gnu99"

        if "+mpi" in self.spec:
            targets.append("CC={0}".format(self.spec["mpi"].mpicc))
            targets.append("MPI=yes")
        else:
            targets.append("CC={0}".format(self.compiler.cc))
            targets.append("MPI=no")

        if "+openmp" in self.spec:
            cflags += " " + self.compiler.openmp_flag
        targets.append("CFLAGS={0}".format(cflags))
        targets.append("LDFLAGS=-lm")

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        with working_dir(self.build_directory):
            install("XSBench", prefix.bin)
