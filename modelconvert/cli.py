# -*- coding: utf-8 -*-
"""


"""

import sys
import logging
import click

from modelconvert import __version__

__author__ = "Andrew Davison"
__copyright__ = "Andrew Davison"
__license__ = "mit"

_logger = logging.getLogger(__name__)




def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def guess_input_format(input_model):
    raise NotImplementedError


def from_PyNN(input_model, output_format, output_file=None):
    if output_format == "NeuroML":
        if output_file is None:
            output_file = input_model.replace(".py", ".nml")
        # todo: introspect input file, modify setup() call if necessary to
        command = "python {} neuroml"
    elif output_format == "SONATA":
        # from pyNN.network import Network
        # from pyNN.serialization import export_to_sonata

        # sim.setup()
        # ...
        # # create populations, projections, etc.
        # ...

        # # add populations and projections to a Network
        # net = Network(pop1, pop2, ...., prj1, prj2, ...)

        # export_to_sonata(net, "sonata_output_dir")
    else:
        raise NotImplementedError


def from_NeuroML(input_model, output_format, output_file=None):
    raise NotImplementedError


def from_SONATA(input_model, output_format, output_file=None):
    raise NotImplementedError


def from_NetPyNE(input_model, output_format, output_file=None):
    raise NotImplementedError


CONVERTERS = {
    "PyNN": from_PyNN,
    "NeuroML": from_NeuroML,
    "SONATA": from_SONATA,
    "NetPyNE": from_NetPyNE
}


@click.command
@click.argument('input-model', click.Path(exists=True),
                help="model to be converted")
@click.argument('output-format', click.Choice(("PyNN", "NeuroML"), case_sensitive=False),
                help="format the model should be converted to")
@click.option('-i', '--input-format',
              help="format the model is being converted from")
@click.option('-o', '--output-file',
              help="file or directory name for the output model")
@click.option('-v', '--verbose', click.BOOL)
def run(input_model, output_format, input_format=None, output_file=None, verbose=False):
    """
    docstring goes here
    """
    if verbose:
        setup_logging(logging.INFO)
    else:
        setup_logging(logging.WARNING)
    # Determine input format
    if not input_format:
        input_format = guess_input_format(input_model)

    convert = CONVERTERS[input_format]
    return convert(input_model, output_format, output_file)
