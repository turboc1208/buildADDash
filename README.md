# buildADDash
build dashboards from HA views
This program works by reading the group files in HomeAssistant and creating a dashboard for each group with view set to yes in HomeAssistant.
Installation
<ol>
<li>Clone this repository to a directory in your AppDaemon app_dir
<li>Modify Room.tmp or create your own dashboard template.
<li>There are three key words in the template.
<ul>
<li> &ltroom&gt - this will be replaced with the name of the group being processed.
<li> &ltwidgets&gt - at this point the widgets associated with the entities in your group will be inserted.
<li> &ltlayout&gt - at this point the widgets inserted above will be included in the layout.
</ul>
<li>Modify your appdaemon.cfg file as follows.
<ul><li>[buildADDash]
<li>module=buildADDash
<li>class=buildADDash<br>
<i><b>Note</b>: I recommend that your output directory not be the dashboards directory.  Please point the output files to a directory where you can examine them and correct any issues in your template before copying them to your dashboard directory.</i>
<li>outputdir=/home/pi/appdaemon/conf/apps/buildADDash  (or wherever you want the output files to go)
<li>template=Room.tmp  (or whatever you called your template)</ul>
This file runs once and exits.  There are not any callback or schedules in it.  To run it simply go to the directory where the file is and type "touch buildADDash" and press enter.  This will make AppDaemon think the file has been changed and it will pick it up and run it.
