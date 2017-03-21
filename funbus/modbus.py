
import enum

from collections import namedtuple
from pprint import pformat


# containers for declarative Modbus protocol specification
FramePart = namedtuple("FramePart", "size description")
FunctionCode = namedtuple("FunctionCode", "code action description")


class ModbusEnumMeta(enum.EnumMeta):
    """Our Modbus enum metaclass with a special __repr__ so
    that Modbus functions can be more easily investigated from the shell"""

    def __repr__(self):
        return pformat(dict(self.__members__))


class ModbusEnum(enum.Enum, metaclass=ModbusEnumMeta):
    """Our modbus enum base class with custom metaclass
    and a hash that is based on the *values*, not names of members.
    The reason this is desirable is so that we can subdivide the Modbus
    functions into multiple Enum objects and have repeated members
    from both get hashed the same way."""

    def __hash__(self):
        return hash(self._value_)


class TcpFrame(FramePart, ModbusEnum):
    """Parts of a Modbus TCP frame"""
    transaction = 2, "transaction identfier"
    protocol = 2, "protocol identifier"
    length = 2, "length"
    unit = 1, "slave address"
    function = 1, "function code"
    data = 0, "data bytes"


class Action(enum.Flag):
    read = enum.auto()
    write = enum.auto()
    readwrite = read | write
    misc = enum.auto()


# for convenience in specifying Function members
READ, WRITE, READWRITE, MISC = Action


class Function(FunctionCode, ModbusEnum):
    """All Modbus function codes"""
    read_discrete_inputs =  2, READ, "read discrete/physical inputs"
    read_coils =            1, READ, "read coils/bits"
    write_single_coil =     5, WRITE, "write single coil"
    write_coils =          15, WRITE, "write multiple coils"
    read_input =            4, READ, "read input registers"
    read_holding =          3, READ, "read multiple holding registers"
    write_single_holding =  6, WRITE, "write single holding register"
    write_holding =        16, WRITE, "write multiple holding registers"
    read_write =           23, READWRITE, "read/write multiple registers"
    mask_write =           22, WRITE, "mask write register"
    read_fifo =            24, READ, "read FIFO queue"
    read_file_record =     20, READ, "read file record"
    write_file_record =    21, WRITE, "write file record"
    exception_status =      7, MISC, "read exception status"
    diagnostic =            8, MISC, "diagnostic"
    com_counter =          11, MISC, "get com event counter"
    com_log =              12, MISC, "get com event log"
    report_slave =         17, MISC, "report slave identifier"
    read_id =              43, MISC, "read device identifier"


code_map = {fn.code: fn for fn in Function}


class Coil(ModbusEnum):
    read = Function.read_coils
    write_single = Function.write_single_coil
    write = Function.write_coils


class Holding(ModbusEnum):
    write_single = Function.write_single_holding
    write = Function.write_holding
    read = Function.read_holding


class Diagnostic(ModbusEnum):
    exception_status = Function.exception_status
    diagnostic = Function.diagnostic
    com_counter = Function.com_counter
    com_log = Function.com_log
    report_slave = Function.report_slave
    read_id = Function.read_id

