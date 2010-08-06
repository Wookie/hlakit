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
from hlakit.common.conditional import Conditional as CommonConditional

class Conditional(CommonConditional):
    """
    This is the 6502 CPU specific implementation of the conditional block.
    Each CPU has to have its own because the thing that is tested is CPU
    specific.  For instance, a switch statement can switch only on a register
    value and the registers are CPU specific.
    """

    NEAR, FAR = range(2)
    NORMAL, NEGATED = range(2)
    A, X, Y = range(3)
    PLUS, POSITIVE, GREATER, MINUS, NEGATIVE, LESS, OVERFLOW, CARRY, NONZERO, \
    SET, TRUE, ONE, EQUAL, ZERO, FALSE, UNSET, CLEAR = range(17)

    conditions = { 'plus': PLUS,
                   'positive': POSITIVE,
                   'greater': GREATER,
                   'minus': MINUS,
                   'negative': NEGATIVE,
                   'less': LESS,
                   'overflow': OVERFLOW,
                   'carry': CARRY,
                   'nonzero': NONZERO,
                   'set': SET,
                   'true': TRUE,
                   'one': ONE,
                   '1': ONE,
                   'equal': EQUAL,
                   'zero': ZERO,
                   '0': ZERO,
                   'false': FALSE,
                   'unset': UNSET,
                   'clear': CLEAR }
    registers = { 'a': A,
                  'x': X,
                  'y': Y }
    distances = { 'near': NEAR,
                  'far': FAR }
    modifiers = { 'is': NORMAL,
                  'has': NORMAL,
                  'no': NEGATED,
                  'not': NEGATED }

    @classmethod
    def parse(klass, pstring, location, tokens):
        pp = Session().preprocessor()

        if pp.ignore():
            return []

        if 'if_' in tokens.keys():
           return klass(Conditional.IF, tokens.if_)

        if 'else_' in tokens.keys():
            return klass(Conditional.ELSE)

        if 'while_' in tokens.keys():
            return klass(Conditional.WHILE, tokens.while_)

        if 'do_' in tokens.keys():
            return klass(Conditional.DO)

        if 'forever_' in tokens.keys():
            return klass(Conditional.FOREVER)

        if 'switch_' in tokens.keys():
            return klass(Conditional.SWITCH, tokens.switch_)

        if 'case_' in tokens.keys():
            return klass(Conditional.CASE, tokens.case_)

        if 'default_' in tokens.keys():
            return klass(Conditional.DEFAULT)

        raise ParseFatalException('invalid conditional')

    @classmethod
    def _get_switch_registers(klass):
        regs = Optional(Suppress(CaselessLiteral('reg') + Literal('.'))) + \
               oneOf("a x y", True).setResultsName('register')
        return regs

    @classmethod
    def _get_conditions(klass):
        expr = Optional(Or([Keyword('near'), 
                            Keyword('far')])).setResultsName('distance') + \
               Optional(Or([Keyword('is'),
                            Keyword('has'),
                            Keyword('no'),
                            Keyword('not')])).setResultsName('modifier') + \
               Or([Keyword('plus'),
                   Keyword('positive'),
                   Keyword('greater'),
                   Keyword('minus'),
                   Keyword('negative'),
                   Keyword('less'),
                   Keyword('overflow'),
                   Keyword('carry'),
                   Keyword('nonzero'),
                   Keyword('set'),
                   Keyword('true'),
                   Keyword('1'),
                   Keyword('equal'),
                   Keyword('zero'),
                   Keyword('false'),
                   Keyword('unset'),
                   Keyword('clear'),
                   Keyword('0')]).setResultsName('condition')
        return expr

    def __init__(self, mode, cond=None):
        super(Conditional, self).__init__(mode, cond)

        self._distance = self.NEAR
        self._modifier = self.NORMAL
        self._condition = None

        # make sure the condition is a valid one
        if mode in (self.IF, self.WHILE):
            if 'condition' not in cond.keys():
                raise ParseFatalException('conditional is missing condition')
            if cond.condition.lower() not in self.conditions:
                raise ParseFatalException('invalid condition in conditional clause')
            self._condition = self.conditions[cond.condition.lower()]

            if 'modifier' in cond.keys():
                if cond.modifier.lower() not in self.modifiers:
                    raise ParseFatalException('invalid condition modifier')
                self._modifier = self.modifiers[cond.modifier.lower()]

            if 'distance' in cond.keys():
                if cond.distance.lower() not in self.distances:
                    raise ParseFatalException('invalid condition distance')
                self._distance = self.distances[cond.distance.lower()]

        elif mode == self.SWITCH:
            if 'register' not in cond.keys():
                raise ParseFatalException('switch statement can only take a register')
            self._condition = self.registers[cond.register.lower()]

        elif mode == self.CASE:
            if len(cond) != 1:
                raise ParseFatalException('case must take an immediate')
            self._condition = cond[0]


    def get_distance(self):
        return self._distance

    def get_modifier(self):
        return self._modifier

    def get_condition(self):
        return self._condition

