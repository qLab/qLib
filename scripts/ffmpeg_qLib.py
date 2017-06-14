import mvexportutils
import os

import sys

def dbg(m):
	msg = "[test] %s" % str(m)
	sys.stderr.write('%s\n' % msg)
	hou.hscript('message "%s"' % msg)



def isSupported():
    #dbg('isSupported()')
    try:
        #status, (stdout, stderr) = mvexportutils.run(['ffmpeg'])
	return True
    except:
        return False
    return True

def ffmpeg_queryCodecs():
    video_codecs = {}
    audio_codecs = {}

    status, (stdout, stderr) = mvexportutils.run(['ffmpeg', '-formats'])
    lines = stdout.splitlines()
    try:
        codec_start = lines.find('Codecs:')
    except:
        # Probably failed due to a newer version of ffmpeg.
        status, (stdout, stderr) = mvexportutils.run(['ffmpeg', '-codecs'])
        lines = stdout.splitlines()
        codec_start = 0
    for line in lines[codec_start+1:]:
        if len(line) == 0:
            break

        space_index = line.rfind(' ')
        if space_index >= 0:
            codec_flags = line[1:space_index]
            # We may not have enough characters, in which
            # case we skip this.
            if len(codec_flags) > 3:
                if codec_flags[2] == 'V':
                    video_codecs[line[space_index+1:]] = codec_flags
                elif codec_flags[2] == 'A':
                    audio_codecs[line[space_index+1:]] = codec_flags
    return video_codecs, audio_codecs

def encode(kwargs):
    dbg('encode() %s' % str(kwargs))
    args = []
    args.append('ffmpeg')
    # Ensure that we don't prompt about overwriting output files.
    args.append('-y')
    args.extend(['-r', "%g" % kwargs['framerate']])
    args.extend(['-i', kwargs['imagefilesstringformat']])
    # args.append('-shortest')

    # Codec names are different depending on the version of ffmpeg installed
    # so query them directly from the application.
    video_codecs, audio_codecs = ffmpeg_queryCodecs()

    audio_preset = {}
    if audio_codecs.has_key('libfaac'):
        audio_preset['aac'] = ['-acodec', 'libfaac']
    else:
        audio_preset['aac'] = ['-acodec', 'aac']
    if audio_codecs.has_key('libmp3lame'):
        audio_preset['mp3'] = ['-acodec', 'libmp3lame', '-ab', '192k']
    else:
        audio_preset['mp3'] = ['-acodec', 'mp3', '-ab', '192k']

    if kwargs.has_key('audiofile') and len(kwargs['audiofile']) > 0:
        args.extend(['-i', kwargs['audiofile']])
        if kwargs.has_key('audiocopy') and kwargs['audiocopy']:
            args.extend(['-acodec', 'copy'])
        else:
            args.extend(audio_preset[kwargs['audiopreset']])
        # Restrict the duration to that of the video, in seconds, otherwise a
	# longer audio track will specified value in seconds, otherwise
	# a long 
        args.extend(['-t', "%g" % mvexportutils.videoDuration(kwargs)])

    if kwargs['videopreset'].find('hq') >= 0:
        args.extend(['-qscale', '1'])   # highest quality VBR
    else:
        args.extend(['-qscale', '4'])   

    args.append(kwargs['outputfile'])

    dbg("args: %s" % str(args))
    #return False
    return mvexportutils.run(args)

