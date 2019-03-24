from matplotlib import pyplot as plt
from matplotlib import image as Image
import numpy as np
import math
import sys
import os

class LineBuilder():
    def __init__(self, scale, img_size ,line,line2,line3,line_paral_1,line_paral_2,text_1,line_ex1,line_ex2, line_relative, text_relative,result_name):

        self.line = line
        self.vertical_line_1 = line2
        self.vertical_line_2 = line3
        self.text_1 = text_1
        self.result_name = result_name


        self.line_paral_1 = line_paral_1
        self.line_paral_2 = line_paral_2


        self.line_ex1 = line_ex1
        self.line_ex2 = line_ex2


        self.line_relative = line_relative
        self.text_relative = text_relative

        self.line.set_linewidth(0.5)
        self.vertical_line_1.set_linewidth(0.5)
        self.vertical_line_2.set_linewidth(0.5)
        self.line_paral_1.set_linewidth(0.5)
        self.line_paral_2.set_linewidth(0.5)
        self.line_ex1.set_linewidth(0.5)
        self.line_ex2.set_linewidth(0.5)
        self.line_relative.set_linewidth(0.5)



        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.point_prev = [0, 0]
        self.point_update = [10, 11]
        self.press = None
        self.key = 0
        self.holding = None

        # scale == 1cm
        self.scale = float(scale)
        self.factor = round(float(img_size)/112,2)
        self.scale_pixel = 1
        self.enter_count = 0

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.line.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.line.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.line.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
        self.cidkeypress = self.line.figure.canvas.mpl_connect(
            'key_press_event', self.on_key_press)


    def on_press(self, event):
        print('operator:',self.key)
        if self.holding : 
            print('holding')
            return
        print('click', event)
        # if event.inaxes!=self.line.axes: return


        if self.key ==0:
        # draw the relative line
            relative_x = list(self.line_relative.get_xdata())
            relative_y = list(self.line_relative.get_ydata())
            print('relative_x',relative_x)

            if relative_x[0]==0:
                relative_x[0]=event.xdata
                relative_y[0]=event.ydata
                print('relative_x_sign',relative_x)
                self.line_relative.set_data(relative_x,relative_y)
                return

            elif len(relative_x)==1:
                relative_x.append(event.xdata)
                relative_y.append(event.xdata)

            else:
                point_distance_1 = np.sqrt( np.square(relative_x[0]-event.xdata) + np.square(relative_y[0]-event.ydata) )
                point_distance_2 = np.sqrt( np.square(relative_x[1]-event.xdata) + np.square(relative_y[1]-event.ydata) )

                if point_distance_1<=point_distance_2:
                    relative_x[0]=event.xdata
                    relative_y[0]=event.ydata
                else:
                    relative_x[1]=event.xdata
                    relative_y[1]=event.ydata

            self.line_relative.set_data(relative_x,relative_y)
            self.line_relative.figure.canvas.draw()

            self.scale_pixel = np.sqrt( np.square(relative_x[0] -relative_x[1]) + np.square(relative_y[0] - relative_y[1]))

            # t = 'pixels:'+ str(round(self.scale_pixel,2)) + '\n' + 'scale:' +str(self.scale)+'cm'
            # t =  str(self.scale)+'cm'
            t = ''
            self.text_relative.set_text(t)
            self.text_relative.set_position( [(relative_x[0]+relative_x[1])/2, (relative_y[0]+relative_y[1])/2 ])
            self.text_relative.figure.canvas.draw()

        if self.key =='b':
        # draw the basic line
            if len(self.xs)==2:
                self.xs = list(self.line.get_xdata())
                self.ys = list(self.line.get_ydata())

                x1 = self.xs[0]
                x2 = self.xs[1]
                x3 = event.xdata
                y1 = self.ys[0]
                y2 = self.ys[1]
                y3 = event.ydata

                slope_12 = (y2-y1)/(x2-x1+1e-5)
                slope_13 = (y3-y1)/(x3-x1+1e-5)
                rate = np.abs(slope_13/(slope_12+1e-5))
                print('slope_12:',slope_12)
                print('slope_13:',slope_13)
                print('rate',rate)

                # if x3>=min(x1,x2) and x3<=max(x1,x2) and y3>=min(y1,y2) and y3<=max(y1,y2) and rate<=1.4 and rate>=0.7:
                if (x3>=(min(x1,x2)-1) and x3<=(max(x1,x2)+1) and y3>=(min(y1,y2)-3) and y3<=(max(y1,y2)+3) ) and \
                 ( (rate<=1.4 and rate>=0.7) or (np.abs(slope_12)>10 and np.abs(slope_13)>10) or (np.abs(slope_12)< 0.1 and np.abs(slope_13)<0.1 ) ):
                    self.press = x3,y3
                    return

                else:
                    point_distance_1 = np.sqrt( np.square(self.xs[0]-event.xdata) + np.square(self.ys[0]-event.ydata) )
                    point_distance_2 = np.sqrt( np.square(self.xs[1]-event.xdata) + np.square(self.ys[1]-event.ydata) )

                    if point_distance_1<point_distance_2:
                        self.xs[0]=event.xdata
                        self.ys[0]=event.ydata
                    else:
                        self.xs[1]=event.xdata
                        self.ys[1]=event.ydata

                    self.line.set_data(self.xs, self.ys)

            else:
                if self.xs[0]==0:
                    self.xs[0] = event.xdata
                    self.ys[0] = event.ydata
                    self.line.set_data(self.xs, self.ys)
                    return
                else:
                    self.xs.append(event.xdata)
                    self.ys.append(event.ydata)
                    self.line.set_data(self.xs, self.ys)
            
            self.line.figure.canvas.draw()

        # draw vertical_line 1
        if self.key =='n':
            # check for the basic line existance
            self.xs = list(self.line.get_xdata())
            self.ys = list(self.line.get_ydata())
            if len(self.xs)!=2:
                return

            # draw vertical_line_1
            x1 = self.xs[0]
            x2 = self.xs[1]
            y1 = self.ys[0]
            y2 = self.ys[1]

            x3 = event.xdata
            y3 = event.ydata

            slope_12 = (y1-y2)/(x1-x2+1e-5)
            slope_34 = -1/(slope_12+1e-5)

            x4 = (y1-y3+x3*slope_34 - x1*slope_12)/(slope_34 - slope_12+1e-5)
            y4 = y1 + (x4-x1)*slope_12

            self.vertical_line_1.set_data([x3,x4],[y3,y4])
            self.vertical_line_1.figure.canvas.draw()

        # draw vertical_line 2
        if self.key =='m':
            # check for the basic line existance
            self.xs = list(self.line.get_xdata())
            self.ys = list(self.line.get_ydata())
            if len(self.xs)!=2:
                return

            # draw vertical_line_1
            x1 = self.xs[0]
            x2 = self.xs[1]
            y1 = self.ys[0]
            y2 = self.ys[1]

            x3 = event.xdata
            y3 = event.ydata

            slope_12 = (y1-y2)/(x1-x2+1e-5)
            slope_34 = -1/(slope_12+1e-5)

            x4 = (y1-y3+x3*slope_34 - x1*slope_12)/(slope_34 - slope_12+1e-5)
            y4 = y1 + (x4-x1)*slope_12

            self.vertical_line_2.set_data([x3,x4],[y3,y4])
            self.vertical_line_2.figure.canvas.draw()


    def on_motion(self, event):
        if self.press is None: return
        
        x3 , y3 = self.press
        dx = event.xdata - x3
        dy = event.ydata - y3
        self.xs = self.xs +dx
        self.ys = self.ys +dy 
        self.line.set_data(self.xs,self.ys)
        self.line.figure.canvas.draw()
        self.press = event.xdata, event.ydata
        print('motion')


    def on_release(self, event):
        if self.press is None: return

        self.press = None
        print('release')


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.line.figure.canvas.mpl_disconnect(self.cidpress)
        self.line.figure.canvas.mpl_disconnect(self.cidrelease)
        self.line.figure.canvas.mpl_disconnect(self.cidmotion)
        self.line.figure.canvas.mpl_disconnect(self.cidkeypress)


    def on_key_press(self, event):
        print('key_press',event)
        print(event.key)
        if event.key == '0':
            self.key=0
        if event.key == 'b':
            self.key='b'
        if event.key == 'n':
            self.key='n'
        if event.key == 'm':
            self.key='m'
        if event.key == 'escape':

            self.key=0
            self.enter_count=0

            self.line.set_data([0],[0])
            self.vertical_line_1.set_data([0],[0])
            self.vertical_line_2.set_data([0],[0])
            self.text_1.set_text('')

            self.line_paral_1.set_data([0],[0])
            self.line_paral_2.set_data([0],[0])


            self.line_ex1.set_data([0],[0])
            self.line_ex2.set_data([0],[0])
            self.line_relative.set_data([0],[0])
            self.text_relative.set_text('')

            self.line.figure.canvas.draw()
            self.vertical_line_1.figure.canvas.draw()
            self.vertical_line_2.figure.canvas.draw()
            self.text_1.figure.canvas.draw()

            self.line_paral_1.figure.canvas.draw()
            self.line_paral_2.figure.canvas.draw()

            self.line_ex1.figure.canvas.draw()
            self.line_ex2.figure.canvas.draw()
            self.line_relative.figure.canvas.draw()
            self.text_relative.figure.canvas.draw()

            print('clear done!')
        if event.key == 'enter':
            line_v1_x_list = list(self.vertical_line_1.get_xdata())
            left_x = line_v1_x_list[1]
            line_v2_x_list = list(self.vertical_line_2.get_xdata())
            right_x = line_v2_x_list[1]
            line_v1_y_list = list(self.vertical_line_1.get_ydata())
            left_y = line_v1_y_list[1]
            line_v2_y_list = list(self.vertical_line_2.get_ydata())
            right_y = line_v2_y_list[1]

            distance = np.sqrt( np.square(left_x - right_x) + np.square(left_y - right_y))
            real_distance = (distance / self.scale_pixel) * self.scale 
            print('real_distance:',real_distance)

            real_distance = round(real_distance,2)
            t = str(real_distance)+'mm'

            
            slope_12 = -(right_y - left_y)/(right_x -left_x+1e-5)
            # self.text_1.set_position([(left_x+right_x)/2 -2.5 ,(left_y+right_y)/2-6])
            param_move_text = np.sqrt( np.square(2.5*2) /(np.square(slope_12)+1) ) * self.factor
            self.text_1.set_position([(left_x+right_x)/2 - param_move_text*slope_12 ,(left_y+right_y)/2- param_move_text])
            # self.text_1.set_position([(left_x+right_x)/2 - 7*slope_12 ,(left_y+right_y)/2-7])
            self.text_1.set_text(t)
            self.text_1.set_rotation( (np.arctan(slope_12)/math.pi)*180 )
            self.text_1.figure.canvas.draw()

            pixels = np.sqrt((right_x- left_x)**2 + (right_y - left_y)**2)
            print('pixels_distance',pixels)

            if pixels > 15*self.factor:

                paral_rate = 1 - 15*self.factor / pixels

                param_move_bar = np.sqrt( np.square(1.6*2) /(np.square(slope_12)+1) )*self.factor
                
                if line_v1_x_list[1]<line_v2_x_list[1]:
                    inverse=1
                elif line_v1_x_list[1]>line_v2_x_list[1]:
                    inverse=-1
                self.line_paral_1.set_data([line_v1_x_list[1] - param_move_bar*slope_12 , line_v1_x_list[1] + inverse*1/2*(distance-16*self.factor)/np.sqrt(1+slope_12**2) - param_move_bar*slope_12 ],
                                            [line_v1_y_list[1] -param_move_bar,line_v1_y_list[1] - inverse*1/2*(distance-16*self.factor)/np.sqrt(1+slope_12**2)*slope_12 - param_move_bar ])
                self.line_paral_1.figure.canvas.draw()

                self.line_paral_2.set_data([line_v2_x_list[1] - param_move_bar*slope_12 , line_v2_x_list[1] - inverse*1/2*(distance-16*self.factor)/np.sqrt(1+slope_12**2) - param_move_bar*slope_12 ],
                                            [line_v2_y_list[1] - param_move_bar,line_v2_y_list[1] + inverse*1/2*(distance-16*self.factor)/np.sqrt(1+slope_12**2)*slope_12 - param_move_bar ])
                self.line_paral_2.figure.canvas.draw()

            else:
                self.line_paral_1.set_data([0],[0])
                self.line_paral_1.figure.canvas.draw()
                self.line_paral_2.set_data([0],[0])
                self.line_paral_2.figure.canvas.draw()



            print('slope_12',slope_12)

            # judge the side of line2 & line3
            # param_move_ex = np.sqrt( np.square(4*2) /(np.square(slope_12)+1) )*self.factor
            param_move_ex = np.sqrt( np.square(2*2) /(np.square(slope_12)+1) )*self.factor

            if slope_12 >= 0 :
                if line_v1_x_list[1]>=line_v1_x_list[0]:
                # if -(line_v1_x_list[1] - line_v1_x_list[0])/(line_v1_y_list[1] - line_v1_y_list[0]+1e-5)<=0:
                    self.line_ex1.set_data([line_v1_x_list[1],line_v1_x_list[1] + param_move_ex*slope_12],
                                                [line_v1_y_list[1],line_v1_y_list[1] + param_move_ex])
                elif line_v1_x_list[1]<line_v1_x_list[0]:
                    self.line_ex1.set_data([line_v1_x_list[1],line_v1_x_list[1] - param_move_ex*slope_12],
                                                [line_v1_y_list[1],line_v1_y_list[1] - param_move_ex])

                if line_v2_x_list[1]>=line_v2_x_list[0]:
                    self.line_ex2.set_data([line_v2_x_list[1],line_v2_x_list[1] + param_move_ex*slope_12],
                                            [line_v2_y_list[1],line_v2_y_list[1]+ param_move_ex])
                elif line_v2_x_list[1]<line_v2_x_list[0]:
                    self.line_ex2.set_data([line_v2_x_list[1],line_v2_x_list[1] - param_move_ex*slope_12],
                                            [line_v2_y_list[1],line_v2_y_list[1]- param_move_ex])

            elif slope_12 < 0:
                if line_v1_x_list[1]>=line_v1_x_list[0]:
                # if -(line_v1_x_list[1] - line_v1_x_list[0])/(line_v1_y_list[1] - line_v1_y_list[0]+1e-5)<=0:
                    self.line_ex1.set_data([line_v1_x_list[1],line_v1_x_list[1] - param_move_ex*slope_12],
                                                [line_v1_y_list[1],line_v1_y_list[1] - param_move_ex])
                elif line_v1_x_list[1]<line_v1_x_list[0]:
                    self.line_ex1.set_data([line_v1_x_list[1],line_v1_x_list[1] + param_move_ex*slope_12],
                                                [line_v1_y_list[1],line_v1_y_list[1] + param_move_ex])

                if line_v2_x_list[1]>=line_v2_x_list[0]:
                    self.line_ex2.set_data([line_v2_x_list[1],line_v2_x_list[1] - param_move_ex*slope_12],
                                            [line_v2_y_list[1],line_v2_y_list[1]- param_move_ex])
                elif line_v2_x_list[1]<line_v2_x_list[0]:
                    self.line_ex2.set_data([line_v2_x_list[1],line_v2_x_list[1] + param_move_ex*slope_12],
                                            [line_v2_y_list[1],line_v2_y_list[1]+ param_move_ex])



           
            self.line_ex1.figure.canvas.draw()
            self.line_ex2.figure.canvas.draw()

            if self.enter_count==0:
                self.enter_count +=1
            else:
                self.text_relative.set_text('')
                self.text_relative.figure.canvas.draw()
                self.line_relative.set_data([0],[0])
                self.line_relative.figure.canvas.draw()

                self.text_1.set_text('')
                self.text_1.figure.canvas.draw()
                self.line_paral_1.set_data([0],[0])
                self.line_paral_2.set_data([0],[0])
                self.line_paral_1.figure.canvas.draw()
                self.line_paral_2.figure.canvas.draw()


        if event.key == 'j':
            if self.holding:
                self.holding = False
            else:
                self.holding = True


        if event.key == 'x':
            exists_num = 0
            save_status = 0
            while save_status==0:
                result_name = './data/result/'+ self.result_name+'_result_'+str(exists_num)+'.png'
                if not os.path.exists(result_name):
                    plt.savefig(result_name,quality=100,dpi=800)
                    print('save_success')
                    print('file name:',result_name)
                    break
                else:
                    exists_num+=1
            # plt.savefig('./1.png',quality=100,dpi=800)
            # print('save_success')






# path = 'G:/Dataset/faces_emore/lfw/lfw_picture/1.jpg'

if not os.path.exists('./data/result/'):
    os.mkdir('./data/result')

path = sys.argv[1]
target = Image.imread(path)

sys_info = sys.platform
if sys_info == 'win32':
    result_name_list = path.split('\\')
if sys_info == 'darwin':
    result_name_list = path.split('/')

print(result_name_list)
result_name = result_name_list[-1].split('.')[0]
print(result_name)


if len(sys.argv)>2:
    scale = sys.argv[2]
else:
    scale = 50

img_size = int(np.sqrt((np.shape(target)[0]**2 + np.shape(target)[1]**2) /2))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(target)
ax.set_title('click to build line segments')

color_line = '#ff769c'
color_text = 'w'

line, = ax.plot([0], [0],color= color_line)  # empty line
line2, = ax.plot([0], [0],color=color_line)
line3, = ax.plot([0], [0],color=color_line)

line_paral_1, = ax.plot([0], [0],color=color_line)
line_paral_2, = ax.plot([0], [0],color=color_line)

line_ex1, = ax.plot([0], [0],color=color_line)
line_ex2, = ax.plot([0], [0],color=color_line)
# b_bar =ax.bar( [0],[0], color='k',align='center',linewidth=4)
text_1 = ax.text(5,5,'',ha='center',va='top',wrap=True,color=color_text)

line_relative, = ax.plot([0],[0],color=color_line)
text_relative = ax.text(5,5,'',ha='center',va='top',wrap=True,color=color_text)
lb = LineBuilder(scale,img_size,line,line2,line3,line_paral_1,line_paral_2,text_1,line_ex1,line_ex2,line_relative,text_relative,result_name)
lb.connect()

plt.show()
