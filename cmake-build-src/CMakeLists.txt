PROJECT(speexdsp LANGUAGES C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(FFT_SOURCES
    libspeexdsp/smallft.c)

add_library(speexdsp STATIC
    libspeexdsp/preprocess.c
    libspeexdsp/jitter.c
    libspeexdsp/mdf.c
    libspeexdsp/fftwrap.c
    libspeexdsp/filterbank.c
    libspeexdsp/resample.c
    libspeexdsp/buffer.c
    libspeexdsp/scal.c
    ${FFT_SOURCES})
set_property(TARGET speexdsp
    PROPERTY PUBLIC_HEADER
    include/speex/speex_buffer.h
    include/speex/speex_echo.h
    include/speex/speex_jitter.h
    include/speex/speex_preprocess.h
    include/speex/speex_resampler.h
    include/speex/speexdsp_types.h)
target_include_directories(speexdsp
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
    PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/speex>)
target_compile_definitions(speexdsp
    PRIVATE 
    FLOATING_POINT
    USE_SSE
    USE_SMALLFT
    "INCLUDE_STDINT=#include <stdint.h>"
    EXPORT= )
install(TARGETS speexdsp
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    PUBLIC_HEADER DESTINATION include)
