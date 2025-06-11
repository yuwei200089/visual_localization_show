from tkinter import filedialog
from os import path
from decimal import Decimal, ROUND_HALF_UP
import matplotlib.pyplot as plt

feature_order = ['surf', 'fast', 'brisk', 'kaze', 'superpoint', 'superglue', 'gift']    # 特徵順序

# 每張地圖的節點範圍，請依照順序排序
map_node_range = [[304, 732, 1076, 1440],    # SURF
                  [304, 732, 1076, 1440],    # FAST/BRIEIF
                  [304, 732, 1076, 1440],    # BRISK
                  [304, 732, 1076, 1440],    # KAZE
                  [304, 732, 1076, 1440],    # SuperPoint
                  [304, 732, 1076, 1440],    # SuperGlue
                  [304, 732, 1076, 1440]]    # GIFT

class FileAnalyze():
    def __init__(self):
        if len(load_file_path) == 0 : return
        self.count = [0]*len(load_file_path)
        self.location_count = [0]*len(load_file_path)
        self.content = None
        # 不能寫 "[[]]*變數" 因為這樣會讓裡面的子list都指向同一個位址，導致在進行內容修改或append的時候會連同其他子list也一起修改
        self.data_event = [[[] for _ in range(len(map_node_range))] for _ in range(len(load_file_path))] 

    def ReadFile(self, file_path):
        try:
            for index, path in enumerate(file_path):
                with open(path, 'r', encoding='utf-8') as file_obj:
                    while True:
                        self.content = file_obj.readline()
                        if self.content == '': break
                        # print(self.content.strip('\n'))
                        self.DataAnalyze(index)
                
            return self.count, self.location_count, self.data_event
        except:
            pass

    def DataAnalyze(self, index):
        self.content = self.content.strip('\n')
        if '-' not in self.content:
            self.count[index] += 1
            if self.content != '0':
                self.location_count[index] += 1
                for index_node, i in enumerate(map_node_range[index]) :
                    if int(self.content) <= i :
                        self.data_event[index][index_node].append(self.count[index]-0.5)
                        break
                
                if int(self.content) > map_node_range[index][len(map_node_range[index])-1] : print("超出節點範圍！！！")
                # if int(self.content) < 250 : self.data_event[0].append(self.count-0.5)
                # elif int(self.content) < 500: self.data_event[1].append(self.count-0.5)
                # elif int(self.content) < 750: self.data_event[2].append(self.count-0.5)
                # else : self.data_event[3].append(self.count-0.5)

class DrawPicture():
    def __init__(self):
        if len(load_file_path) == 0 : return
        self.fig, self.ax = plt.subplots(len(load_file_path), 1, figsize=(16, 5))
        # ax_width_inch = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted()).width-4.25
        fig_dpi = self.fig.dpi
        print(fig_dpi)
        ax_width_inch = 12.4 - 4.30
        # fig_dpi = 100
        # print(f"dpi {fig_dpi}, inch {ax_width_inch}")
        self.fig_width_px = ax_width_inch * fig_dpi

    def DrawEvent(self, data_event=[[]], i=0, multi_file=False, color_swich = 'all'):
            if len(map_node_range[i]) != len(location_color[color_swich]) : print(f"{self.filename}所設定的節點數與顏色數量不同！！"); return
            if multi_file:
                for j in range(len(map_node_range[i])):
                    self.ax[i].eventplot(data_event[j], lineoffsets=0, linewidths=self.points_per_x_unit, linelengths=0.5, colors=location_color[color_swich][j])
                self.ax[i].eventplot([0, count[i]], lineoffsets=0, linewidths=3, linelengths=1, colors=["black"])
            else:
                for j in range(len(map_node_range[i])):
                    self.ax.eventplot(data_event[j], lineoffsets=0, linewidths=self.points_per_x_unit, linelengths=0.5, colors=location_color[color_swich][j])
                self.ax.eventplot([0, count[i]], lineoffsets=0, linewidths=3, linelengths=1, colors=["black"])            

    def Show(self, data_event=[[]], percent=0, i=0, multi_file=False):
        self.points_per_x_unit = float(self.fig_width_px / count[i]+2)
        basename = path.basename(load_file_path[i])
        self.filename = path.splitext(basename)[0]
        s = str(*([picture_text[j] for j in picture_text.keys() if j.lower() in self.filename.lower()]))
        s = (s if s != '' else self.filename)
        color_swich = str(*[j for j in location_color.keys() if j in self.filename.lower()])
        # print(color_swich)
        self.DrawEvent(data_event, i, multi_file, color_swich=color_swich)
        if multi_file:
            self.ax[i].axis('off')
            pos = self.ax[i].get_position()
            self.ax[i].set_position([pos.bounds[0]+0.0, pos.bounds[1], pos.bounds[2], pos.bounds[3]])
            self.ax[i].text(-0.08, 0.49, s, fontsize=19, verticalalignment='center', horizontalalignment='center', transform=self.ax[i].transAxes)
            self.ax[i].text(1.02, 0.49, f'{percent} %', fontsize=19, verticalalignment='center', horizontalalignment='center', transform=self.ax[i].transAxes)
        else:
            self.ax.yaxis.set_major_locator(plt.MultipleLocator(2))
            plt.ylim(-2, 2)
            self.ax.axis('off')
            pos = self.ax.get_position()
            self.ax.set_position([pos.bounds[0]+0.0, pos.bounds[1], pos.bounds[2], pos.bounds[3]])
            self.ax.text(-0.08, 0.49, s, fontsize=19, verticalalignment='center', horizontalalignment='center', transform=self.ax.transAxes)
            self.ax.text(1.04, 0.49, f'{percent} %', fontsize=19, verticalalignment='center', horizontalalignment='center', transform=self.ax.transAxes)

if __name__ == '__main__':
    load_file_path = []
    load_file_path_buf = filedialog.askopenfilenames()
    for i in feature_order:
        for j in load_file_path_buf:
            if i in j : load_file_path.append(j); break
    # print(load_file_path)
    draw = DrawPicture()
    file = FileAnalyze()
    data_event_list = [[[]]]
    count = []
    location_count = []
    picture_text = {'gift':'GIFT', 'superpoint':'SuperPoint', 'superglue':'SuperGlue', 'fast':'FAST/BRIEF', 'brisk':'BRISK', 'kaze':'KAZE', 'surf':'SURF'} 
    location_color = {'1+3':["#1f77b4", "#01b07bff"], '2+4':["#fb4a4a", "#ce2dce"], 'all':["#1f77b4", "#fb4a4a", "#01b07bff", "#ce2dce"]}
    # location_color = plt.rcParams['axes.prop_cycle'].by_key()['color']
    strict_all = lambda x: bool(x) and all(x)
    # print(strict_all([1 if path.exists(j) else 0 for j in load_file_path]))
    if strict_all([1 if path.exists(j) else 0 for j in load_file_path]):
        count, location_count, data_event_list = file.ReadFile(load_file_path)
        for i in range(len(load_file_path)):
            location_percent = Decimal(str(location_count[i] / count[i] * 100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            draw.Show(data_event_list[i], location_percent, i, multi_file = (True if len(load_file_path) > 1 else False))
            print(count[i], location_count[i])
            print(location_percent)
        plt.show()
    else :
        print("找不到檔案")