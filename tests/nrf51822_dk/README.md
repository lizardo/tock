These samples contain the bare minimum to test Rust based projects for
nRF51822-DK.

Requirements:

* [nRF51 SDK 4.4.2](https://developer.nordicsemi.com/nRF51_SDK/nRF51_SDK_v4.x.x/) (ZIP version)
* [gcc-arm-none-eabi-4\_9-2015q2](https://launchpad.net/gcc-arm-embedded/+download)
* [JLink 5.02](https://www.segger.com/jlink-software.html)
* rustc 1.4.0-nightly (e35fd7481 2015-08-17)
* blessed sources: https://github.com/lizardo/blessed

Hardware: nRF51822-DK PCA10001 V1.0

Build instructions (replace "blink" with the demo to build):

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/rust-nightly/lib
export PATH=$PATH:/opt/rust-nightly/bin:/opt/gcc-arm-none/bin

make -C tests/nrf51822_dk/blink
make -C tests/nrf51822_dk/blink flash
```

For the broadcaster example, set the BLESSED\_SRC variable to the path of the
blessed repository sources.
