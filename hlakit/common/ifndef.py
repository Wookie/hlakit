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

class Ifndef(object):
    """
    This defines the rules for parsing a #ifndef <symbol> line in a file
    """

    @classmethod
    def parse(klass, pstring, location, tokens):
        pp = Session().preprocessor()

        # the top of the ignore stack is None if we're nested inside
        # of an ignored block of code.  we have to push another None
        # on the stack to track our nesting
        if pp.ignore():
            pp.ignore_stack_push(None)
            return []

        # check to see if we should turn ignore on
        if pp.has_symbol(tokens.label):
            pp.ignore_stack_push(True)
        else:
            pp.ignore_stack_push(False)

        return []

    @classmethod
    def exprs(klass):
        ifndef = Keyword('#ifndef')
        label = Word(alphas + '_', alphanums + '_').setResultsName('label')

        expr = Suppress(ifndef) + \
               label + \
               Suppress(LineEnd())
        expr.setParseAction(klass.parse)

        return expr

