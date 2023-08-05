# -*- coding: utf-8 -*-
"""
Convert quakeml file to y2k arc file

:copyright:
    Mike Hagerty (m.hagerty@isti.com), 2022
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

import logging
import os

from seismic_format.libs.cmd_line import parse_cmd_line, required_arg, optional_arg
from seismic_format.libs.libs_log import configure_logger
from seismic_format.libs.qml_to_y2k import quakeml_to_y2k

def main():
    '''
    >>>quakeml-to-y2k /path/to/y2kfile [--loglevel DEBUG] [--logdir logs] [--logfile y2k.log] [--logconsole]
    '''

    r = required_arg(arg=['quakeml'], type=str, description='quakeml_file',
                     help='>quakeml-to-y2k qml_file')
    optional = []
    optional.append(optional_arg(arg=['--no-phase'], type=bool, description='Only output event header lines, no phase lines'))
    args, parser = parse_cmd_line(required_args=[r], optional_args=optional, expand_wildcards=False, flag_configfile=False)

    configure_logger(**vars(args))
    logger = logging.getLogger()

    quakemlfile = args.quakeml

    infile = os.path.basename(quakemlfile)
    outfile = infile.replace('.qml', '.y2k')
    if outfile == infile:
        outfile = infile.replace('.xml', '.y2k')
    if outfile == infile:
        logger.info("Infile doesn't have expected suffix (.qml, .xml) --> Add .y2k to infile")
        outfile += ".y2k"

    logger.info("infile=%s --> outfile=./%s" % (quakemlfile, outfile))

    y2k = quakeml_to_y2k(quakemlfile, args.no_phase)

    with open(outfile, 'w') as fh:
        fh.write(y2k)

    return

if __name__ == "__main__":
    main()
