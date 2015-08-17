#![feature(no_std)]
#![no_std]
#![crate_type = "rlib"]
#![feature(lang_items, asm)]
//#![feature(core_intrinsics)]
//#![feature(core)]
#![feature(core_slice_ext)]

#![allow(dead_code)]
#![allow(non_snake_case)]

extern {
//    fn nrf_lib_gpio_range_cfg_output(pin_range_start: u32, pin_range_end: u32);
//    fn nrf_lib_gpio_port_write(port: u8, value: u8);
//    fn nrf_lib_delay_ms(number_of_ms: u32);
    fn ll_init(data: *const u8) -> i16;
    fn ll_set_advertising_data(data: *const u8, len: u8) -> i16;
    fn ll_set_scan_response_data(data: *const u8, len: u8) -> i16;
    fn ll_advertise_start(ptype: u8, interval: u32, chmap: u8) -> i16;
    fn evt_loop_run();
}

//enum ll_pdu_t {
//    LL_PDU_ADV_IND,
//    LL_PDU_ADV_DIRECT_IND,
//    LL_PDU_ADV_NONCONN_IND,
//    LL_PDU_SCAN_REQ,
//    LL_PDU_SCAN_RSP,
//    LL_PDU_CONNECT_REQ,
//    LL_PDU_ADV_SCAN_IND
//}

pub fn ble_init(data: &[u8]) -> bool {
    unsafe {
        ll_init(data.as_ptr()) == 0
    }
}

pub fn ble_set_advertising_data(data: &[u8]) -> bool {
    unsafe {
        ll_set_advertising_data(data.as_ptr(), data.len() as u8) == 0
    }
}

pub fn ble_set_scan_response_data(data: &[u8]) -> bool {
    unsafe {
        ll_set_scan_response_data(data.as_ptr(), data.len() as u8) == 0
    }
}

pub fn ble_advertise_start(ptype: u8, interval: u32, chmap: u8) -> bool {
    unsafe {
        ll_advertise_start(ptype, interval, chmap) == 0
    }
}

#[no_mangle]
pub fn main() {
    let addr = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x01 ];
    let data = [0x0F, 0x09, 0x62, 0x6C, 0x65, 0x73, 0x73, 0x65, 0x64,
                0x20, 0x64, 0x65, 0x76, 0x69, 0x63, 0x65];
    let scan_data = [0x03, 0x19, 0x00, 0x00];
    ble_init(&addr);
    ble_set_advertising_data(&data);
    ble_set_scan_response_data(&scan_data);
    ble_advertise_start(0x06, 1280000, 0x07);
    unsafe { evt_loop_run(); }
//    loop {
//    }
}
