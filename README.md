# Markline

## Discribe
This tool help to get the distance on the image with the reference pixels.


## Requirement
> If you have never run the python code before, strongly reconmand you to install anaconda. It will make the installement more simple.

python=3.6
matplotlib
numpy


## Todo list
- [x] basic function
- [ ] UI
- [ ] load image from directory

## How to run
get the root to the this repo directory
run anaconda prompt,run the code by
> python mark_line_demo.py [the path of your image, you can drag the picture to the prompt to add the path]

And you can test by run 
> python mark_line_demo.py ./data/bone.jpeg

Then you should see like:
![image](https://github.com/ZhengXing-shawn/Markline/raw/master/images/bone_result_0.jpg)


## How to draw
#### Draw the reference line. Click two points to get a line. In the example the line was draw on o needle.(the needle length is set to 5cm)
![image](https://github.com/ZhengXing-shawn/Markline/raw/master/images/bone_result_1.jpg)

#### Press B on your keyboard. Click two points to draw the line on the object you want to konw the length.(We may mention it as Baseline after)
![image](https://github.com/ZhengXing-shawn/Markline/raw/master/images/bone_result_2.jpg)

#### Press N . Click one point to draw the first vertical line of Baseline
![image](https://github.com/ZhengXing-shawn/Markline/raw/master/images/bone_result_3.jpg)

#### Press M . Click one point to draw the second vertical line of Baseline
![image](https://github.com/ZhengXing-shawn/Markline/raw/master/images/bone_result_4.jpg)

#### Press Enter to see the result
![image](https://github.com/ZhengXing-shawn/Markline/raw/master/images/bone_result_5.jpg)

#### When drawing the line. Press J to hold the line. Combine with Zoomin to get a precision point.(Press J again to activate drawing)
![image](https://github.com/ZhengXing-shawn/Markline/raw/master/images/bone_result_7.jpg)


(Press Esc and you can start again)

(Press X and the result will be save on folder './data/result')


## Lisence 
MIT Lisence


## At the end
This tool is create for my best friend - Yipeng Lin.

Except the UI, there may not be any other function added in the future.