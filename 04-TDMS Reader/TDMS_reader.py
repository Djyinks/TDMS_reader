from nptdms import TdmsFile
from matplotlib import pyplot as plt
import os
import time

start = time.time()
"""
Definition of customized class for reading TDMS files.

"""

# tdms_path = "/Users/fabricejeanneret/Documents/01-coding/04-TDMS Reader/01-test/raw1.tdms"
# tdms_path = "/Users/fabricejeanneret/Documents/01-coding/04-TDMS Reader/01-test/Recipe datalog/rec_datalog.tdms"
tdms_path = "/Users/fabricejeanneret/Documents/01-coding/04-TDMS Reader/01-test/DATALOG 20180717/DATALOG 20180717.tdms"


class TDMS_dj(object):

    def __init__(self, tdms_path):
        self.tdms_path = tdms_path
        self.file_name = path_leaf(self.tdms_path)
        self.file_dir = path_dir(self.tdms_path)
        self.tdms_file = TdmsFile(tdms_path)

    def get_groups(self):
        self.group_lst = self.tdms_file.groups()
        return self.group_lst

    def get_channels(self, grp_ind):
        self.chans_lst = self.tdms_file.group_channels(grp_ind)
        self.chans_lstout = []
        for ch in self.chans_lst:
            ch = str(ch)
            ch = ch[ch.find("'/'")+3:]
            if ch.find("\t") < 0:
                ch = ch[:ch.find("'>")]
            else:
                ch = ch[:ch.find("\t")]
            self.chans_lstout.append(ch)
        return self.chans_lstout

    def get_all_grps_chnls(self):
        self.grps = self.get_groups()
        self.grps_chans_dict = {}
        for grp in self.grps:
            self.grps_chans_dict[grp] = self.get_channels(grp)
        return self.grps_chans_dict

    def get_data(self, group, channel):
        return self.tdms_file.object(group, channel).data

    def conv_to_hdf(self):
        self.hdf_path = path_join_hdf(self.file_dir, self.file_name)
        self.tdms_file.as_hdf(self.hdf_path, mode='w', group='/')


def path_leaf(path):
    head, tail = os.path.split(path)
    return os.path.splitext(tail)[0]


def path_dir(path):
    return os.path.dirname(path)


def path_join_hdf(dir, file_name):
    return os.path.join(dir, file_name + '.hdf5')


tdms_file = TDMS_dj(tdms_path)
tdms_file.conv_to_hdf()

print tdms_file.get_channels(tdms_file.get_groups()[0])




"""
x = tdms_file.get_data('Data', 'Time')
y = tdms_file.get_data('Data', 'PECVD_F_input.ST_Vx2_PRES')
plt.plot(x, y)
plt.show()

print tdms_file.properties()

channel = tdms_file.object('Data', 'PECVD_F_input.CDGx')
data = channel.data
"""
end = time.time()
print end - start
