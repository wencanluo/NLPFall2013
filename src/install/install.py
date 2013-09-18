import sys,os,argparse,shutil,glob

def main(argv):
    #
    # CMD LINE ARGS
    # 
    src_path = os.path.abspath(os.path.dirname(__file__))
    default_install_path = os.path.abspath(os.path.join(src_path,'..','install'))

    parser = argparse.ArgumentParser(description='Install dialog state tracking challenge data tools.')
    parser.add_argument('--installpath', dest='raw_install_path', action='store', metavar='PATH',
                        help='Path to install to.  If not specified, defaults to <install-script>/../install.',
                        default=default_install_path)
    args = parser.parse_args()

    #
    # ENVIRONMENT AND INSTALL LOCATIONS
    #
    py_exec = sys.executable
    HASH_BANG = '#! ' + py_exec
    install_path = os.path.abspath(args.raw_install_path)
    print 'Intall Path: ' + install_path
    if (not os.path.exists(install_path)):
        os.makedirs(install_path)

    #
    # COPY OVER CODE
    # 
    shutil.copy(os.path.join(src_path,'VERSION'),install_path)
    for dirname in ['lib','config','bin']:
        src = os.path.join(src_path,dirname)
        dst = os.path.join(install_path,dirname)
        print 'Installing %s' % (dirname)
        print '  src: %s' % (src)
        print '  dst: %s' % (dst)
        if (not os.path.exists(dst)):
            os.makedirs(dst)
        src_files = glob.glob(os.path.join(src,'*'))
        for src_file in src_files:
            basename = os.path.basename(src_file)
            dst_file = os.path.join(dst,basename)
            if (dirname == 'bin'):
                f_in = open(src_file)
                f_out = open(dst_file,'w')
                print >>f_out,HASH_BANG
                f_out.write(f_in.read())
                f_in.close()
                f_out.close()
            else:
                shutil.copy(src_file,dst_file)

if (__name__ == '__main__'):
    main(sys.argv)

