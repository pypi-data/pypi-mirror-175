# -*- coding: utf-8 -*-
"""
Convert y2k arc file to quakeml

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
from seismic_format.libs.y2k_to_qml import y2k_to_quakeml

def main():
    '''
    >>>y2k-to-quakeml /path/to/y2kfile [--loglevel DEBUG] [--logdir logs] [--logfile y2k.log] [--logconsole]
    '''

    r = required_arg(arg=['y2kfile'], type=str, description='y2kfile',
                     help='>y2k-to-quakeml y2kfile')
    args, parser = parse_cmd_line(required_args=[r], expand_wildcards=False, flag_configfile=False)
    configure_logger(**vars(args))
    logger = logging.getLogger()

    infile = os.path.basename(args.y2kfile)
    outfile = infile.replace('.y2k','.qml')

    if outfile == infile:
        logger.info("Infile doesn't have expected .y2k suffix --> Add .qml to infile")
        outfile += ".qml"

    logger.info("infile=%s --> outfile=./%s" % (args.y2kfile, outfile))

    cat = y2k_to_quakeml(args.y2kfile)
    cat.write(outfile, format="QUAKEML")

    return

if __name__ == "__main__":
    main()
