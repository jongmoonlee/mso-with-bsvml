from ctypes import *
import platform
import os

lib_ext = ""
if os.name == 'nt':
    lib_ext = "dll"
elif platform.system() == "Linux":
    lib_ext = "so"
else:
    exit("OS not supported.")

cdll.LoadLibrary("libbsvml." + lib_ext)
bvl = CDLL("libbsvml." + lib_ext)

# MODE
SINGLE               = 0
DUAL                 = 1
LOGIC                = 2
MIXED_SINGLE         = 3
MIXED_DUAL           = 4
STREAM_SINGLE        = 5
STREAM_DUAL          = 6
STREAM_LOGIC         = 7
STREAM_MIXED_SINGLE  = 8
STREAM_MIXED_DUAL    = 9

# TRIGTYPE
SALT = 0
COMP = 1

# CHANNELS
CHA = 0
CHB = 1
CHL = 128

# LOGICCHANNELS
L0 = 128
L1 = 129
L2 = 130
L3 = 131
L4 = 132
L5 = 133
L6 = 134
L7 = 135

# TRACECODES
DONE = 0
AUTO = 1
WAIT = 2
STOP = 3

# STATUS
IDLE      = 0
STREAMING = 1
TRACING   = 2
UPDATING  = 3
DISCONNECTED = 4

# TRIGLOGIC
FALL = 0
RISE = 1

# GEN FUNCTION
SINE        = 0
TRIANGLE    = 1
EXPONENTIAL = 2
SQUARE      = 3
ARBITRARY   = 4

# BitScopeInfo Struct

class BitScopeInfo(Structure):
    _fields_ = [
        ("port",  c_char_p),
        ("model", c_char_p),
        ("uid",   c_char_p)
    ]

# State
mode     = bvl.bv_mode
rate     = bvl.bv_rate
dumpSize = bvl.bv_dumpSize
address  = bvl.bv_address
enableAnalogueChannel  = bvl.bv_enableAnalogueChannel
disableAnalogueChannel = bvl.bv_disableAnalogueChannel
dumpChannel  = bvl.bv_dumpChannel
range        = bvl.bv_range
offset       = bvl.bv_offset
macro        = bvl.bv_macro
unifiedDump  = bvl.bv_unifiedDump
traceIntro   = bvl.bv_traceIntro
traceOutro   = bvl.bv_traceOutro
traceDelay   = bvl.bv_traceDelay
traceTimeout = bvl.bv_traceTimeout
trigSource   = bvl.bv_trigSource
trigSwap     = bvl.bv_trigSwap
trigType     = bvl.bv_trigType
trigChannelEnable = bvl.bv_trigChannelEnable
trigChannelEdge   = bvl.bv_trigChannelEdge
trigIntro = bvl.bv_trigIntro
trigOutro = bvl.bv_trigOutro
trigValue = bvl.bv_trigValue
trigLevel = bvl.bv_trigLevel

# Exec
openBitScope   = bvl.bv_openBitScope
closeBitScope  = bvl.bv_closeBitScope
updateBitScope = bvl.bv_updateBitScope
trace          = bvl.bv_trace
asyncTrace     = bvl.bv_asyncTrace
acquire        = bvl.bv_acquire
stream         = bvl.bv_stream
streamAcquire  = bvl.bv_streamAcquire
cancel         = bvl.bv_cancel
wait           = bvl.bv_wait

# Helpers
getBitScopeInfo      = bvl.bv_getBitScopeInfo
getStartAddress      = bvl.bv_getStartAddress
getIntroStartAddress = bvl.bv_getIntroStartAddress
getBytesInDump       = bvl.bv_getBytesInDump
listBitScopes        = bvl.bv_listBitScopes
getMinTimeout        = bvl.bv_getMinTimeout
getStatus            = bvl.bv_getStatus
getTraceCode         = bvl.bv_getTraceCode

# Dump convertors
convertMacroTrace      = bvl.bv_convertMacroTrace
convertMacroStream     = bvl.bv_convertMacroStream
splitDualStream        = bvl.bv_splitDualStream
splitDualMixedStream   = bvl.bv_splitDualMixedStream
splitSingleMixedStream = bvl.bv_splitSingleMixedStream
splitDualTrace         = bvl.bv_splitDualTrace
splitDualMixedTrace    = bvl.bv_splitDualMixedTrace
splitSingleMixedTrace  = bvl.bv_splitSingleMixedTrace

# AWG
genFunction   = bvl.bv_genFunction
genRate       = bvl.bv_genRate
genSymmetry   = bvl.bv_genSymmetry
genLevel      = bvl.bv_genLevel
genOffset     = bvl.bv_genOffset
genSize       = bvl.bv_genSize
genAddress    = bvl.bv_genAddress
writeWaveData = bvl.bv_writeWaveData
updateAWG     = bvl.bv_updateAWG

# Serial passthrough
write = bvl.bv_write
read  = bvl.bv_read

# Type information

mode.argtypes = [c_int]
mode.restype  = c_int

rate.argtypes = [c_int, c_double]
rate.restype  = c_double

dumpSize.argtypes = [c_int, c_int]
dumpSize.restype  = c_int

enableAnalogueChannel.argtypes = [c_int, c_int]
enableAnalogueChannel.restype  = c_bool

disableAnalogueChannel.argtypes = [c_int, c_int]
disableAnalogueChannel.restype  = c_bool

dumpChannel.argtypes = [c_int, c_int]
dumpChannel.restypes = c_int

range.argtypes = [c_int, c_float]
range.restype  = c_float

offset.argtypes = [c_int, c_float]
offset.restype  = c_float

macro.argtypes = [c_int, c_bool]
macro.restype  = c_bool

unifiedDump.argTypes = [c_int, c_bool]
unifiedDump.restype  = c_bool

traceIntro.argtypes = [c_int, c_int]
traceIntro.restype  = c_int

traceOutro.argtypes = [c_int, c_int]
traceOutro.restype  = c_int

traceDelay.argtypes = [c_int, c_float]
traceDelay.restype  = c_float

traceTimeout.argtypes = [c_int, c_float]
traceTimeout.restype  = c_float

trigSource.argtypes = [c_int, c_int]
trigSource.restype  = c_int

trigSwap.argtypes = [c_int, c_bool]
trigSwap.restype  = c_bool

trigType.argtypes = [c_int, c_bool]
trigType.restype  = c_bool

trigChannelEnable.argTypes = [c_int, c_int, c_bool]
trigChannelEnable.restype  = c_bool

trigChannelEdge.argtypes = [c_int, c_int, c_bool]
trigChannelEdge.restype  = c_bool

trigIntro.argtypes = [c_int, c_int]
trigIntro.restype  = c_int

trigOutro.argtypes = [c_int, c_int]
trigOutro.restype  = c_int

trigLevel.argtypes = [c_int, c_float]
trigLevel.restype  = c_float

trigValue.argtypes = [c_int, c_float]
trigValue.restype  = c_float

openBitScope.argtypes = [c_char_p]
openBitScope.restype  = c_int

closeBitScope.argtypes = [c_int]

updateBitScope.argtypes = [c_int]
updateBitScope.restype  = c_bool

trace.argtypes = [c_int]
trace.restype  = c_bool

asyncTrace.argtypes = [c_int]
asyncTrace.restype  = c_bool

acquire.argtypes = [c_int, POINTER(c_ubyte)]
acquire.restype  = c_bool

stream.argtypes = [c_int]
stream.restype  = c_bool

streamAcquire.argtypes = [c_int, POINTER(c_ubyte)]
streamAcquire.restype  = c_bool

cancel.argtypes = [c_int]
cancel.restype  = c_bool

wait.argtypes = [c_int]
wait.restype  = c_bool

getBitScopeInfo.argtypes = [c_int]
getBitScopeInfo.restype  = BitScopeInfo

getStartAddress.argtypes = [c_int]
getStartAddress.restype  = c_int

getIntroStartAddress.argtypes = [c_int]
getIntroStartAddress.restype  = c_int

getBytesInDump.argtypes = [c_int]
getBytesInDump.restype  = c_int

listBitScopes.argtypes = [c_int, POINTER(BitScopeInfo)]
listBitScopes.restype  = c_int

getMinTimeout.argtypes = [c_int]
getMinTimeout.restype  = c_float

getStatus.argtypes = [c_int]
getStatus.restype  = c_int

getTraceCode.argtypes = [c_int]
getTraceCode.restype  = c_int

convertMacroTrace.argtypes = [POINTER(c_ubyte), POINTER(c_short), c_int]

convertMacroStream.argtypes = [POINTER(c_ubyte), POINTER(c_short), c_int]

splitDualStream.argtypes = [
    POINTER(c_ubyte), POINTER(c_ubyte),
    POINTER(c_ubyte), c_int, c_bool]

splitDualMixedStream.argtypes = [
    POINTER(c_ubyte), POINTER(c_ubyte),
    POINTER(c_ubyte), POINTER(c_ubyte),
    c_int]

splitSingleMixedStream.argtypes = [
    POINTER(c_ubyte), POINTER(c_ubyte),
    POINTER(c_ubyte), c_int]

splitDualTrace.argtypes = [
    POINTER(c_ubyte), POINTER(c_ubyte),
    POINTER(c_ubyte), c_int, c_bool]

splitDualMixedTrace.argtypes = [
    POINTER(c_ubyte), POINTER(c_ubyte),
    POINTER(c_ubyte), POINTER(c_ubyte), c_int]

splitSingleMixedTrace.argtypes = [
    POINTER(c_ubyte), POINTER(c_ubyte),
    POINTER(c_ubyte), c_int]

genFunction.argtypes = [c_int, c_int]
genFunction.restype  = c_int

genRate.argtypes = [c_int, c_float]
genRate.restype  = c_float

genSymmetry.argtypes = [c_int, c_float]
genSymmetry.restype  = c_float

genLevel.argtypes = [c_int, c_float]
genLevel.restype  = c_float

genOffset.argtypes = [c_int, c_float]
genOffset.restype  = c_float

genSize.argtypes = [c_int, c_int]
genSize.restype  = c_int

genAddress.argtypes = [c_int, c_int]
genAddress.restype  = c_int

writeWaveData.argtypes = [c_int, POINTER(c_ubyte), c_int]

updateAWG.argtypes = [c_int]
updateAWG.restype  = c_bool

write.argtypes = [c_int, c_char_p, c_int]
write.restype  = c_int

read.argtypes = [c_int, c_char_p, c_int, c_int]
read.restype  = c_int
