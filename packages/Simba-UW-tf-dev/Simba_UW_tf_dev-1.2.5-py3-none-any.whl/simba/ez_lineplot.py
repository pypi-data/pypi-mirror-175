__author__ = "Simon Nilsson", "JJ Choong"

import os
import cv2
import numpy as np
from configparser import ConfigParser, MissingSectionHeaderError, NoSectionError, NoOptionError
from simba.rw_dfs import read_df
from simba.drop_bp_cords import get_fn_ext
import pandas as pd
from simba.misc_tools import get_video_meta_data
from copy import deepcopy


# class DrawPathPlotWithoutConfig(object):
#     def __init__(self,
#                  data_path: str,
#                  video_path: str,
#                  body_part: str,
#                  bg_color: str,
#                  line_color: str,
#                  line_thinkness: int):
#
#         self.named_shape_colors = {'White': (255, 255, 255),
#                                    'Black': (0, 0, 0),
#                                    'Grey': (220, 200, 200),
#                                    'Red': (0, 0, 255),
#                                    'Dark-red': (0, 0, 139),
#                                    'Maroon': (0, 0, 128),
#                                    'Orange': (0, 165, 255),
#                                    'Dark-orange': (0, 140, 255),
#                                    'Coral': (80, 127, 255),
#                                    'Chocolate': (30, 105, 210),
#                                    'Yellow': (0, 255, 255),
#                                    'Green': (0, 128, 0),
#                                    'Dark-grey': (105, 105, 105),
#                                    'Light-grey': (192, 192, 192),
#                                    'Pink': (178, 102, 255),
#                                    'Lime': (204, 255, 229),
#                                    'Purple': (255, 51, 153),
#                                    'Cyan': (255, 255, 102)}
#         self.line_clr_bgr = self.named_shape_colors[line_color]
#         self.bg_clr_bgr = self.named_shape_colors[bg_color]
#         self.line_thinkness = line_thinkness
#         if self.line_clr_bgr == self.bg_clr_bgr:
#             print('SIMBA ERROR: The line color and background color are identical')
#             raise ValueError()
#         directory, file_name, ext = get_fn_ext(filepath=data_path)
#         if ext.lower() == '.h5':
#             self.data = pd.read_hdf(data_path)
#         elif ext.lower() == '.csv':
#             self.data = pd.read_csv(data_path)
#         else:
#             print('SIMBA ERROR: File type {} is not supported (OPTIONS: h5 or csv)'.format(str(ext)))
#             raise AttributeError()
#         self.data = self.data.loc[2:]
#         body_parts_available = [x[:-2] for x in self.data.columns]
#         self.col_heads = [body_part + '_x', body_part + '_y', body_part + '_likelihood']
#         if self.col_heads[0] not in self.data.columns:
#             print('SIMBA ERROR: Body-part {} is not present in the data file. The body-parts available are: {}'.format(body_part, body_parts_available))
#             raise ValueError
#         self.data = self.data[self.col_heads].astype(int).reset_index(drop=True)
#         video_meta_data = get_video_meta_data(video_path=video_path)
#         self.save_name = os.path.join(os.path.dirname(video_path), file_name + '_line_plot.mp4')
#         self.bg_image = np.zeros([video_meta_data['height'], video_meta_data['width'], 3])
#         self.bg_image[:] = self.named_shape_colors[bg_color]
#         self.bg_image = np.uint8(self.bg_image)
#         self.writer = cv2.VideoWriter(self.save_name, 0x7634706d, video_meta_data['fps'], (video_meta_data['width'], video_meta_data['height']))
#         self.cap = cv2.VideoCapture(video_path)
#         self.draw_video()
#
#
#     def draw_video(self):
#         frm_counter = 0
#         prior_x, prior_y = 0, 0
#         while (self.cap.isOpened()):
#             ret, frame = self.cap.read()
#             img =
#             if ret == True:
#                 current_x, current_y = self.data.loc[frm_counter, self.col_heads[0]], self.data.loc[frm_counter, self.col_heads[1]]
#                 if frm_counter > 0:
#                     cv2.line(self.bg_image, (prior_x, prior_y), (current_x, current_y), self.line_thinkness)
#                 prior_x, prior_y = deepcopy(current_x), deepcopy(current_y)
#
#
#
#
#
#


def draw_line_plot(configini,video,bodypart):
    configFile = str(configini)
    config = ConfigParser()
    try:
        config.read(configFile)
    except MissingSectionHeaderError:
        print('ERROR:  Not a valid project_config file. Please check the project_config.ini path.')
    configdir = os.path.dirname(configini)
    try:
        wfileType = config.get('General settings', 'workflow_file_type')
    except NoOptionError:
        wfileType = 'csv'
    dir_path, vid_name, ext = get_fn_ext(video)
    csvname = vid_name + '.' + wfileType
    tracking_csv = os.path.join(configdir, 'csv', 'outlier_corrected_movement_location', csvname)
    inputDf = read_df(tracking_csv, wfileType)
    videopath = os.path.join(configdir,'videos',video)
    outputvideopath = os.path.join(configdir, 'frames', 'output', 'simple_path_plots')

    if not os.path.exists(outputvideopath):
        os.mkdir(outputvideopath)

    #datacleaning
    colHeads = [bodypart + '_x', bodypart + '_y', bodypart + '_p']
    df = inputDf[colHeads].copy()

    widthlist = df[colHeads[0]].astype(float).astype(int)
    heightlist = df[colHeads[1]].astype(float).astype(int)
    circletup = tuple(zip(widthlist,heightlist))

    # get resolution of video
    vcap = cv2.VideoCapture(videopath)
    if vcap.isOpened():
        width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
        height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
        fps = int(vcap.get(cv2.CAP_PROP_FPS))
        totalFrameCount = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))

    # make white background
    img = np.zeros([height, width, 3])
    img.fill(255)
    img = np.uint8(img)


    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(os.path.join(outputvideopath,video), 0x7634706d, fps, (width,height))
    counter=0
    while (vcap.isOpened()):
        ret,frame = vcap.read()
        if ret == True:
            if counter !=0:
                cv2.line(img,circletup[counter-1],circletup[counter],5)

            lineWithCircle = img.copy()
            cv2.circle(lineWithCircle, circletup[counter],5,[0,0,255],-1)



            out.write(lineWithCircle)
            counter+=1
            print('Frame ' + str(counter) + '/' + str(totalFrameCount))

        else:
            break

    vcap.release()
    cv2.destroyAllWindows()
    print('Video generated.')


def draw_line_plot_tools(videopath,csvfile,bodypart):
    inputDf = pd.read_csv(csvfile)


    #restructure
    col1 = inputDf.loc[0].to_list()
    col2 = inputDf.loc[1].to_list()
    finalcol = [m+'_'+n for m,n in zip(col1,col2)]
    inputDf.columns = finalcol
    inputDf = inputDf.loc[2:]
    print(inputDf.columns)
    inputDf = inputDf.reset_index(drop=True)
    #datacleaning
    colHeads = [bodypart + '_x', bodypart + '_y', bodypart + '_likelihood']
    df = inputDf[colHeads].copy()

    widthlist = df[colHeads[0]].astype(float).astype(int)
    heightlist = df[colHeads[1]].astype(float).astype(int)
    circletup = tuple(zip(widthlist,heightlist))

    # get resolution of video
    vcap = cv2.VideoCapture(videopath)
    if vcap.isOpened():
        width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
        height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float
        fps = int(vcap.get(cv2.CAP_PROP_FPS))
        totalFrameCount = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))

    # make white background
    img = np.zeros([height, width, 3])
    img.fill(255)
    img = np.uint8(img)

    outputvideoname = os.path.join(os.path.dirname(videopath),'line_plot'+os.path.basename(videopath))
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(outputvideoname, 0x7634706d, fps, (width,height))
    counter=0
    while (vcap.isOpened()):
        ret,frame = vcap.read()
        if ret == True:
            if counter !=0:
                cv2.line(img,circletup[counter-1],circletup[counter],5)

            lineWithCircle = img.copy()
            cv2.circle(lineWithCircle, circletup[counter],5,[0,0,255],-1)



            out.write(lineWithCircle)
            counter+=1
            print('Frame ' + str(counter) + '/' + str(totalFrameCount))

        else:
            break

    vcap.release()
    cv2.destroyAllWindows()
    print('Video generated.')