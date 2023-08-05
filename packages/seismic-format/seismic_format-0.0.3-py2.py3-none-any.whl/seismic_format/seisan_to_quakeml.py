# -*- coding: utf-8 -*-
"""
Convert seisan file to quakeml

:copyright:
    Mike Hagerty (m.hagerty@isti.com), 2022
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

import ast
import logging
import os

from seismic_format.libs.cmd_line import parse_cmd_line, required_arg, optional_arg
from seismic_format.libs.libs_log import configure_logger
from seismic_format.libs.nordic_to_qml import seisan_to_quakeml

def main():
    '''
    >>>seisan-to-quakeml /path/to/seisan_file [--loglevel DEBUG] [--logdir logs] [--logfile y2k.log] [--logconsole]
    '''

    r = required_arg(arg=['infile'], type=str, description='seisan file',
                     help='>seisan-to-quakeml seisan_file')
    optional = []
    optional.append(optional_arg(arg=['--network-code'], type=str, description='Hard-code network code in output quakeml file'))
    optional.append(optional_arg(arg=['--network-dict'], type=str, description='File containing stn:net dict to assign network codes'))
    optional.append(optional_arg(arg=['--fix-amptype'], type=bool))

    args, parser = parse_cmd_line(required_args=[r], optional_args=optional, expand_wildcards=False, flag_configfile=False)
    configure_logger(**vars(args))
    logger = logging.getLogger()

    seisan_file = args.infile
    args.network_dict = check_for_network_dict(args)

    infile = os.path.basename(seisan_file)
    # What do seisan files end with ???????
    outfile = infile.replace('.y2k','.qml')
    if outfile == infile:
        logger.info("Infile doesn't have expected .y2k suffix --> Add .qml to infile")
        outfile += ".qml"

    logger.info("infile=%s --> outfile=./%s" % (seisan_file, outfile))

    cat = seisan_to_quakeml(seisan_file, args)
    if cat is None:
        logger.error("seisan_to_quakeml did not scan a valid seisan_file=[%s] --> No conversion output!" % seisan_file)
        exit(2)
    cat.write(outfile, format="QUAKEML")

    return


def check_for_network_dict(args):
    """
    If --network-dict ... was passed on cmd line, read it in 
      and use it to get net from sta code
    """
    #if getattr(args, 'network_dict', None):
    if args.network_dict:
        network_dict = args.network_dict
        if not os.path.exists(network_dict):
            network_dict = os.path.join(os.getcwd(), os.path.basename(args.network_dict))
        if not os.path.exists(network_dict):
            logger.error('Unable to locate network-dict=[%s]' % args.network_dict)
            exit(2)
        with open(network_dict) as f:
            nd = f.read()

        return ast.literal_eval(nd)
    return None

if __name__ == "__main__":
    main()
