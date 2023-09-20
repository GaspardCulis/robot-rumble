# Host player
# Other players send the position they are at (they calculate their own physics)
# Host sends world items physics and counts hits between them
# WARNING !!!! This system is VERY vulnerable to cheating ! but has the advantage of not having desyncs

# These packets will be sent over UDP, with NO CONFIRMATION
# (except for initial connections, three-way handshake, similar to TCP)
# If a movement packet is lost, the updated version will be sent soon enough after

# movement packet is sent like every frame (1/60 or 1/120 depending on fps, vsync advantage ? yes but I don't care)
# server will send position of every item (except the player that receives that info)

# Client will still run the physics simulations for everything, except corrected for server data (interpolate ?)

# ------------- Data Types ------------
# VarInt a 32bit encoded in the lowest amount of space it fits in
# (most significant bit used to say if there is another byte in the int)
# VarLong same but 64bit

# ------------- Packets List ----------
# Packet is UDP data <packet id : VarInt (in practice, just works as a byte)> <last_id VarLong> <packet data>
# last id is an integer that MUST increase after every packet
# if you receive a packet with a lower last_id then last obtained then it's assumed out of order and SHOULD be dropped
# C->S Client to server
# C<-S Server to client
# C<=>S Can be sent both ways

# FOR HANDSHAKE
# un-answered packets need to be resent frequently (once every 2s ? or more)
# after handshake, receiving no packets for 10s will be considered a timeout


# Handshake
# C->S  0x01 id
# C<-S  0x02 id
# C->S  0x03 id

# KEEPALIVE packet
# In situations where no packet was sent for 1s, you can send a KEEPALIVE PACKET
# This packet is a NOOP except it resets the timeout timer
# C<=>S 0x00 id 0x00

# IN PLAY STATE
# C->S 0x04 id <DATA ABOUT PLAYER>
# C<-S 0x05 id <ARRAY OF OBJECTS AND STATES>

from typing import TypeAlias, Any
import struct
from pygame import Vector2

Address: TypeAlias = tuple[str | Any, int]


class DataConverter:
    def __init__(self):
        raise NotImplementedError  # DataConverter is not to be initialized

    @staticmethod
    def write_vector_float(vector: Vector2) -> bytes:
        return DataConverter.write_float(vector.x) + DataConverter.write_float(vector.y)

    @staticmethod
    def parse_vector_float(data: bytes) -> Vector2:
        return Vector2(DataConverter.parse_float(data), DataConverter.parse_float(data[struct.calcsize(">d"):]))

    @staticmethod
    def write_vector_int(vector: Vector2) -> bytes:
        return DataConverter.write_varint(vector.x) + DataConverter.write_varint(vector.y)

    @staticmethod  # bytesused,vector
    def parse_vector_int(data: bytes) -> tuple[int, Vector2]:
        used, first = DataConverter.parse_varint(data)
        used2, second = DataConverter.parse_varint(data[used:])
        return used + used2, Vector2(first, second)

    @staticmethod  # will return 8 bytes
    def write_float(nb: float) -> bytes:
        return struct.pack(">d", nb)

    @staticmethod  # will use 8 bytes
    def parse_float(data: bytes) -> float:
        return struct.unpack(">d", data[:struct.calcsize(">d")])[0]

    @staticmethod  # tuple is (bytesused,value)
    def parse_varlong(data: bytes) -> tuple[int, int]:
        val = 0
        pos = 0
        current: int
        while True:
            current = data[0]
            data = data[1:]
            val |= (current & 0x7F) << pos
            if current & 0x80 == 0:
                break
            pos += 7
            if pos >= 64:
                raise IndexError("VarLong too big !")
        return int(pos / 7) + 1, val

    @staticmethod  # tuple is (bytesused,value)
    def parse_varint(data: bytes) -> tuple[int, int]:
        val = 0
        pos = 0
        current: int
        while True:
            current = data[0]
            data = data[1:]
            val |= (current & 0x7F) << pos
            if current & 0x80 == 0:
                break
            pos += 7
            if pos >= 32:
                raise IndexError("VarLong too big !")
        return int(pos / 7) + 1, val

    @staticmethod
    def write_varint(number: int) -> bytes:
        number = number & 0xFFFF_FFFF  # limit to 32 bits
        output = bytearray()
        while True:
            if (number & ~0x7F) == 0:
                output.append(number)
                return bytes(output)
            output.append((number & 0x7F) | 0x80)
            number >>= 7

    @staticmethod
    def write_varlong(number: int) -> bytes:
        number = number & 0xFFFF_FFFF_FFFF_FFFF  # limit to 64 bits
        output = bytearray()
        while True:
            if (number & ~0x7F) == 0:
                output.append(number)
                return bytes(output)
            output.append((number & 0x7F) | 0x80)
            number >>= 7
