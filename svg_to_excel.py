import csv
from bs4 import BeautifulSoup
import cv2
def read_svg(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'xml')  # Specify 'xml' parser for SVG
    return soup

svg_file_path = 'svg_images/10.svg'
svg_soup = read_svg(svg_file_path)

# Find and print text content within rect tags
texts = []
for rect in svg_soup.find_all('rect'):
    text_element = rect.find_next('text')
    print(text_element)
    text_content = text_element.get_text().strip() if text_element else ''
    x_coordinate = float(text_element.attrs['x'])
    y_coordinate = float(text_element.attrs['y'])
    width=float(rect.attrs['width'])
    # print(y_coordinate)
    texts.append((x_coordinate, y_coordinate,text_content,width))




row=[]
min_y=texts[0][1]
# get column names
header=[]
max_y=0
height=float(svg_soup.find_all('rect')[-1].attrs['height'])

for text in texts:

    y=text[1]
    if abs(y-min_y)<height:
        row.append(text)
    else:
        header.append(row)
        # print(row)

        min_y=y
        row=[]
        row.append(text)
       
    if len(header)==4:

       
        break


# img=cv2.imread("cropped/crop_21.jpg")

# organize column interval
col_cord={}
for ind,item in enumerate(sorted(header[3], key=lambda x: x[0])):
    x1=item[0]-item[3]/2
    x2=item[0]+item[3]/2
    print(item[2])
    col_cord[f"col{ind+1}"]=[x1,x2]
#     cv2.line(img,(int(x1),int(item[1])),(int(x2),int(item[1])),(0,0,255),1)
# cv2.imshow("img",img)
# cv2.waitKey(0)
col_cord['col1'][0]=0
col_cord['col3'][0]=col_cord['col3'][0]-20
print(col_cord)
# making table by checking x and y coordinates
sheet=[]
row=["","","","","","","","","",""]
for text in texts:
    
    available=False
    y=text[1]
    if abs(y-min_y)<height:
        for ind, col in enumerate(col_cord.values()):
            
            x1,x2=col
            x1_text=text[0]-text[3]/2
            x2_text=text[0]+text[3]/2
            if (x1<=x1_text and x1_text <= x2) or (x1<=x2_text and x2_text <= x2) or (x1_text<=x1 and x1<=x2_text) or (x1_text<=x2 and x2<=x2_text):
             
                row[ind]=text[2]
           
                break    
    else:
        sheet.append(row)
   

        min_y=y
        row=["","","","","","","","","",""]
        for ind, col in enumerate(col_cord.values()):
            x1,x2=col
            x1_text=text[0]-text[3]/2
            x2_text=text[0]+text[3]/2

            if (x1<=x1_text and x1_text <= x2) or (x1<=x2_text and x2_text <= x2) or (x1_text<=x1 and x1<=x2_text) or (x1_text<=x2 and x2<=x2_text):
             
                row[ind]=text[2]

                break

sheet.pop(0)

sheet.append(row)


# # Sort each group of 10 texts based on X-coordinates
# sorted_grouped_texts = [sorted(group, key=lambda x: x[0]) for group in content]

# # Extract only text content after sorting
# sorted_text_content = [[text[2] for text in group] for group in sorted_grouped_texts]

# Write to CSV file
csv_file_path = '10.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write grouped texts to CSV file
    csv_writer.writerows(sheet)
