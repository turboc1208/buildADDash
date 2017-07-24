import appdaemon.appapi as appapi
import os

###############################
# build AppDaemonDash boards   PRE ALPHA (try at your own risk)  I have not tested much.
#
# assumptions:
# all group names follow the format room_<roomname>
# 
# because like me you could have numerous appdaemon groups and may only want to get the ones associated with rooms
#
# Setup in appdaemon.cfg file as follows
# buildADDash:
# module: buildADDash
# class: buildADDash
# outputdir: <where every you want the files written to>
# template: <template file name, must be placed in the outputdir
#
# I highly suggest writing the files out somewhere other than the dashboards directory so you can review them before
# moving them to the dashboards directory.  
#
# object types are based on home assistant types.  Some may not have been implemented in the dashboard yet.
#

class buildADDash(appapi.AppDaemon):

  def initialize(self):
     self.log("Hello from buildADDash")
     filedir=self.args["outputdir"]
     tmpname=self.args["template"]
     if not filedir[len(filedir)-1]=="/":
       filedir=filedir+"/"
     tmpname=filedir+tmpname
     self.log("tmpname={}".format(tmpname))
     for entity in self.get_state("group"):
       enttyp,name=self.split_entity(entity)
       if name[:4]=="room":
         roomname=filedir + name[5:] +".dash"
         self.log("entity={}, roomanme={}".format(entity,roomname))
         fout=open(roomname,"wt")
         with open(tmpname,"rt") as fin:
           for inline in fin:
             self.log("inline={}".format(inline))
             self.log("<room> is at {}".format(inline.find("<room>")))
             if inline.find("<room>")>=0:
               t=""
               t=inline[:inline.find("<room>")]
               self.log("t={}".format(t))
               t=t+name[5:]+inline[inline.find("<room>")+6:]
               fout.write("{}".format(t))
             elif inline.find("<widgets>")>=0:
               entlist=self.build_entity_list(entity)
               self.log("entlist={}".format(entlist))
               for membername in entlist:
                 memtype, memname = self.split_entity(membername)
                 fout.write("{}:\n".format(memname))
                 fout.write("    widget_type: {}\n".format(memtype))
                 fout.write("    entity: {}\n".format(membername))
                 fout.write("    title: {}\n".format(memname.replace('_',' ')))
             elif inline.find("<layout>")>=0:
               entlist=self.build_entity_list(entity)
               i=0
               y=len(entlist)
               for membername in entlist:
                 if i==0:
                   fout.write("    - ")
                 memtype, memname = self.split_entity(membername)
                 fout.write("{}(1x1)".format(memname))
                 i=i+1
                 y=y-1
                 if i==8:
                   fout.write("\n")
                   i=0
                 else:
                   if y>0:
                     fout.write(", ")
               fout.write("\n")
             else:
               fout.write("{}".format(inline)) 

         fout.close()
         fin.close()

  ######################
  #
  # build_entity_list (self, ingroup, inlist - optional: defaults to all entity types))
  #
  # build a list of all of the entities in a group or nested hierarchy of groups
  #
  # ingroup = Starting group to cascade through
  # inlist = a list of the entity types the list may contain.  Use this if you only want a list of lights and switches for example.
  #            this would then exclude any input_booleans, input_sliders, media_players, sensors, etc. - defaults to all entity types.
  #
  # returns a python list containing all the entities found that match the device types in inlist.
  ######################
  def build_entity_list(self,ingroup,inlist=['all']):
    retlist=[]
    types=[]
    typelist=[]

    # validate values passed in
    if not self.entity_exists(ingroup):
      self.log("entity {} does not exist in home assistant".format(ingroup))
      return None
    if isinstance(inlist,list):
      typelist=inlist
    else:
      self.log("inlist must be a list ['light','switch','media_player'] for example")
      return None

    # determine what types of HA entities to return
    if "all" in typelist:
      types=["all"]
    else:
      types= types + typelist
      types.append("group")            # include group so that it doesn't ignore child groups

    # check the device type to see if it is something we care about
    devtyp, devname = self.split_entity(ingroup)
    if (devtyp in types) or ("all" in types):                # do we have a valid HA entity type
      if devtyp=="group":                                    # entity is a group so iterate through it recursing back into this function.
        for entity in self.get_state(ingroup,attribute="all")["attributes"]["entity_id"]:
          newitem=self.build_entity_list(entity,typelist)    # recurse through each member of the child group we are in.
          if not newitem==None:                              # None means there was a problem with the value passed in, so don't include it in our output list
            retlist.extend(newitem)                          # all is good so concatenate our lists together
      else:
        retlist.append(ingroup)                                      # actual entity so return it as part of a list so it can be concatenated
    return retlist


