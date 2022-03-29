# IO Lib 2.0 by bqio
from struct import pack, unpack


class MemoryReader:
    """
    Simple memory reader.
    """

    def __init__(self, buffer: bytes, e="<") -> None:
        self.buffer = buffer
        self.e = e
        self.offset = 0

    def read(self, count: int) -> bytes:
        """
        Read bytes from buffer.
        """
        buf = self.buffer[self.offset:self.offset + count]
        self.offset += count
        return buf

    def read_8(self) -> int:
        """
        Read 8-bit signed integer from buffer.
        """
        buf = self.read(1)
        return unpack(self.e + "b", buf)[0]

    def read_16(self) -> int:
        """
        Read 16-bit signed integer from buffer.
        """
        buf = self.read(2)
        return unpack(self.e + "h", buf)[0]

    def read_32(self) -> int:
        """
        Read 32-bit signed integer from buffer.
        """
        buf = self.read(4)
        return unpack(self.e + "i", buf)[0]

    def read_64(self) -> int:
        """
        Read 64-bit signed integer from buffer.
        """
        buf = self.read(8)
        return unpack(self.e + "q", buf)[0]

    def read_u8(self) -> int:
        """
        Read 8-bit unsigned integer from buffer.
        """
        buf = self.read(1)
        return unpack(self.e + "B", buf)[0]

    def read_u16(self) -> int:
        """
        Read 16-bit unsigned integer from buffer.
        """
        buf = self.read(2)
        return unpack(self.e + "H", buf)[0]

    def read_u32(self) -> int:
        """
        Read 32-bit unsigned integer from buffer.
        """
        buf = self.read(4)
        return unpack(self.e + "I", buf)[0]

    def read_u64(self) -> int:
        """
        Read 64-bit unsigned integer from buffer.
        """
        buf = self.read(8)
        return unpack(self.e + "Q", buf)[0]

    def read_str(self, size: int) -> str:
        """
        Read UTF-8 string from buffer.
        """
        return self.read(size).decode('utf-8')

    def read_str_xor(self, size: int, xor: int) -> str:
        """
        Read UTF-8 XOR string from buffer.
        """
        return bytes(list(map(lambda n: n ^ xor, list(self.read(size))))).decode('utf-8')

    def read_null_str(self, terminator: int = 0) -> str:
        """
        Read UTF-8 null terminated string from buffer.
        """
        length = 0
        pos = self.tell()
        while self.read_8() != terminator:
            length += 1
        self.seek(pos)
        line = self.read_str(length)
        self.skip(1)
        return line

    def seek(self, offset: int):
        """
        Set offset in buffer.
        """
        self.offset = offset

    def tell(self):
        """
        Get offset in buffer.
        """
        return self.offset

    def skip(self, count: int):
        """
        Skip bytes in buffer.
        """
        self.seek(self.tell() + count)


class MemoryWriter:
    """
    Simple memory writer.
    """

    def __init__(self, e="<"):
        self.e = e
        self.buffer = bytes()

    def write(self, data: bytes) -> None:
        """
        Write bytes into buffer.
        """
        self.buffer += data

    def write_8(self, data: int) -> None:
        """
        Write 8-bit signed integer into buffer.
        """
        buf = pack(self.e + "b", data)
        self.write(buf)

    def write_16(self, data: int) -> None:
        """
        Write 16-bit signed integer into buffer.
        """
        buf = pack(self.e + "h", data)
        self.write(buf)

    def write_32(self, data: int) -> None:
        """
        Write 32-bit signed integer into buffer.
        """
        buf = pack(self.e + "i", data)
        self.write(buf)

    def write_64(self, data: int) -> None:
        """
        Write 64-bit signed integer into buffer.
        """
        buf = pack(self.e + "q", data)
        self.write(buf)

    def write_u8(self, data: int) -> None:
        """
        Write 8-bit unsigned integer into buffer.
        """
        buf = pack(self.e + "B", data)
        self.write(buf)

    def write_u16(self, data: int) -> None:
        """
        Write 16-bit unsigned integer into buffer.
        """
        buf = pack(self.e + "H", data)
        self.write(buf)

    def write_u32(self, data: int) -> None:
        """
        Write 32-bit unsigned integer into buffer.
        """
        buf = pack(self.e + "I", data)
        self.write(buf)

    def write_u64(self, data: int) -> None:
        """
        Write 64-bit unsigned integer into buffer.
        """
        buf = pack(self.e + "Q", data)
        self.write(buf)

    def write_str(self, data: str) -> None:
        """
        Write UTF-8 string into buffer.
        """
        buf = data.encode('utf-8')
        self.write(buf)

    def write_null_str(self, data: str) -> None:
        """
        Write UTF-8 string with null terminated byte into buffer.
        """
        buf = data.encode('utf-8')
        self.write(buf)
        self.write_8(0)


class Writer:
    """
    Simple writer class.
    """

    def __init__(self, f, e="<") -> None:
        self.f = f
        self.e = e

    @staticmethod
    def into_file(filename, buffer: bytes) -> None:
        """
        Write buffer into file.
        """
        with open(filename, "wb") as f:
            f.write(buffer)

    def close(self) -> None:
        """
        Close writer.
        """
        self.f.close()

    def write(self, buf: bytes) -> None:
        """
        Write bytes into buffer.
        """
        self.f.write(buf)

    def write_8(self, data: int) -> None:
        """
        Write 8-bit signed integer into buffer.
        """
        buf = pack(self.e + "b", data)
        self.write(buf)

    def write_16(self, data: int) -> None:
        """
        Write 16-bit signed integer into buffer.
        """
        buf = pack(self.e + "h", data)
        self.write(buf)

    def write_32(self, data: int) -> None:
        """
        Write 32-bit signed integer into buffer.
        """
        buf = pack(self.e + "i", data)
        self.write(buf)

    def write_64(self, data: int) -> None:
        """
        Write 64-bit signed integer into buffer.
        """
        buf = pack(self.e + "q", data)
        self.write(buf)

    def write_u8(self, data: int) -> None:
        """
        Write 8-bit unsigned integer into buffer.
        """
        buf = pack(self.e + "B", data)
        self.write(buf)

    def write_u16(self, data: int) -> None:
        """
        Write 16-bit unsigned integer into buffer.
        """
        buf = pack(self.e + "H", data)
        self.write(buf)

    def write_u32(self, data: int) -> None:
        """
        Write 32-bit unsigned integer into buffer.
        """
        buf = pack(self.e + "I", data)
        self.write(buf)

    def write_u64(self, data: int) -> None:
        """
        Write 64-bit unsigned integer into buffer.
        """
        buf = pack(self.e + "Q", data)
        self.write(buf)

    def write_str(self, data: str) -> None:
        """
        Write UTF-8 string into buffer.
        """
        buf = data.encode('utf-8')
        self.write(buf)

    def write_null_str(self, data: str) -> None:
        """
        Write UTF-8 string with null terminated byte into buffer.
        """
        buf = data.encode('utf-8')
        self.write(buf)
        self.write_8(0)

    def skip(self, count: int) -> None:
        """
        Skip (fill) bytes in buffer.
        """
        for _ in range(count):
            self.write_8(0)

    def seek(self, offset: int) -> None:
        """
        Set offset in buffer.
        """
        self.f.seek(offset)

    def tell(self) -> int:
        """
        Get offset from buffer.
        """
        return self.f.tell()


class Reader:
    """
    Simple memory reader.
    """

    def __init__(self, f, e="<") -> None:
        self.f = f
        self.e = e

    def close(self) -> None:
        """
        Close reader.
        """
        self.f.close()

    def read(self, count: int) -> bytes:
        """
        Read bytes from buffer.
        """
        return self.f.read(count)

    def read_8(self) -> int:
        """
        Read 8-bit signed integer from buffer.
        """
        buf = self.read(1)
        return unpack(self.e + "b", buf)[0]

    def read_16(self) -> int:
        """
        Read 16-bit signed integer from buffer.
        """
        buf = self.read(2)
        return unpack(self.e + "h", buf)[0]

    def read_32(self) -> int:
        """
        Read 32-bit signed integer from buffer.
        """
        buf = self.read(4)
        return unpack(self.e + "i", buf)[0]

    def read_64(self) -> int:
        """
        Read 64-bit signed integer from buffer.
        """
        buf = self.read(8)
        return unpack(self.e + "q", buf)[0]

    def read_u8(self) -> int:
        """
        Read 8-bit unsigned integer from buffer.
        """
        buf = self.read(1)
        return unpack(self.e + "B", buf)[0]

    def read_u16(self) -> int:
        """
        Read 16-bit unsigned integer from buffer.
        """
        buf = self.f.read(2)
        return unpack(self.e + "H", buf)[0]

    def read_u32(self) -> int:
        """
        Read 32-bit unsigned integer from buffer.
        """
        buf = self.read(4)
        return unpack(self.e + "I", buf)[0]

    def read_u64(self) -> int:
        """
        Read 64-bit unsigned integer from buffer.
        """
        buf = self.read(8)
        return unpack(self.e + "Q", buf)[0]

    def read_str(self, size) -> str:
        """
        Read UTF-8 string from buffer.
        """
        return self.read(size).decode('utf-8')

    def read_str_xor(self, size, xor) -> str:
        """
        Read UTF-8 XOR string from buffer.
        """
        return bytes(list(map(lambda n: n ^ xor, list(self.read(size))))).decode('utf-8')

    def read_null_str(self, terminator: int = 0) -> str:
        """
        Read UTF-8 null terminated string from buffer.
        """
        length = 0
        pos = self.tell()
        while self.read_8() != terminator:
            length += 1
        self.seek(pos)
        line = self.read_str(length)
        self.skip(1)
        return line

    def seek(self, offset: int) -> None:
        """
        Set offset in buffer.
        """
        self.f.seek(offset)

    def tell(self) -> int:
        """
        Get offset from buffer.
        """
        return self.f.tell()

    def skip(self, count: int) -> None:
        """
        Skip bytes in buffer.
        """
        self.seek(self.tell() + count)
