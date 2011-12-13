#!/usr/bin/env python
import sys
import os
import glob
#PKG = 'win_setup' # this package name
#import roslib; roslib.load_manifest(PKG)
import roslib
ROSROOT=roslib.rosenv.get_ros_root()
sys.path.append(os.path.join(ROSROOT+"_comm","clients","rospy","src"))
sys.path.append(os.path.join(ROSROOT+"_comm","clients","rospy","scripts"))
sys.path.append(os.path.join(ROSROOT+"_comm","clients","cpp","roscpp","scripts"))
sys.path.append(os.path.join(ROSROOT+"_comm","clients","cpp","roscpp","src","roscpp"))

#for python
import genutil
import genmsg_py
import gensrv_py
#for cpp
import msg_gen
import gensrv_cpp

##############################################################################
# Functions
##############################################################################

def genmsgMain(argv, stdout, env):
    #print(argv)
    if(len(argv) < 3):
        print("*Ussage : %s [msg/srv/both] [package name]."%os.path.basename(argv[0]))
    else:
        try:
            dep_list = roslib.rospack.rospack_depends(argv[2])
            #print(dep_list) 
        except Exception:
            print("*Error : wrong package name.")
            return -1
        whole_list=dep_list
        whole_list.append(argv[2])
        if(argv[1] == "msg" or argv[1] == "both"):
            gen_msg_srv_py(whole_list,"msg")
            gen_msg_srv_cpp(whole_list,"msg")
        if(argv[1] == "srv" or argv[1] == "both"):
            gen_msg_srv_py(whole_list,"srv")
            gen_msg_srv_cpp(whole_list,"srv")
    raw_input("Press ENTER to continue.")
       
def gen_msg_srv_py(list,type):
    for pkg in list:
        pkgdir = roslib.packages.get_pkg_dir(pkg)
        pkgmsgpath = pkgdir+"\\%s"%type+"\\*.%s"%type
        existed_msgpath = pkgdir+"\\src\\%s\\"%pkg+"\\%s"%type
        existed_pyinitpath = pkgdir+"\\src\\%s\\"%pkg
        #print(existed_msgpath)
        #print(pkgmsgpath)
        msglist = glob.glob(pkgmsgpath)
        #print type(msglist)
        #print(msglist)
        for msgfile in msglist:
            #msgfilepath = ["D:\\Dev\\winmaster\\trunk\\ros_comm\\clients\\rospy\\scripts\\genmsg_py.py","--noinitpy",msglist[0]]
            existed_msgfile = existed_msgpath + r"\_" + os.path.splitext(os.path.basename(msgfile))[0] + ".py"
            print("existed_msgfile : %s"%existed_msgfile)
            #redundancy check
            if(os.path.isfile(existed_msgfile)) == False:
                if(os.path.isdir(existed_msgpath)) == False:
                    os.makedirs(existed_msgpath)
                #msgfilepath = ["--noinitpy", msgfile]
                #print(msgfilepath)
                if type == "msg":
                    #genutilgen = genutil.Generator("genmsg_py","messages",".msg","msg",roslib.genpy.MsgGenerationException)
                    gen = genmsg_py.GenmsgPackage()
                    gen.generate(pkg, msgfile, existed_msgpath)
                    #genutil.genmain(msgfilepath, genmsg_py.GenmsgPackage())
                else:
                    gen = gensrv_py.SrvGenerator()
                    gen.generate(pkg, msgfile, existed_msgpath)
                    #genutil.genmain(msgfilepath, gensrv_py.SrvGenerator())
                
            else:
                print("skipped : %s"%msgfile)
        if len(msglist) > 0:
            #redundancy check
            existed_initfile = existed_pyinitpath + "__init__.py"
            existed_initfile2 = existed_pyinitpath + "//%s//"%type + "__init__.py"
            if(os.path.isfile(existed_initfile) == False or os.path.isfile(existed_initfile2) == False):
                #msgfilepath = ["genmsg_py.py","--initpy"]
                for msgfile in msglist:
                    #msgfilepath.append(os.path.normcase(msgfile))
                    if type == "msg":
                        gen = genutil.Generator("genmsg_py","messages",".msg","msg",roslib.genpy.MsgGenerationException)
                        gen.write_modules({pkg:os.path.normcase(msgfile)})
                        #genutil.genmain(msgfilepath, genmsg_py.GenmsgPackage())
                    else: 
                        gen = genutil.Generator("gensrv_py","services",".srv","srv",gensrv_py.SrvGenerationException)
                        gen.write_modules({pkg:os.path.normcase(msgfile)})
                        #genutil.genmain(msgfilepath, gensrv_py.SrvGenerator())
            else:
                print("skipped generation of python module init file : %s"%pkg)

def gen_msg_srv_cpp(list,type):
    for pkg in list:
        pkgdir = roslib.packages.get_pkg_dir(pkg)
        pkgmsgpath = pkgdir+"\\%s"%type+"\\*.%s"%type
        outputmsg_path = pkgdir+"\\%s_gen"%type+"\\cpp\\include\\%s"%pkg
        #print(pkgmsgpath)
        msglist = glob.glob(pkgmsgpath)
        #print(msglist)
        errcount = 0
        for msgfile in msglist:
            outputmsg_file = outputmsg_path + os.path.splitext(os.path.basename(msgfile))[0] + ".h"
            #print("outputmsg_file : %s"%outputmsg_file)
            #redundancy check
            if(os.path.isfile(outputmsg_file)) == False:
                msgfilepath = ["gen_msg_srv_cpp", msgfile]
                if type == "msg":
                    try :
                        msg_gen.generate_messages(msgfilepath)
                    except Exception:
                        print "*Error : Error was occurred while message header for c++"
                        errcount = errcount + 1
                elif type == "srv": 
                    try :
                        gensrv_cpp.generate(msgfile)
                    except Exception:
                        print "*Error : Error was occurred while service header for c++"
                        errcount = errcount + 1
            else:
                print("skipped : %s"%msgfile)
        if errcount == 0:
            generated_path = pkgdir+"\\%s_gen"%type
            create_generated_file(generated_path)
                    
def create_generated_file(path):
    if os.path.isdir(path) == True:
        msgfilepath = path + "\\generated"
        f = open(msgfilepath,'w')
        f.write('yes')
        f.close()

##############################################################################
# Main
##############################################################################

if __name__ == '__main__':
    sys.exit(genmsgMain(sys.argv, sys.stdout, os.environ))
