REM echo OFF

mkdir build
cd build

set WITHOUT_FLAGS=-DWITH_BZIP2=OFF -DWITH_DOXYGEN=OFF -DWITH_EXPAT=OFF -DWITH_ICU=OFF -DWITH_MPI=OFF -DWITH_VALGRIND=OFF -DWITH_XSLTPROC=OFF -DWITH_ZLIB=OFF
set WITH_FLAGS=-DWITH_PYTHON=ON -DCMAKE_INSTALL_PREFIX=C:\opt\rosdeps\x86
set NO_STATIC=-DENABLE_STATIC:BOOL=FALSE -DENABLE_STATIC_RUNTIME:BOOL=FALSE
set BUILD_PROJECTS=^
preprocessor;concept_check;property_map;config;mpl;type_traits;function;iterator;smart_ptr;exception;^
utility;integer;detail;static_assert;tuple;function_types;fusion;typeof;proto;intrusive;logic;numeric;^
xpressive;optional;tokenizer;io;bind;date_time;thread;^
algorithm;range;foreach;array;functional;unordered;pool;spirit;variant;serialization;format;math;^
multi_index;any;random;graph;python;parameter;accumulators;system;asio;circular_buffer;ptr_container;^
assign;bimap;compatibility;conversion;crc;timer;test;disjoint_sets;dynamic_bitset;filesystem;^
interprocess;flyweight;geometry;gil;regex;^
icl;iostreams;lambda;msm;multi_array;phoenix;polygon;program_options;property_tree;^
ratio;rational;signals;signals2;statechart;tr1;units;uuid;wave
SET FAILED_TO_BUILD_PROJECTS=chrono;
set WILL_BE_DISABLED_PROJECTS_BECAUSE_OF_DEPS=mpi;graph_parallel

cmake -G "NMake Makefiles" %WITHOUT_FLAGS% %WITH_FLAGS% -DBUILD_PROJECTS:STRING=%BUILD_PROJECTS% %NO_STATIC% ..\boost
nmake
REM nmake package
REM nmake install
cd ..
