# -*- coding: utf-8 -*-
import os as _os
import binascii as _binascii
import re as _re
import numpy as _np


class DirectValue(object):
    def __init__(self, value=None, unhexlify=True):
        self.unhexlify = unhexlify
        self.value = self._check_value(value)

    def _check_value(self, input):
        """确认输入的曲线格式合法性"""
        if isinstance(input, str):
            # We expect a valid hexString
            if self.unhexlify:
                # A valid hexstring must have an even size
                if len(input) % 2 != 0:
                    raise ValueError("Odd-length string.")
                # and only the following subset of characters
                elif not _re.fullmatch(r"[0-9a-fA-F]*", input):
                    raise ValueError("Invalid character in input string.")
            # Any regular string is fine otherwise
        elif isinstance(input, list):
            try:
                bytes(input)
            except TypeError as t_err:
                raise TypeError(t_err)
        else:
            raise ValueError("Invalid value format %s. HexString without the '0x' prefix or a list of integer in range(0, 256) is expected." % type(input))

        return input

    def get_text(self, _):
        # User input is a string
        if isinstance(self.value, str):
            if self.unhexlify:
                return _binascii.unhexlify(self.value)
            else:
                return self.value
        # User input is an integer list
        elif isinstance(self.value, list):
            if self.unhexlify:
                return bytes(self.value)
            else:
                return str(self.value)


class HeaderExtractor(object):

    def __init__(self, start=None, end=None, count=None, unhexlify=True):
        self._check_and_set_boundaries(start, end, count)
        self.unhexlify = unhexlify

    def _check_and_set_boundaries(self, start, end, count):
        if start is not None:
            if end is None and count is None:
                raise ValueError("No 'end' offset or 'count' specified.")
            elif end is not None and count is not None:
                raise ValueError("Use either 'end' or 'count' option, not both.")
        else:
            raise ValueError("No 'start' offset specified.")

        if not isinstance(start, int) or start < 0:
            raise ValueError('offsets must be positive integer.')

        self.start = start

        if end is not None:
            if not isinstance(end, int) or end < 0:
                raise ValueError('offsets must be positive integer.')
            self.end = end
            self.count = self.end - self.start

        if count is not None:
            if not isinstance(count, int) or count < 0:
                raise ValueError('offsets must be positive integer.')
            self.count = count
            self.end = self.start + count

        if self.end <= self.start:
            raise ValueError('The end offset must be greater than the start offset.')

    def get_text(self, filename):
        file_size = _os.stat(filename).st_size
        if self.end > file_size:
            raise ValueError('%d is greater than file size (%d bytes)' % (self.end, file_size))
        file_pointer = _np.memmap(filename, dtype=_np.uint8, mode='r')
        data = _np.copy(file_pointer[self.start:self.end])
        del file_pointer

        if not self.unhexlify:
            return str("".join(hex(i)[2:] for i in data))
        else:
            return data.tobytes()

    def get_text_stacked(self, header):
        if self.end > len(header):
            raise ValueError('%d is greater than header size (%d bytes).' % (self.end, len(header)))
        data = _np.copy(header[self.start:self.end])

        if not self.unhexlify:
            return str("".join(hex(i)[2:] for i in data))
        else:
            return data.tobytes()


class PatternExtractor(object):
    def __init__(self, pattern=None, replace=None, num=0, unhexlify=True):
        self.pattern = _re.compile(pattern)
        self.replace = replace
        self.num = num
        self.unhexlify = unhexlify

    def get_pattern(self, string):
        string = string.rstrip()
        if self.replace:
            string = self.pattern.sub(self.replace, string)
        elif self.num is not None:
            try:
                string = self.pattern.findall(string)[self.num]
            except IndexError:
                raise ValueError("Pattern '%s' not found in '%s'." % (self.pattern.pattern, string))
        if self.unhexlify:
            string = _binascii.unhexlify(string)
        return string

    def get_text(self, filename):
        return self.get_pattern(self.get_value(filename))

    def get_value(self, filename):
        # FIXME: What is the purpose of this function ?
        return filename


class FilePatternExtractor(PatternExtractor):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = self._check_filename(filename)
        self._iter = self.text_generator(filename)
        self._fixed_value = None

    def _check_filename(self, filename):
        if _os.path.isfile(filename):
            return filename
        else:
            raise FileNotFoundError("'%s' not found" % filename)

    def text_generator(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            if len(lines) > 1:
                for m in lines:
                    yield m
            else:
                self._fixed_value = lines[0]
                yield lines[0]

    def get_value(self, filename):
        if self._fixed_value:
            return self._fixed_value
        else:
            return next(self._iter)
