import mvexportutils
import os

import sys


def dbg(m):
    msg = "[test] %s" % str(m)
    sys.stderr.write('%s\n' % msg)
    hou.hscript('message "%s"' % msg)


def isSupported():
    # dbg('isSupported()')
    try:
        #status, (stdout, stderr) = mvexportutils.run(['ffmpeg'])
        return True
    except:
        return False
    return True


def encode(kwargs):
    dbg('encode() %s' % str(kwargs))

    vcodec = kwargs['videopreset']
    cmd = ['ffmpeg', '-y',
           '-r', str(kwargs['framerate']),
           '-i', kwargs['imagefilesstringformat']]

    audioFile = kwargs['audiofile']
    if audioFile:
        cmd.extend(('-i', audioFile,
                    '-shortest'))

    cmd.extend(('-s', '{0[xres]}x{0[yres]}'.format(kwargs),
                '-c:v', vcodec))

    if vcodec == 'mjpeg':
        cmd.extend(('-pix_fmt', 'yuvj420p',
                    '-q:v', '1'))
    elif vcodec == 'libx264':
        cmd.extend(('-pix_fmt', 'yuv420p',
                    '-crf', '10',
                    '-preset', 'slow',
                    '-tune', 'animation,fastdecode'))

    audioFlags = None
    if kwargs['audiocopy']:
        acodec = 'copy'
    else:
        acodec = kwargs['audiopreset']
        if acodec == 'aac':
            audioFlags = ('-b:a', '128k',
                          '-strict', 'experimental')

    cmd.extend(('-c:a', acodec))
    if audioFlags:
        cmd.extend(audioFlags)

    cmd.append(kwargs['outputfile'])
    print((subprocess.list2cmdline(cmd)))

    env = os.environ.copy()
    setpkg.setpkg('ffmpeg', environ=env, quiet=True)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            close_fds=True, env=env)
    output = proc.communicate()

    # Function has to return (status, (stdout_data, stderr_data))
    return (proc.returncode, output)
