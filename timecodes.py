def parse_timecode(timecode_str):
    """
    Parse a timecode.

    The timecode format:
        MM:SS:FFF, where:
            MM is one or two digits denoting minutes
            SS is one or two digits denoting seconds
            FFF is one to three digits denoting milliseconds

            Leading zeros are permitted.

    * timecode_str: A string containing a timecode.

    Returns the milliseconds represented by the timecode.
    """
    parts = timecode_str.split(':')
    minutes = int(parts[0])
    seconds = int(parts[1])
    if len(parts) == 3:
        milliseconds = int(parts[2])
    else:
        milliseconds = 0
    total_milliseconds = (minutes * 60000) + (seconds * 1000) + milliseconds
    return total_milliseconds

def parse_timecodes(timecode_str):
    """
    Parse a comma separated list of timecodes.
    Format:
        start0-end0,start1-end1,...,startN-endN, where
            start is a timecode denoting the start of section
            end is a timecode denoting the end of a section
            0, 1, ..., N are the number of sections
            The format start and end timecodes are as defined in parse_timecode().

    * timecode_str: A string of comma separated time codes.

    Returns the parsed timecodes as a list of dicts with "start" and "duration" as keys.
    """
    start_times = []
    end_times = []

    for st in timecode_str.split(','):
        start, end = st.split('-')
        start, end = parse_timecode(start), parse_timecode(end)
        start_times.append(start)
        end_times.append(end)

    durations = [j-i for i, j in zip(start_times, end_times)]

    timecodes = []
    for i in range(len(durations)):
        timecodes.append( {
            "start": start_times[i],
            "duration": durations[i]
        } )

    return timecodes


# Some tests
if __name__ == "__main__":
    start_timecode = "00:08"
    end_timecode = "00:14:500"
    start = parse_timecode(start_timecode)
    end = parse_timecode(end_timecode)
    print "start:", start_timecode, "=", start
    print "end:  ", end_timecode, "=", end
    assert start == 8000
    assert end == 14500

