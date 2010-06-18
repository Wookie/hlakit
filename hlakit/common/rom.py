"""
HLAKit
Copyright (c) 2010 David Huseby. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY DAVID HUSEBY ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DAVID HUSEBY OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of David Huseby.
"""

from pyparsing import *
from hlakit.common.session import Session
from hlakit.common.numericvalue import NumericValue

class RomOrg(object):
    """
    This defines the rules for parsing a #rom.org <blockaddress>[,maxsize] line 
    in a file
    """

    @classmethod
    def parse(klass, pstring, location, tokens):
        pp = Session().preprocessor()

        if pp.ignore():
            return []

        if not hasattr(tokens, 'address'):
            raise ParseFatalException('#rom.org without an address')

        maxsize = getattr(tokens, 'maxsize', None)

        return klass(tokens.address, maxsize)

    @classmethod
    def exprs(klass):
        romorg = Keyword('#rom.org')
        address = NumericValue.exprs().setResultsName('address')
        maxsize = NumericValue.exprs().setResultsName('maxsize')

        expr = Suppress(romorg) + \
               address + \
               Optional(Literal(',') + maxsize) + \
               Suppress(LineEnd())
        expr.setParseAction(klass.parse)

        return expr

    def __init__(self, address, maxsize=None):
        self._address = address
        self._maxsize = maxsize

    def get_address(self):
        return self._address

    def get_maxsize(self):
        return self._maxsize

    def __str__(self):
        s = "RomOrg <0x%x>" % self._address
        if self._maxsize:
            s += ',<0x%x>' % self._maxsize
        return s

    __repr__ = __str__


class RomEnd(object):
    """
    This defines the rules for parsing a #rom.end line in a file
    """

    @classmethod
    def parse(klass, pstring, location, tokens):
        pp = Session().preprocessor()

        if pp.ignore():
            return []

        return klass()

    @classmethod
    def exprs(klass):
        romend = Keyword('#rom.end')
        expr = Suppress(romend) + \
               Suppress(LineEnd())
        expr.setParseAction(klass.parse)

        return expr

    def __str__(self):
        return 'RomEnd'

    __repr__ = __str__

class RomBanksize(object):
    """
    This defines the rules for parsing a #rom.banksize <size> line in a file
    """

    @classmethod
    def parse(klass, pstring, location, tokens):
        pp = Session().preprocessor()

        if pp.ignore():
            return []

        if not hasattr(tokens, 'size'):
            raise ParseFatalException('#rom.banksize without a size')

        return klass(tokens.size)

    @classmethod
    def exprs(klass):
        rombanksize = Keyword('#rom.banksize')
        size = NumericValue.exprs().setResultsName('size')

        expr = Suppress(rombanksize) + \
               size + \
               Suppress(LineEnd())
        expr.setParseAction(klass.parse)

        return expr

    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def __str__(self):
        return "RomBanksize <0x%x>" % self._size

    __repr__ = __str__

class RomBank(object):
    """
    This defines the rules for parsing a #rom.bank <blocknumber>[,maxsize] line 
    in a file
    """

    @classmethod
    def parse(klass, pstring, location, tokens):
        pp = Session().preprocessor()

        if pp.ignore():
            return []

        if not hasattr(tokens, 'number'):
            raise ParseFatalException('#rom.bank without a number')

        maxsize = getattr(tokens, 'maxsize', None)

        return klass(tokens.number, maxsize)

    @classmethod
    def exprs(klass):
        rombank = Keyword('#rom.bank')
        number = NumericValue.exprs().setResultsName('number')
        maxsize = NumericValue.exprs().setResultsName('maxsize')

        expr = Suppress(rombank) + \
               number + \
               Optional(Literal(',') + maxsize) + \
               Suppress(LineEnd())
        expr.setParseAction(klass.parse)

        return expr

    def __init__(self, number, maxsize=None):
        self._number = number
        self._maxsize = maxsize

    def get_number(self):
        return self._number

    def get_maxsize(self):
        return self._maxsize

    def __str__(self):
        s = "RomBank %s" % self._number
        if self._maxsize:
            s += ',<0x%x>' % self._maxsize
        return s

    __repr__ = __str__



