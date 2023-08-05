
import os

from obspy.core.event.origin import Arrival
from obspy.core.event.origin import Origin
from obspy.core.event.origin import OriginQuality, OriginUncertainty
from obspy.core.event.origin import Pick
from obspy.core.event.base import CreationInfo
from obspy.core.event.base import QuantityError
from obspy.core.event.base import WaveformStreamID
from obspy.core.utcdatetime import UTCDateTime
from obspy.core.event.magnitude import Magnitude
from obspy.core.event.magnitude import Amplitude

#from mappings import (hypoinv_weight_to_obspy_time_error,
from .mappings import (hypoinv_weight_to_obspy_time_error,
                    obspy_time_error_to_hypoinv_weight)

import numpy as np

from obspy.core.event import Catalog
from obspy.core.event.event import Event

from logging import getLogger
logger = getLogger()

from .lib_y2k import read_format, parse_y2k_line, check_set
#from lib_y2k import read_format, parse_y2k_line

from .. import get_format_dir
#from zget_dir import get_format_dir
formats_dir = get_format_dir()

def seisan_to_quakeml(seisan_file, args=None):

    '''
    Note: Type 1 line must be the first, all type 4 lines should be together and the last line must be blank
          Type E Line (Optional): Hyp error estimates
          Type H line, High accuracy hypocenter line
    '''
    formats = {}
    #nordic_types = ['1', '4', '6', '7', 'E', 'H', 'I']
    nordic_types = ['1', '4', 'E', 'H']

    logger.info("formats_dir=%s" % formats_dir)

    for ntype in nordic_types:
        #format_file = '../formats/format.nordic.type%s' % ntype
        format_file = os.path.join(formats_dir, 'format.nordic.type%s' % ntype)
        formats[ntype]= read_format(format_file)

    try_with_iso_encoding = False
    with open(seisan_file, 'r', encoding='utf-8') as f:
        try:
            lines = f.readlines()
        except UnicodeDecodeError:
            try_with_iso_encoding = True
            logger.warning("Caught UnicodedecodeError --> Try again with iso encoding")

    if try_with_iso_encoding:
        with open(seisan_file, 'r', encoding='ISO-8859-1') as f:
            try:
                lines = f.readlines()
            except UnicodeDecodeError:
                logger.error("Caught UnicodedecodeError AGAIN!!")


    line_1 = None
    line_E = None
    line_H = None

    for line in lines:
        if len(line.strip()) == 0:
            break
        if line[79].strip() == "1":
            line_1 = line
        elif line[79].strip() == "H":
            line_H = line
        elif line[79].strip() == "E":
            line_E = line

    origin = None
    origin_hypo = None
    magnitudes = []
    if line_1:
        seisan_hdr = parse_y2k_line(line_1, formats['1'])
        origin = seisan_hdr_to_origin(seisan_hdr)
        magnitudes = seisan_hdr_to_magnitudes(seisan_hdr)
    if line_H:
        seisan_hypo = parse_y2k_line(line_H, formats['H'])
        origin_hypo = seisan_hdr_to_origin(seisan_hypo)
    if line_E:
        seisan_errs = parse_y2k_line(line_E, formats['E'])
        add_seisan_errors_to_origin(seisan_errs, origin)
        origin.quality.azimuthal_gap = seisan_errs['Gap']

    if origin_hypo:
        origin.time = origin_hypo.time
        origin.latitude = origin_hypo.latitude
        origin.longitude = origin_hypo.longitude
        origin.depth = origin_hypo.depth

    # MTH: probably don't want this:
    #for magnitude in magnitudes:
        #magnitude.azimuthal_gap = origin.quality.azimuthal_gap

    ntype = '4'
    arrivals = []
    amplitudes = []
    picks = []
    for line in lines:
        if len(line.strip()) == 0:
            break
        if not line[79] in ['4', ' ']:
            continue

        parsed_type4 = parse_y2k_line(line, formats[ntype])
        # MTH: type4 Phase = 1-4 chars
        #    Probably it should look like:
        #12345678901234567890
        # ODSA HZ IP        65323.000                             125   -0.0510 7.71 108
        # ODSA H1 IS        65324.488                             125   -0.1710 7.71 108
        # ODSA H2 IAML      65324.691     15409.9 0.15                          7.71 108
        #    But it looks like (IAML col is right-shifted 1):
        #12345678901234567890
        # ODSA HZ IP        65323.000                             125   -0.0510 7.71 108
        # ODSA H1 IS        65324.488                             125   -0.1710 7.71 108
        # ODSA H2  IAML     65324.691     15409.9 0.15                          7.71 108
        #
        # valid pick phases: 'P', 'Pg', 'S', 'Sn'

        if not parsed_type4['Phase']:
            logger.warning("nordic_to_qml: Unable to parse valid phase from line=[%s]" % line)
            continue

        if parsed_type4['Phase'][0] not in ['P', 'S', 'A', 'I'] or \
           (len(parsed_type4['Phase']) == 1 and parsed_type4['Phase'] not in ['P', 'S']):
            #logger.warning("nordic_to_qml: Phase=[%s] doesn't look like: 'P', 'S', or 'A' !" %
                           #parsed_type4['Phase'])
            logger.warning("nordic_to_qml: Unable to parse valid phase from line=[%s]" % line)
            continue

        if args.network_code is None:
            parsed_type4['network_code'] = 'UNK'
        else:
            parsed_type4['network_code'] = args.network_code

        if args.network_dict:
            sta = parsed_type4['sta']
            if sta in args.network_dict:
                parsed_type4['network_code'] = args.network_dict[sta]
            else:
                logger.warning("** No network code for stn:%s in network_dict" % sta)


        if parsed_type4['Phase'][0] in ['A', 'I']:
            if args.fix_amptype:
                parsed_type4['amplitude_type'] = 'WAS'
                # SEISAN WAS units are in NM but obspy amplitude doesn't support nm:
                parsed_type4['amplitude_unit'] = 'other'

            amplitude = seisan_type4_to_amplitude(parsed_type4, origin)
            amplitudes.append(amplitude)
        else:
            arrival, pick = seisan_type4_to_arrival(parsed_type4, origin)
            arrivals.append(arrival)
            picks.append(pick)

    origin.arrivals = arrivals
    event = Event()
    event.origins = [origin]
    event.picks = picks
    event.preferred_origin_id = origin.resource_id.id
    event.magnitudes = magnitudes
    if magnitudes:
        stns = set([amp.waveform_id.station_code for amp in amplitudes])
        for magnitude in magnitudes:
            magnitude.station_count = len(stns)

        event.preferred_magnitude_id = magnitudes[0].resource_id.id
    event.amplitudes = amplitudes

    cat = Catalog(events=[event])

    if origin is None:
        logger.warning("Missing origin: Looks like an empty s-file --> Exitting")
        return None
    elif origin.latitude is None:
        logger.warning("Missing origin latitude: Looks like an empty s-file --> Exitting")
        return None
    elif origin.longitude is None:
        logger.warning("Missing origin longitude: Looks like an empty s-file --> Exitting")
        return None
    elif origin.depth is None:
        logger.warning("Missing origin depth: Looks like an empty s-file --> Exitting")
        return None
    elif not arrivals:
        logger.warning("Missing arrivals: Looks like an empty s-file --> Exitting")
        return None

    return cat

def seisan_type4_to_amplitude(type4, origin):
    '''
    Convert a seisan type4 phase dict to obspy amplitude

    :param type4: parsed type4 line
    :type type4: python dict

    :return: converted phase 
    :rtype: obspy amplitude
    '''

    net=type4['network_code']
    sta=type4['sta']

    waveform_id = WaveformStreamID(net, sta)
    channel_code = "%sH%s" % (type4['Instrument_type'], type4['Component'])
    waveform_id.channel_code = channel_code
    # MTH:
    #waveform_id.location_code = "00"

    year = origin.time.year
    mo = origin.time.month
    dd = origin.time.day
    hh = type4['Hour']
    mi = type4['Minutes']
    ss = type4['Seconds']
    date = "%s-%s-%sT%s:%s:%s" % (year, mo, dd, hh, mi, ss)

    amplitude = Amplitude()
    amplitude.waveform_id = waveform_id
    amplitude.generic_amplitude = type4['Amplitude']
    #amplitude.scaling_time = UTCDateTime(date)
    amplitude.scaling_time = getUTCDateTime(year, mo, dd, hh, mi, ss)

    if 'amplitude_type' in type4:
        amplitude.type = type4['amplitude_type']
        amplitude.unit = type4['amplitude_unit']
    else:
        amplitude.type = 'AML' if 'AML' in type4['Phase'] else 'A'
        #amplitude.unit = ??

    if 'Period' in type4 and type4['Period'] > 0.:
        amplitude.period = type4['Period']

    return amplitude


def seisan_type4_to_arrival(type4, origin):
    '''
    Convert a seisan type4 phase dict to obspy arrival

    :param type4: parsed type4 line
    :type type4: python dict

    :return: converted phase 
    :rtype: obspy arrival and pick
    '''

    arrival = Arrival()
    phase = type4['Phase']
    arrival.phase = phase

    net=type4['network_code']
    sta=type4['sta']

    waveform_id = WaveformStreamID(net, sta)
    channel_code = "%sH%s" % (type4['Instrument_type'], type4['Component'])
    waveform_id.channel_code = channel_code
    # MTH:
    #waveform_id.location_code = "00"

    if check_set(type4, 'Azimuth_at_the_source'):
        arrival.azimuth = type4['Azimuth_at_the_source']
    if check_set(type4, 'Azimuth_residual'):
        arrival.backazimuth_residual = type4['Azimuth_residual']   # Could be wrong - is it even in the seisan manual ??
    if check_set(type4, 'Epicentral_distance'):
        arrival.distance = type4['Epicentral_distance'] / 111.19   # obspy dist in deg
    if check_set(type4, 'Angle_of_incidence'):
        arrival.takeoff_angle = type4['Angle_of_incidence']        # No idea if these are measured with same convention
    if check_set(type4, 'Travel_time_residual'):
        arrival.time_residual = type4['Travel_time_residual']

    # Unmapped:              type4 field
    # somehow type4 I2      L   Weight ==> needs to map to arrival.time_weight (=float) ?
    #               I1      L   Weighting_indicator     (1-4) 0 or bank = full weight, 1=75%, 2=50%, 3=25%, 4=0%

    pick = Pick()
    arrival.pick_id = pick.resource_id
    pick.waveform_id = waveform_id
    year = origin.time.year
    mo = origin.time.month
    dd = origin.time.day
    hh = type4['Hour']
    mi = type4['Minutes']
    ss = type4['Seconds']
    date = "%s-%s-%sT%s:%s:%s" % (year, mo, dd, hh, mi, ss)
    #pick.time = UTCDateTime(date)
    pick.time = getUTCDateTime(year, mo, dd, hh, mi, ss)

    if check_set(type4, 'Phase_velocity'):
        pick.horizontal_slowness = 111.19 / type4['Phase_velocity'] # km/s --> s/deg
    if check_set(type4, 'Direction_of_approach'):
        pick.backazimuth = type4['Direction_of_approach']     # This is a guess - is it explained in the manual ??

    onset = type4['Quality_indicator']

    if onset == 'I':
        pick.onset = "impulsive"
    elif onset == 'E':
        pick.onset = "emergent"

    pick.phase_hint = phase

    if phase == 'P':
        if type4['First_motion'] == 'C':
            pick.polarity == 'positive'
        elif type4['First_motion'] == 'D':
            pick.polarity == 'negative'

    time_errors = QuantityError()
    #if not check_set(type4, 'Weighting_indicator'):
        #time_errors.uncertainty = hypoinv_weight_to_obspy_time_error(-9)
    #else:
        #time_errors.uncertainty = hypoinv_weight_to_obspy_time_error(type4['Weighting_indicator'])
    time_errors.uncertainty = hypoinv_weight_to_obspy_time_error(type4['Weighting_indicator'])
    pick.time_errors = time_errors

    return arrival, pick


def seisan_hdr_to_origin(seisan_hdr):
    '''
    Convert a seisan type1 or typeH line to quakeml Origin

    :param seisan_hdr: seisan type1/typeH parsed line
    :type seisan_hdr: python dict

    :return: converted origin 
    :rtype: obspy.core.event.origin.Origin
    '''

    origin = Origin()

    year = seisan_hdr['Year']

    mo = seisan_hdr['Month']
    dd = seisan_hdr['Day']
    hh = seisan_hdr['Hour']
    mi = seisan_hdr['Minutes']
    ss = seisan_hdr['Seconds']

    #date = "%s-%s-%sT%s:%s:%s" % (year, mo, dd, hh, mi, ss)
    #origin.time = UTCDateTime(date)
    origin.time = getUTCDateTime(year, mo, dd, hh, mi, ss)

    if check_set(seisan_hdr, 'Longitude'):
        origin.longitude = seisan_hdr['Longitude']
    if check_set(seisan_hdr, 'Latitude'):
        origin.latitude = seisan_hdr['Latitude']
    if check_set(seisan_hdr, 'Depth'):
        origin.depth = seisan_hdr['Depth'] * 1.e3  # seisan depth [km] --> obspy depth [m]

    if 'Depth_indicator'in seisan_hdr:
        if seisan_hdr['Depth_indicator'] == 'F':
            origin.depth_type = "operator assigned"
    if 'Fix_o_time' in seisan_hdr:
        if seisan_hdr['Fix_o_time'] == 'F':
            origin.time_fixed = True

    quality = OriginQuality()
    # MTH: default is to map missing fields in s-file to "-9":
    if 'Number_of_stations_used' in seisan_hdr:
        if check_set(seisan_hdr, 'Number_of_stations_used'):
            quality.used_station_count = seisan_hdr['Number_of_stations_used']
    if 'RMS_of_time_residuals' in seisan_hdr:
        if check_set(seisan_hdr, 'RMS_of_time_residuals'):
            quality.standard_error  = seisan_hdr['RMS_of_time_residuals']

    origin.quality = quality

    creation_info = CreationInfo()
    if 'Hypocenter_reporting_agency' in seisan_hdr:
        creation_info.agency_id = seisan_hdr['Hypocenter_reporting_agency']
    origin.creation_info = creation_info

    return origin

def seisan_hdr_to_magnitudes(seisan_hdr):
    '''
    Convert a seisan type1 or typeH line to quakeml magnitudes

    :param seisan_hdr: seisan type1/typeH parsed line
    :type seisan_hdr: python dict

    :return: obspy magnitudes
    :rtype: list
    '''

    seisan_mag_types = {'L':'ML', 'b':'mb', 'B':'mB', 's':'Ms', 'S':'MS', 'W':'Mw', 'G':'MbLg', 'C':'Mc'}

    creation_info = None
    #  len(seisan_hdr['Magnitude_reporting_agency'].strip()) > 0:
    if check_set(seisan_hdr, 'Magnitude_reporting_agency'):
        creation_info = CreationInfo()
        creation_info.agency_id = seisan_hdr['Magnitude_reporting_agency']

    magnitudes = []
    for i in range(2):
        field = 'Magnitude_no_%d' % (i+1)
        if check_set(seisan_hdr, field):
            #print("field:%s has value:%f" % (field, seisan_hdr[field]))
            magnitude = Magnitude()
            magnitude.mag = seisan_hdr[field]
            if not check_set(seisan_hdr, 'Type_of_magnitude'):
                mag_type = 'M' # default = unspecified
            elif seisan_hdr['Type_of_magnitude'] in seisan_mag_types:
                mag_type = seisan_mag_types[seisan_hdr['Type_of_magnitude']]
            else: # Use as is
                mag_type = seisan_hdr['Type_of_magnitude']

            magnitude.magnitude_type = mag_type
            # This is probably wrong - likely better to count the # of type4 line amp measurements
            # 2021-11-26 - Now counting type4 line amp stations in seisan_to_quakeml:
            #magnitude.station_count = seisan_hdr['Number_of_stations_used'] 

            if creation_info:
                magnitude.creation_info = creation_info

            magnitudes.append(magnitude)

    return magnitudes


def add_seisan_errors_to_origin(seisan_errs, origin):
    '''
    seisan_errs = parsed seisan typeE line
    '''

    if seisan_errs['Longitude_error'] >= 0:
        longitude_errors = QuantityError()
        longitude_errors.uncertainty = seisan_errs['Longitude_error']
        origin.longitude_errors = longitude_errors

    if seisan_errs['Latitude_error'] >= 0:
        latitude_errors = QuantityError()
        latitude_errors.uncertainty = seisan_errs['Latitude_error']
        origin.latitude_errors = latitude_errors

    if seisan_errs['Depth_error'] >= 0:
        depth_errors = QuantityError()
        depth_errors.uncertainty = seisan_errs['Depth_error']
        origin.depth_errors = depth_errors

    if seisan_errs['Origin_time_error'] >= 0:
        time_errors = QuantityError()
        time_errors.uncertainty = seisan_errs['Origin_time_error']
        origin.time_errors = time_errors

    ''' What to do with this ?
    uncertainty = OriginUncertainty()
    seisan_hdrs['Covariance_xy']
    seisan_hdrs['Covariance_xz']
    seisan_hdrs['Covariance_yz']
    uncertainty.
    origin.uncertainty = uncertainty
horizontal_uncertainty (float, optional)
Circular confidence region, given by single value of horizontal uncertainty. Unit: m
min_horizontal_uncertainty (float, optional)
Semi-minor axis of confidence ellipse. Unit: m
max_horizontal_uncertainty (float, optional)
Semi-major axis of confidence ellipse. Unit: m
azimuth_max_horizontal_uncertainty (float, optional)
Azimuth of major axis of confidence ellipse. Measured clockwise from South-North direction at epicenter. Unit: deg
confidence_ellipsoid (ConfidenceEllipsoid, optional)
Confidence ellipsoid
preferred_description (str, optional)
Preferred uncertainty description. See OriginUncertaintyDescription for allowed values.
confidence_level (float, optional)
Confidence level of the uncertainty, given in percent.
    '''

def getUTCDateTime(year, mo, dd, hh, mi, ss):

    if hh >= 24:
        logger.warning("hour=[%s] needs to be converted" % hh)
        dd += 1
        hh -= 24

    if mi >= 60:
        logger.warning("minute=[%s] needs to be converted" % mi)
        hh += 1
        mi -= 60

    if ss >= 60:
        logger.warning("second=[%s] needs to be converted" % ss)
        mi += 1
        ss -= 60

    date = "%s-%s-%sT%s:%s:%s" % (year, mo, dd, hh, mi, ss)

    utc = UTCDateTime(date)
    return utc


    return


if __name__ == "__main__":
    main()
