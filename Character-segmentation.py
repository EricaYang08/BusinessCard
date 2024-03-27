import matplotlib.pyplot as plt
from PIL import Image
import math

# read image
img = plt.imread("1.jpg")
SecondImage = Image.open("1.jpg")

# fine the coordinators it have pixels with text
x_coordinator = []
y_coordinator = []
row_size = len(img)
column_size = len(img[0])

number_of_pixels = []
for i in range(row_size):
    count_of_small_area = 0
    for j in range(column_size):
        if img[i][j] > 100:
            y_coordinator.append(i)
            x_coordinator.append(j)
            count_of_small_area += 1
    number_of_pixels.append(count_of_small_area)

coordinator_size = len(x_coordinator)


# row indices
row_group = []
# PixelArraySize = len(number_of_pixels)  # always equals to RowSize
# set the threshold of the number of pixels.
# For here, we say that if the number of text pixels is larger than 1, it is a row with text
for i in range(row_size):
    if number_of_pixels[i] > 10:
        row_group.append(i)

final_row_val = [row_group[0]]
row_group_size = len(row_group)


# group the rows together
for j in range(row_group_size - 1):
    row_diff = abs(row_group[j] - row_group[j + 1])
    if row_diff > 1:
        final_row_val.append(row_group[j])
        final_row_val.append(row_group[j + 1])

last_row = row_group[-1]
final_row_val.append(last_row)


left_val_array = []
right_val_array = []

final_row_val_len = len(final_row_val) // 2

# find the left and the right borders
for i in range(final_row_val_len):
    left_val = column_size
    right_val = 0

    row_diff = final_row_val[2 * i + 1] - final_row_val[2 * i]
    for k in range(row_diff):
        current_row = final_row_val[2 * i] + k
        for j in range(coordinator_size):
            if y_coordinator[j] == current_row:
                if left_val > x_coordinator[j]:
                    left_val = x_coordinator[j]
                if right_val < x_coordinator[j]:
                    right_val = x_coordinator[j]
    left_val_array.append(left_val)
    right_val_array.append(right_val)

new_x_value = []
count_for = []


#find the left and right borders for each character
for i in range(final_row_val_len):
    count_of_small_area = 1
    b_top = final_row_val[2 * i]
    b_bottom = final_row_val[2 * i + 1]
    b_left = left_val_array[i]
    b_right = right_val_array[i]

    # text pixels
    current_x_value = []
    new_x_value.append(left_val_array[i])
    row_diff = b_bottom - b_top
    for k in range(row_diff):
        cur_row = b_top + k
        for j in range(coordinator_size):
            if y_coordinator[j] == cur_row:
                current_x_value.append(x_coordinator[j])
    current_x_value.sort()

    #find the noncontinuous x value. We think that if the x value is not continuous 
    change_size = len(current_x_value)
    for k in range(change_size - 1):
        if (current_x_value[k + 1] - current_x_value[k]) > 1:
            new_x_value.append(current_x_value[k])
            new_x_value.append(current_x_value[k + 1])
            count_of_small_area += 1


    new_x_value.append(b_right)
    count_for.append(count_of_small_area)
    #print("index", count_of_small_area)
    #print("NewXValue,:", new_x_value)
# plt.imshow(img)
# plt.show()
# exit()

#08/11/2021 Wenhui Yang
#final segmentation
start_index = 0
count_of_all_small_area = len(count_for)
ComparedVal = 0
AddedValue = []
AddedCount = []
AddedIndex = []
AddedCountNum = []
OriginalRemove = []
for z in range(final_row_val_len):
    count_of_current_big_area = count_for[z]
    if z > 0:
        start_index += count_for[z - 1] * 2

    for b in range(count_of_current_big_area):
        if(b == 0):
            ComparedVal = b + 1
        else:
            ComparedVal = b - 1
        left = new_x_value[start_index + 2 * b]
        right = min(column_size, new_x_value[start_index + 2 * b + 1] + 1)
        
        Comparedleft = new_x_value[start_index + 2 * ComparedVal]
        Comparedright = min(column_size, new_x_value[start_index + 2 * ComparedVal + 1] + 1)
        
        absComp = abs(Comparedleft-Comparedright)
        absOrig = abs(left-right)
        percent = math.ceil(absOrig/absComp)
        if(percent > 1):
            AddedCount.append(percent - 1)
            AddedCountNum.append(z)
            absOrig = absOrig/percent
            OriginalRemove.append(left)
            OriginalRemove.append(right-1)
            for i in range(percent-1):
                AddedIndex.append(start_index + 2 * b + i + 1)
                AddedValue.append(left+(i+1)*absOrig)
                AddedValue.append(left+(i+1)*absOrig)

  
#added the values to the final result               
for i in range(len(AddedIndex)):
    new_x_value.insert(AddedIndex[i],AddedValue[i])
    new_x_value.insert(AddedIndex[i]+1,AddedValue[i+1])

for i in range(len(AddedCountNum)):
    num = AddedCountNum[i]
    count_for[num] = count_for[num] + AddedCount[i]


#show or save the cropped images
#final result step
start_index = 0
count_of_all_small_area = len(count_for)
fpNameCount = 0
for i in range(final_row_val_len):
    count_of_current_big_area = count_for[i]
    if i > 0:
        start_index += count_for[i - 1] * 2

    for b in range(count_of_current_big_area):
        top = final_row_val[2 * i]
        bottom = min(row_size, final_row_val[2 * i + 1] + 1)
        left = new_x_value[start_index + 2 * b]
        right = min(column_size, new_x_value[start_index + 2 * b + 1] + 1)
        
        if(left > right):
            index = left
            left = right
            right = index
        
        #print("Left,top,right,bottom:", i, left, top, right, bottom)
        im1 = SecondImage.crop((left,top,right,bottom+1))
        fpName = str(fpNameCount) + ".png"
        fpNameCount = fpNameCount + 1
        im1.save(fpName)
       # plt.imshow(img[top:bottom, left:right])
       # plt.show()
        #im1.show()
#
# plt.imshow(img)
# plt.show()
