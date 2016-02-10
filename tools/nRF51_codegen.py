#!/usr/bin/env python
# Generate chip specific code from CMSIS SVD definitions.
# To install the cmsis-svd dependency:
#   pip install -U cmsis-svd
from __future__ import print_function
from cmsis_svd.parser import SVDParser

PROGRAM = "tools/nRF51_codegen.py"

# A subset of keywords that may appear as register names
RUST_KEYWORDS = ["in"]

def dump_json(parser):
    """Dump the SVD model as JSON."""
    import json
    svd_dict = parser.get_device().to_dict()
    print(json.dumps(svd_dict, sort_keys=True, indent=4,
        separators=(',', ': ')))

def get_peripheral_interrupts(parser):
    # Cortex M0 supports up to 32 external interrupts
    # Source: See ARMv6-M Architecture Reference Manual,
    # Table C-2 "Programmers' model feature comparison"
    interrupts = [""] * 32

    for peripheral in parser.get_device().peripherals:
        for intr in peripheral.interrupts:
            if interrupts[intr.value]:
                assert interrupts[intr.value] == intr.name
            else:
                interrupts[intr.value] = intr.name

    return interrupts

def dump_as_c_macro(name, lines, outfile, indent=0):
    print("#define %s \\" % name, file=outfile)
    for (n, line) in enumerate(lines):
        line = "\t" * indent + line
        if n < len(lines) - 1:
            line += " \\"
        print(line, file=outfile)

def dump_macros(interrupts, outfile):
    print("/* Automatically generated by %s */" % PROGRAM, file=outfile)

    lines = []
    for name in interrupts:
        if name:
            lines.append("%s_Handler," % name)
        else:
            lines.append("0, /* Reserved */")
    dump_as_c_macro("PERIPHERAL_INTERRUPT_VECTORS", lines, outfile, 1)

    lines = []
    for name in interrupts:
        if not name:
            continue
        lines.append('void %s_Handler(void) __attribute__ ' % name +
            '((weak, alias("Dummy_Handler")));')
    dump_as_c_macro("PERIPHERAL_INTERRUPT_HANDLERS", lines, outfile)

def get_peripheral_registers(parser, peripheral_names=[]):
    peripherals = {}
    for peripheral in parser.get_device().peripherals:
        if peripheral_names and peripheral.name not in peripheral_names:
            continue
        peripherals[peripheral.name] = {
            "base_address": peripheral.base_address,
            "registers": []
        }
        for register in peripheral.registers:
            if register.dim:
                assert register.dim_increment == 4
                assert register.dim_index == range(0, register.dim)
                array_size = register.dim
            else:
                array_size = 0
            peripherals[peripheral.name]["registers"].append((register.name,
                register.address_offset, array_size))
    return peripherals

def dump_registers(peripherals, outfile):
    print("// Automatically generated by %s" % PROGRAM, file=outfile)
    print("use common::VolatileCell;", file=outfile)

    for pname in peripherals.keys():
        print("", file=outfile)
        print("pub const %s_BASE: usize = 0x%08X;" % (pname,
            peripherals[pname]["base_address"]), file=outfile)
        print("pub struct %s {" % pname, file=outfile)
        cur_ofs = 0
        pad_id = 0
        for (rname, offset, array_size) in peripherals[pname]["registers"]:
            rname = rname.replace("[%s]", "").lower()
            if rname in RUST_KEYWORDS:
                rname += "_"
            if offset != cur_ofs:
                assert offset > cur_ofs
                print("    _pad%d: [u8; %d]," % (pad_id, offset - cur_ofs), file=outfile)
                pad_id += 1
            if array_size:
                print("    pub %s: [VolatileCell<u32>; %d]," % (rname, array_size), file=outfile)
            else:
                print("    pub %s: VolatileCell<u32>," % rname, file=outfile)
            cur_ofs = offset + 4
        print("}", file=outfile)

def main():
    parser = SVDParser.for_packaged_svd('Nordic', 'nrf51.svd')
    #dump_json(parser)
    interrupts = get_peripheral_interrupts(parser)
    dump_macros(interrupts,
            open("src/chips/nrf51822/peripheral_interrupts.h", "w"))
    peripherals = get_peripheral_registers(parser, ["GPIO", "TIMER0"])
    dump_registers(peripherals,
            open("src/chips/nrf51822/peripheral_registers.rs", "w"))

if __name__ == "__main__":
    main()
