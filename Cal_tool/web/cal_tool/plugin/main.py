from cal_tool.plugin.uhasselt.uhasselt import *

if __name__ == '__main__':

    uhasselt_plugin = UhasseltPlugin()



    temp = uhasselt_plugin.getSourcePlugin()

    print(temp.giveSources())







