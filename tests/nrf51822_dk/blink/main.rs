#![feature(no_std)]
#![no_std]
#![crate_type = "rlib"]
#![feature(lang_items, asm)]
//#![feature(core_intrinsics)]
//#![feature(core)]

#![allow(dead_code)]
#![allow(non_snake_case)]

extern {
    fn nrf_lib_gpio_range_cfg_output(pin_range_start: u32, pin_range_end: u32);
    fn nrf_lib_gpio_port_write(port: u8, value: u8);
    fn nrf_lib_delay_ms(number_of_ms: u32);
}

#[no_mangle]
pub fn main() {
    unsafe { nrf_lib_gpio_range_cfg_output(18,19); }

    loop {
        unsafe {
            nrf_lib_gpio_port_write(2,8);
            nrf_lib_delay_ms(80);
            nrf_lib_gpio_port_write(2,4);
            nrf_lib_delay_ms(80);
        }
    }
}
