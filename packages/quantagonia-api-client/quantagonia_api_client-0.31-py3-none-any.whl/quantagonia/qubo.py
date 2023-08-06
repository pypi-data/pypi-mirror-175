import os, os.path
from pydoc import classname
import readline
THIS_SCRIPT = os.path.dirname(os.path.realpath(__file__))

from enum import Enum
from distutils.log import error, warn
from logging import warning
from pickletools import optimize
import sys
from typing import List, Dict
import warnings
import re
import tempfile
import subprocess
import json
import copy
import gzip

import pyqubo as pq

from pulp import PulpSolverError
from quantagonia.enums import HybridSolverConnectionType, HybridSolverServers

from quantagonia.runner import Runner
from quantagonia.runner_factory import RunnerFactory
from quantagonia.spec_builder import QUBOSpecBuilder, QuboSolverType

class QuboVariable(object):

    def __init__(self, name : str, pos : int, initial=None, fixing=None):
        self.name = name
        self._pos = pos
        if initial and initial not in [0, 1]:
            warnings.warn(f"Initial variable value {initial} not binary. Ignore initial assignment.")
            initial=None
        if fixing and fixing not in [0, 1]:
            warnings.warn(f"Fixing variable value {fixing} not binary. Ignore fixing.")
            initial=None
        if initial and fixing and initial != fixing:
            warnings.warn("Initial != fixing, discard initial and use fixing")
            initial = fixing
        self.fixing = fixing
        self.__assignment = initial

    @property
    def assignment(self):
        return self.__assignment

    @assignment.setter
    def assignment(self, value):
        # check against fixing
        if self.fixing and self.fixing != value:
            error(f"Assigning {value} to {self.name} contradicts fixing {self.fixing}")
        self.__assignment = value

    def id(self):
        return self._pos

    def eval(self):
        if(self.assignment is None):
            error("Variable " + self.name + " is still unassigned.")
        return self.assignment

    def __str__(self):
        return self.name

    def key(self):
        return str(self)

    def __mul__(self, other):
        return QuboTerm(1, [self, other])

    def __rmul__(self, other : float):
        return QuboTerm(other, [self])

class QuboTerm(object):

    def __init__(self, coefficient : float, vars : list):
        super().__init__()
        self.coefficient = coefficient
        self.order = len(vars)
        self.vars = vars

        if(self.order < 1 or self.order > 2):
            raise Exception("Only QuboTerms of order 1 or 2 are supported!")

        # by convention, we only store the upper triangular part of the QUBO ->
        # need to sort the variables ascendingly by their IDs
        sorted(self.vars, key = lambda v : v.id())

    def eval(self):
        E = self.coefficient * self.vars[0].eval()

        for var in self.vars[1:]:
            E *= var.eval()

        return E

    def __str__(self):
        s = ""
        if(self.coefficient >= 0):
            s += "+ "
        else:
            s += "- "

        s += str(abs(self.coefficient))
        s += " * " + str(self.vars[0])
        for var in self.vars[1:]:
            s += " * " + str(var)

        return s

    def key(self):
        return "_".join([str(v) for v in self.vars])

    # Python 3.10: other: float | QuboVariable
    def __mul__(self, other):
        if isinstance(other, float):
            self.coefficient *= other
            return self

        if(self.order <= 1):
            return QuboTerm(self.coefficient, [*self.vars, other])

        raise Exception("Only QuboTerms of order 1 or 2 are supported!")

    # Python 3.10: other: float | QuboVariable
    def __rmul__(self, other):
        return QuboTerm(self.coefficient * other, self.vars)

class QuboExpression(object):

    def __init__(self):
        super().__init__()

        # hash -> (term with coefficient)
        self.terms = {}
        self.constant = None

    # Python 3.10: other: QuboTerm | QuboVariable
    def __iadd__(self, other):

        if isinstance(other, int) or isinstance(other, float):
            constant = float(other)

            if self.constant is None:
                self.constant = constant
            else:
                self.constant += constant

            return self

        oother = other
        if isinstance(oother, QuboVariable):
            oother = QuboTerm(1, [oother])
        elif other.order == 2:
            if other.vars[0].key() == other.vars[1].key():
                # simplify x0 * x0 -> x0
                oother = QuboTerm(1, [other.vars[0]])
                oother.coefficient = other.coefficient

        key = oother.key()
        if(key in self.terms):
            self.terms[key].coefficient += oother.coefficient

            if(self.terms[key].coefficient == 0):
                del self.terms[key]
        else:
            self.terms[key] = oother

        return self

    # Python 3.10: other: QuboTerm | QuboVariable
    def __isub__(self, other):

        if isinstance(other, int) or isinstance(other, float):
            constant = float(other)

            if self.constant is None:
                self.constant = -constant
            else:
                self.constant -= constant

            return self

        oother = other
        if isinstance(oother, QuboVariable):
            oother = QuboTerm(1, [oother])
        elif other.order == 2:
            if other.vars[0].key() == other.vars[1].key():
                # simplify x0 * x0 -> x0
                oother = QuboTerm(1, [other.vars[0]])
                oother.coefficient = other.coefficient

        key = oother.key()
        if(key in self.terms):
            self.terms[key].coefficient -= oother.coefficient

            if(self.terms[key].coefficient == 0):
                del self.terms[key]
        else:
            self.terms[key] = oother
            self.terms[key].coefficient *= -1

        return self

    def eval(self, shift = 0):
        E = shift

        for term in self.terms:
            E += self.terms[term].eval()

        if self.constant != None:
            E += self.constant

        return E

    def __str__(self):
        s = " ".join([str(self.terms[t]) for t in self.terms])

        if self.constant is not None:
            s += (f" + {self.constant}" if self.constant > 0 else f" - {abs(self.constant)}")

        return s

class QuboModel(object):

    def __init__(self):

        self.vars = {}
        self.objective = QuboExpression()

        # for future use
        self.sos1 = []
        self.sos2 = []

        self._pos_ctr = 0

    def addSOS1(self, vars : list):
        warnings.warn("SOS1 constraints are currently not supported in QUBOs")
        self.sos1.append(vars)

    def addSOS2(self, vars : list):
        warnings.warn("SOS2 constraints are currently not supported in QUBOs")
        self.sos2.append(vars)

    def addVariable(self, name : str, initial=None, fixing=None, disable_warnings=False):
        if(name in self.vars):
            if(not disable_warnings):
                warnings.warn("Variable " + name + " already in QUBO...")

            return self.vars[name]

        self.vars[name] = QuboVariable(name, self._pos_ctr, initial, fixing)
        self._pos_ctr += 1

        return self.vars[name]

    def variable(self, name : str):
        return self.vars[name]

    def eval(self):
        return self.objective.eval()

    def _reduce_symmetric_terms(self):

        # in the internal QUBO format, only the upper triangular matrix should
        # be specified; hence when the problem contains entries (i < j)
        # a x_i x_j + a x_j x_i (-> store only a in (i, j))
        # If however, it contains a x_i x_j + b x_j x_i with a != b, the problem
        # is not symmetric and an exception is triggered
        symm_terms = {}

        for key in self.objective.terms:
            term = self.objective.terms[key]

            if term.order == 1:
                # terms on the diagonal
                symm_terms[key] = copy.deepcopy(self.objective.terms[key])

            if term.order == 2:
                # we only want to deal with terms in the upper triangular part
                if term.vars[0].id() < term.vars[1].id():

                    symm_terms[key] = copy.deepcopy(self.objective.terms[key])

                    coeff = symm_terms[key].coefficient

                    search_term = QuboTerm(1.0, [term.vars[1], term.vars[0]])
                    if search_term.key() in self.objective.terms:
                        symm_term = self.objective.terms[search_term.key()]
                        if symm_term.coefficient != term.coefficient:

                            coeff = 0.5 * (coeff + self.objective.terms[search_term.key()].coefficient)
                            warnings.warn("Asymmetric QUBO detected, will store Q' = 1/2 * (A + A^T)...")

                    else:
                        coeff = 0.5 * coeff
                        warnings.warn("Asymmetric QUBO detected, will store Q' = 1/2 * (A + A^T)...")

                    symm_terms[key].coefficient = coeff

                # if however terms are added to the lower triangular only, then we deal with it here
                else:
                    # only get the terms that are not present in the upper triangle
                    search_term = QuboTerm(1.0, [term.vars[1], term.vars[0]])
                    if not search_term.key() in self.objective.terms:

                        warnings.warn("Asymmetric QUBO detected, will store Q' = 1/2 * (A + A^T)...")

                        # inject 0.5 * coefficient in the upper triangle
                        symm_terms[search_term.key()] = search_term
                        symm_terms[search_term.key()].coefficient = 0.5 * term.coefficient


        return symm_terms

    def writeQUBO(self, path : str):

        upper_triangular_terms = self._reduce_symmetric_terms()

        with open(path, 'w') as f:

            f.write("1\n")
            f.write("1.0\n")

            shift = 0.0
            if self.objective.constant is not None:
                shift = self.objective.constant
            f.write(f"{shift}\n")

            # create sparse matrix from terms in objective
            f.write(f"{len(self.vars)} {len(upper_triangular_terms)}\n")
            for key in upper_triangular_terms:
                term = upper_triangular_terms[key]

                if(term.order == 1):
                    f.write(f"{term.vars[0].id()} {term.vars[0].id()} {term.coefficient}\n")
                if(term.order == 2):
                    f.write(f"{term.vars[0].id()} {term.vars[1].id()} {term.coefficient}\n")

            # add fixings
            for var in self.vars.values():
                if var.fixing:
                    f.write(f"f {var.id()} {var.fixing}\n")

    @classmethod
    def readQUBO(cls, path : str):

        if path.endswith(".gz"):
            with gzip.open(path, 'rt') as f:
                qubo = cls._readQuboFile(f)
        else:
            with open(path, 'r') as f:
                qubo = cls._readQuboFile(f)

        return qubo

    @classmethod
    def _readQuboFile(cls, f):
        num_terms = int(f.readline().strip())
        weight = float(f.readline().strip())
        if weight != 1.0:
            raise Exception("Weighted QUBOs are not supported...")
        shift = float(f.readline().strip())

        nnz_string = f.readline().strip().split(" ")
        num_vars = int(nnz_string[0])
        num_nnz = int(nnz_string[1])

        # create variables
        qubo = QuboModel()

        if shift != 0:
            qubo.objective += shift

        vars = []
        for ix in range(0, num_vars):
            vars.append(qubo.addVariable(f"x_{ix}"))

        # create terms
        term_ctr = 0
        line = f.readline()
        check_symmetry = False
        lower_terms = []
        while line != "":
            split = line.split(" ")
            ix_i = int(split[0])
            ix_j = int(split[1])
            entry = float(split[2])

            if ix_i == ix_j:
                qubo.objective += entry * vars[ix_i]
            elif ix_i > ix_j:
                raise Exception("Invalid .qubo file, only upper triangular matrix can be stored")
            else:
                # qubo file is supposed to be symmetric; add both entries
                qubo.objective += entry * vars[ix_i] * vars[ix_j]
                qubo.objective += entry * vars[ix_j] * vars[ix_i]

            term_ctr += 1

            line = f.readline()

        if term_ctr != num_nnz:
            raise Exception("Invalid .qubo files, number of NNZ specified does not match NZ entries!")

        return qubo

    def __str__(self):
        return str(self.objective)

    def _solvePrep(self):

        # temporary folder for the QUBO problem
        tmp_path = tempfile.mkdtemp()
        tmp_problem = os.path.join(tmp_path, "pyclient.qubo")

        # convert problem into QUBO format (i.e. a matrix)
        self.writeQUBO(tmp_problem)

        return tmp_problem

    def _solveParse(self, solution):

        # parse solution, store assignments in variables
        sol_string_splitted = solution.split("\n")

        for var in self.vars:
            self.vars[var].assignment = int(sol_string_splitted[self.vars[var].id()])

    async def solveAsync(self, specs : dict, runner : Runner, **kwargs):

        tmp_problem = self._solvePrep()
        res = await runner.solveAsync(tmp_problem, specs, **kwargs)

        self._solveParse(res['solution_file'])

        # return (optimal) objective
        return self.eval()

    def solve(self, specs : dict, runner : Runner, **kwargs):

        tmp_problem = self._solvePrep()
        res = runner.solve(tmp_problem, specs, **kwargs)

        self._solveParse(res['solution_file'])

        # return (optimal) objective
        return self.eval()

    def __str__(self):
        return str(self.objective)

    #######
    # PYQUBO Compatibility Layer
    #######
    def fromPyQuboModel(self, model : pq.Model, constants : dict = {}):
        self.vars = {}
        self.objective = QuboExpression()
        self._pos_ctr = 0

        # guarantees that we only have terms of oders {1, 2}
        qmodel, shift = model.to_qubo(feed_dict=constants)

        # create objective from QUBO model
        for term in qmodel:
            if(term[0] == term[1]):
                # unary term
                v = self.addVariable(term[0], disable_warnings=True)
                self.objective += QuboTerm(qmodel[term], [v])
            else:
                # pairwise term
                v0 = self.addVariable(term[0], disable_warnings=True)
                v1 = self.addVariable(term[1], disable_warnings=True)
                self.objective += QuboTerm(qmodel[term], [v0, v1])

        if shift != 0:
            self.objective += shift
