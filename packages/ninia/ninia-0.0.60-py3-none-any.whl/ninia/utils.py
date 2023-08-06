
from fnmatch import filter as flt  # Native filter() function is used as well
from dataclasses import dataclass
from typing import Type, Union
import pkg_resources
import sys
import os
import re

from ase import Atom, Atoms
import pandas as pd
import numpy as np

# Pull in molar mass data from separate csv file
mm_data = pkg_resources.resource_stream(__name__, 'data/mm_of_elements.csv')
molarmass_df = pd.read_csv(mm_data, encoding=sys.stdout.encoding, index_col=0)
# TODO - see if we can pull this in relatively with just pandas - I don't remember


@dataclass
class Control:
    calculation: str = 'relax'
    prefix: str = 'untitled'
    outdir: str = None
    pseudo_dir: str = None
    nstep: int = None
    verbosity: str = None
    restart_mode: str = None
    dt: float = None
    max_seconds: float = None
    forc_conv_thr: float = None
    etot_conv_thr: float = None


@dataclass
class System:
    ibrav: int = 0
    A: float = None
    B: float = None
    C: float = None
    cosAB: float = None
    cosAC: float = None
    cosBC: float = None
    nat: int = None
    ntyp: int = None
    tot_charge: float = None
    ecutwfc: float = None
    ecutrho: float = None
    nosym: bool = None
    nosym_evc: bool = None
    occupations: str = 'smearing'
    degauss: float = 0.02
    smearing: str = 'mv'
    nspin: int = None
    input_dft: str = None
    assume_isolated: str = None
    esm_bc: str = None


@dataclass
class Electrons:
    electron_maxstep: int = None
    scf_must_converge: bool = None
    conv_thr: float = None
    adaptive_thr: bool = None
    conv_thr_init: float = None
    mixing_mode: str = None
    mixing_beta: float = 0.7
    mixing_ndim: int = None
    diagonalization: str = None


@dataclass
class Job:
    job_type: str = 'slurm'
    nodes: int = 1
    ntasks: int = 16
    partition: str = 'general'
    time: int = 50
    memory: int = 100
    mail_type: list[str] = None  # Options: ( NONE, BEGIN, END, FAIL, REQUEUE, ALL )
    mail_user: str = None
    exec: str = 'pw.x'
    nk: int = None
    input: str = None
    output: str = None


def position(geometry: Union[Type[Atom], Type[Atoms]] = None) -> tuple[int, int, str]:

    atomic_positions = ''
    positions = geometry.get_positions().tolist()
    symbols = geometry.get_chemical_symbols()
    unique_symbols = list(set(symbols))
    atom_count = len(positions)

    for atom_set in zip(symbols, positions):
        atomic_positions += f'   {atom_set[0]}\t{np.round(atom_set[1][0], 8):.8f}'
        atomic_positions += f'\t{np.round(atom_set[1][1], 8):.8f}\t{np.round(atom_set[1][2], 8):.8f}'

    return atom_count, len(unique_symbols), atomic_positions
    # nat, ntyp, atomic_positions


def species(geometry: Union[Type[Atom], Type[Atoms]] = None, pseudo_dir: str = None) -> str:

    symbols = geometry.get_chemical_symbols()
    unique_symbols = list(set(symbols))

    list_upf = flt(os.listdir(pseudo_dir), '*.[Uu][Pp][Ff]')
    species_string = ''

    for symbol in unique_symbols:

        r = re.compile(rf'{symbol}[_|.]\S+\Z', flags=re.IGNORECASE)
        match = list(filter(r.match, list_upf))[0]
        mw_species = molarmass_df.loc[symbol][0]

        species_string += f'   {symbol}\t{mw_species}\t{match}\n'

    return species_string


def cell_parameters(geometry: Union[Type[Atom], Type[Atoms]] = None) -> str:

    supercell = geometry.get_cell()
    cell_string = ''

    for dimension in supercell:
        cell_string += f'{dimension[0]:.14f}\t{dimension[1]:.14f}\t{dimension[2]:.14f}\n'

    return cell_string
