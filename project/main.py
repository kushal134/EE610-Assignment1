
#import the necessary libraries
import tkinter as tk                            #main tkinter 
from tkinter import filedialog as fd   #to open and save files
from tkinter.constants import CENTER      #for centering the buttons
from tkinter.messagebox import showinfo         #to show info
from PIL import Image, ImageTk                  #Pillow lib for displaying images
import cv2                                      #opencv for rbg to hsv conversion
import numpy as np

window = tk.Tk()                                #create a window instance
window.geometry('1000x1000')                    #set window size
window.title("Basic Image Editor")              #set window title

image_disp=tk.Label(window,image = '')          #label which will display the image
image_disp.place(relx=0.5, rely=0.6, anchor=CENTER) #place the label in the center (relative positioning)

#--------------------------------------------------------------------------------------
#Select file function to select a particular image file
def select_file():
    file_types = (                                 #specifiying allowed file types
        ('JPG files', '*.jpg'),                    #jpg
        ('PNG files', '*.png'),                    #png 
        ('JPEG files', '*.jpeg'),                  #jpeg
    )       
    filename = fd.askopenfilename(                  #to open a file
        title = "Open a file",                      #title
        initialdir='/C:/Users/HP/Desktop/Kushal/Semester5', #inital director - can be anything 
        filetypes=file_types                        #only the above mentioned file types are allowed
    )
    
    showinfo(
        title = "Selected file",                    #On selecting a file, show the title
        message = filename                          #message
    )

    im_store = []                                   #list to store the images after enhancement, for undo 
    im = Image.open(filename)                       #open the image using the given file name
    width, height = im.size                         #get the width and heigth
    newsize = (int(width/height*300), 300)          #new size, where height is fixed and width is prop to originial dimensions
    im = im.resize(newsize)                         #resize the image
    im_arr = np.array(im)                           #convert to np array for image manipulations
    im_store.append(im_arr)                         #append to the list


    tkimage = ImageTk.PhotoImage(im)                #to display the image

    image_disp.configure(image = tkimage)           #configure the lable with the image
    image_disp.image = tkimage                      #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center

    #The buttons and their functions
    #Log transform
    log_button = tk.Button(                         #Convert log button                
    window,                                         #mention the given window
    text = "Log Transform",                         #Title of the button
    command=lambda: convert_log(im_store)           #Specify the function which is called upon clicking
    )
    log_button.place(relx=0.25, rely=0.7, anchor=CENTER) #Place the button 
    

    #Gamma transform
    gamma_button = tk.Button(                       #Gamma Transform button                
    window,                                         #mention the given window
    text = "Gamma Transform",                       #Title of the button
    command=lambda: convert_gamma(im_store,input_gamma)         #Specify the function which is called upon clicking
    )
    gamma_button.place(relx=0.35, rely=0.7, anchor=CENTER) #Place the button 
    
    input_gamma = tk.Text(window, height = 2,width = 10)  #input gamma button
    input_gamma.place(relx=0.35, rely=0.75, anchor=CENTER) #place the window

    #Blurring 
    blurring_button = tk.Button(                    #Blurring button                
    window,                                         #mention the given window
    text = "Blurring",                              #Title of the button
    command=lambda: convert_blurring(im_store,input_blurring)      #Specify the function which is called upon clicking
    )
    blurring_button.place(relx=0.45, rely=0.7, anchor=CENTER) #Place the button 
    
    input_blurring = tk.Text(window,height = 2,width = 10) #input blurring window
    input_blurring.place(relx=0.45, rely=0.75, anchor=CENTER) #place the window
    
    #Histogram equalise 
    eql_button = tk.Button(                 #Histogram equalise button                
    window,                                         #mention the given window
    text = "Histogram Equalise",                    #Title of the button
    command=lambda: convert_eql(im_store)           #Specify the function which is called upon clicking
    )
    eql_button.place(relx=0.55, rely=0.7, anchor=CENTER) #Place the button 

    sharpen_button = tk.Button(                     #Sharpen button  
    window,                                         #mention the given window
    text = "Sharpen",                               #Title of the button
    command=lambda: convert_sharpen(im_store,input_sharpen)       #Specify the function which is called upon clicking
    )
    sharpen_button.place(relx=0.65, rely=0.7, anchor=CENTER) #Place the button 

    input_sharpen = tk.Text(window,height = 2,width = 10)   #input sharpen button for extent
    input_sharpen.place(relx=0.65, rely=0.75, anchor=CENTER) #place the button

    negative_button = tk.Button(                     #Sharpen button  
    window,                                         #mention the given window
    text = "Negative of the image",                               #Title of the button
    command=lambda: convert_negative(im_store)       #Specify the function which is called upon clicking
    )
    negative_button.place(relx=0.75, rely=0.7, anchor=CENTER) #Place the button 

    #Undo once button
    undo_once_button = tk.Button(                   #Undo once button
    window,                                         #mention the given window
    text = "Undo once ",                            #Title of the button
    command=lambda: convert_undo_once(im_store)     #Specify the function which is called upon clicking
    )
    undo_once_button.place(relx=0.45, rely=0.8, anchor=CENTER) #Place the button
    
    #Undo all button
    undo_all_button = tk.Button(                    #Undo all button
    window,                                         #mention the given window
    text = "Undo all ",                             #Title of the button
    command=lambda: convert_undo_all(im_store)      #Specify the function which is called upon clicking
    )
    undo_all_button.place(relx=0.55, rely=0.8, anchor=CENTER) #Place the button

    save_button = tk.Button(                        #Save button
    window,                                         #mention the given window
    text="save as",                                 #Title of the button
    command=lambda:savefile(im_store)               #Specify the function which is called upon clicking
    )
    save_button.place(relx=0.5, rely=0.9, anchor=CENTER) #Place the button

#Button function definitions
def savefile(im_store):
    """
    This function is for saving a file
    """
    filename = fd.asksaveasfile(mode='w', defaultextension=".jpg") #Ask for a file name
    im = Image.fromarray(im_store[-1])                             #use the latest inage from the array
    if im.mode != 'RGB':                                           #If the image is bw then convert to rgb 
        im = im.convert('RGB')                           
    im.save(filename)                                              #Save the file using the given filename

def convert_log(im_store):
    """
    This function is for log transformation
    """
    im_arr = im_store[-1]                           #Use the latest image from the list
    if im_arr.ndim == 3:
        im_temp = cv2.cvtColor(im_arr, cv2.COLOR_BGR2HSV)   #Convert to HSV
        intensity = im_temp[:,:,2]                          #Manipulate the intensity values
    else:      
        intensity = im_arr                         #use the entire array for bw

    #log transform
    intensity = intensity.astype('uint64')          #Convert to int64 for preventing overflow
    log_val = np.log(intensity + 1)*255/(np.log(np.max(intensity) + 1)) #Log transform
    intensity = log_val.astype('uint8')            #Convert back to int8                   
    
    if im_arr.ndim == 3:
        im_temp[:,:,2] = intensity                  #store the transformed values
        im_conv_arr = cv2.cvtColor(im_temp, cv2.COLOR_HSV2BGR)  #Convert back to RGB                        
    else:
        im_conv_arr = intensity                       #if BW no conversion needed
    
    
    im_conv = Image.fromarray(im_conv_arr)          #Convert back to image
    im_store.append(im_conv_arr)                    #Append the latest transformed image to the list
    tkimage = ImageTk.PhotoImage(im_conv)           #To display image
    print(f"Length of array = {len(im_store)}")

    image_disp.configure(image = tkimage)           #configure the lable with the image
    image_disp.image = tkimage                      #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center





def convert_undo_once(im_store):
    """
    This function is for undo once
    """
    im_store.pop()                      #pop the list (remove the last element)
    im_arr = im_store[-1]               #now take the last image from the array
    print(f"Length of array = {len(im_store)}")
    im = Image.fromarray(im_arr)        #Convert back to image
    tkimage = ImageTk.PhotoImage(im)    #To display image

    image_disp.configure(image = tkimage)               #configure the lable with the image
    image_disp.image = tkimage                          #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center

def convert_undo_all(im_store):
    """
    This function is for undoing all transformations
    """
    for i in range(len(im_store) - 1):
        im_store.pop()
    im_arr = im_store[0]                #Just take the first element (ie the original image)
    
    print(f"Length of array = {len(im_store)}")
    im = Image.fromarray(im_arr)        #Convert back to image
    tkimage = ImageTk.PhotoImage(im)    #To display image

    image_disp.configure(image = tkimage)               #configure the lable with the image
    image_disp.image = tkimage                          #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center


def convert_gamma(im_store,input_gamma):
    """
    This function is for gamma trasnformation
    """
    
    im_arr = im_store[-1]                           #Use the latest image from the list
    if im_arr.ndim == 3:
        im_temp = cv2.cvtColor(im_arr, cv2.COLOR_BGR2HSV)   #Convert to HSV
        intensity = im_temp[:,:,2]                          #Manipulate the intensity values
    else:      
        intensity = im_arr                         #use the entire array for bw

    gamma = float(input_gamma.get(1.0, "end-1c"))   #Take the value of gamma from the input_gamma box and convert to float
    intensity = np.power(intensity/255,gamma)*255   #Gamma transform

    if im_arr.ndim == 3:                            #if rgb image   
        im_temp[:,:,2] = intensity                  #store the transformed values
        im_conv_arr = cv2.cvtColor(im_temp, cv2.COLOR_HSV2BGR)  #Convert back to RGB                        
    else:
        im_conv_arr = intensity                     #if BW no conversion needed
    
    im_conv = Image.fromarray(im_conv_arr)              #Convert back to image
    im_store.append(im_conv_arr)                        #Append the latest transformed image to the list
    tkimage = ImageTk.PhotoImage(im_conv)               #To display image

    image_disp.configure(image = tkimage)               #configure the lable with the image
    image_disp.image = tkimage                          #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center


def convert_blurring(im_store,input_blurring):
    """
    This function is for blurring
    """
    im_arr = im_store[-1]                           #Use the latest image from the list

    if im_arr.ndim == 3:
        im_temp = cv2.cvtColor(im_arr, cv2.COLOR_BGR2HSV)   #Convert to HSV
        intensity = im_temp[:,:,2]                          #Manipulate the intensity values
    else:      
        intensity = im_arr                         #use the entire array for bw

    extent = int(input_blurring.get(1.0, "end-1c")) #Use the value from input_blurring to get the extent of blurring
    int_padded =np.pad(intensity, extent, 'constant', constant_values=(0)) #Pad the array for convolution
    b = np.zeros(intensity.shape)                   #This will be the array for stroing the modified values
    rows = intensity.shape[0]                       #get the rows
    cols = intensity.shape[1]                       #get the columns
    #We will vectorise our operations. The below for loop is for generating 9 addition
    #(for each of the 3*3 window - this is for extent = 1)
    #We will add entire matrices together after scaling them approp
    for i in range(2*extent + 1):                    #loop over i
        for j in range(2*extent + 1):                #loop over j
            b = b + int_padded[i:i+rows,j:j+cols]/((2*extent + 1)**2) #take the particular submatrix of the padded one and divide it by the weights
    
    
    if im_arr.ndim == 3:                            #if rgb image   
        im_temp[:,:,2] = b                  #store the transformed values
        im_conv_arr = cv2.cvtColor(im_temp, cv2.COLOR_HSV2BGR)  #Convert back to RGB                        
    else:
        im_conv_arr = b                     #if BW no conversion needed

    im_conv = Image.fromarray(im_conv_arr)              #Convert back to image
    im_store.append(im_conv_arr)                        #Append the latest transformed image to the list
    tkimage = ImageTk.PhotoImage(im_conv)               #To display image

    image_disp.configure(image = tkimage)               #configure the lable with the image
    image_disp.image = tkimage                          #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center

def convert_sharpen(im_store,input_sharpen):
    """
    This function is to apply sharpening to the inage
    """
    im_arr = im_store[-1]                           #Use the latest image from the list
    extent = int(input_sharpen.get(1.0, "end-1c")) #Use the value from input_blurring to get the extent of blurring
    if im_arr.ndim == 3:
        im_temp = cv2.cvtColor(im_arr, cv2.COLOR_BGR2HSV)   #Convert to HSV
        intensity = im_temp[:,:,2]                          #Manipulate the intensity values
    else:      
        intensity = im_arr                         #use the entire array for bw
    
    intensity = intensity.astype('float64')         #convert to float for image manipulations
    intensity = intensity/np.max(intensity)         #scale it down from 0-255 to 0-1
    
    int_padded =np.pad(intensity, extent, 'constant', constant_values=(0)) #Pad the array for convolution
    b = np.zeros(intensity.shape) #this will have the convolved values
    rows = intensity.shape[0]     #rows
    cols = intensity.shape[1]     #columns
    #We will vectorise our operations. The below for loop is for generating 9 addition
    #(for each of the 3*3 window - this is for extent = 1)
    #We will add entire matrices together after scaling them approp
    for i in range(2*extent + 1):           #loop over rows
        for j in range(2*extent + 1):       #loop over columns
            if(i == extent and j == extent):    #if central pixel
                b = b + int_padded[i:i+rows,j:j+cols]*(-((2*extent + 1)**2 - 1)) #multiply by the weight
            else:
                b = b + int_padded[i:i+rows,j:j+cols]  

    b = b/((2*extent + 1)**2 - 1)  #scale down by the center weight
    a = intensity + 0.5*b          #add it to original image
    a = a*255/np.max(a)            #scale it up by 255
    a = np.clip(a, 0, 255)         #clip the values which are <0 or >255
    a = a.astype('uint8')          #convert to uint8
    if im_arr.ndim == 3:                    #if rgb image   
        im_temp[:,:,2] = a                  #store the transformed values
        im_conv_arr = cv2.cvtColor(im_temp, cv2.COLOR_HSV2BGR)  #Convert back to RGB                        
    else:
        im_conv_arr = a                     #if BW no conversion needed

    im_conv = Image.fromarray(im_conv_arr)              #Convert back to image
    im_store.append(im_conv_arr)                        #Append the latest transformed image to the list
    tkimage = ImageTk.PhotoImage(im_conv)               #To display image

    image_disp.configure(image = tkimage)               #configure the lable with the image
    image_disp.image = tkimage                          #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center

def convert_eql(im_store):
    """
    This function is for histogram equalisation
    """
    im_arr = im_store[-1]                           #Use the latest image from the list
    
    if im_arr.ndim == 3:
        im_temp = cv2.cvtColor(im_arr, cv2.COLOR_BGR2HSV)   #Convert to HSV
        intensity = im_temp[:,:,2]                          #Manipulate the intensity values
    else:      
        intensity = im_arr                         #use the entire array for bw
    size = intensity.shape[0]*intensity.shape[1]   #size for scalinf the cdf 
    hist, bins = np.histogram(intensity.flatten(), 255, range=(0,255), density=True)   #Flatten the array and convert to histogram
    cdf = hist.cumsum()                             #obtain cdf
    cdf_scaled = cdf*size                           #scale the cdf, these are the number of pixels at each
    

    intensity = intensity.astype('uint64')          
    if im_arr.ndim == 3:
        intensity = np.round(255*(cdf_scaled[intensity - 1]- cdf_scaled[np.min(intensity)])/(size - cdf_scaled[np.min(intensity)])) #use the formula
        im_temp[:,:,2] = intensity.astype('uint8')          #convert to uint8
        im_conv_arr = cv2.cvtColor(im_temp, cv2.COLOR_HSV2BGR) #convert to rgb
    else: 
        intensity = np.round(255*(cdf_scaled[intensity - 1]- cdf_scaled[np.min(intensity)])/(size - cdf_scaled[np.min(intensity)]))
        
        im_conv_arr = intensity.astype('uint8') #convert to uint8
        
    
        
    im_conv = Image.fromarray(im_conv_arr)              #Convert back to image
    im_store.append(im_conv_arr)                        #Append the latest transformed image to the list
    tkimage = ImageTk.PhotoImage(im_conv)               #To display image

    image_disp.configure(image = tkimage)               #configure the lable with the image
    image_disp.image = tkimage                          #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center




def convert_negative(im_store):
    """
    This function is to take the negative of the image
    """
    
    im_arr = im_store[-1]                           #Use the latest image from the list
    if im_arr.ndim == 3:
        im_temp = cv2.cvtColor(im_arr, cv2.COLOR_BGR2HSV)   #Convert to HSV
        intensity = im_temp[:,:,2]                          #Manipulate the intensity values
    else:      
        intensity = im_arr                         #use the entire array for bw

    intensity = 255 - intensity
    if im_arr.ndim == 3:                            #if rgb image   
        im_temp[:,:,2] = intensity                  #store the transformed values
        im_conv_arr = cv2.cvtColor(im_temp, cv2.COLOR_HSV2BGR)  #Convert back to RGB                        
    else:
        im_conv_arr = intensity                     #if BW no conversion needed

    im_conv = Image.fromarray(im_conv_arr)              #Convert back to image
    im_store.append(im_conv_arr)                        #Append the latest transformed image to the list
    tkimage = ImageTk.PhotoImage(im_conv)               #To display image

    image_disp.configure(image = tkimage)               #configure the lable with the image
    image_disp.image = tkimage                          #display the image
    image_disp.place(relx=0.5, rely=0.5, anchor=CENTER) #place the image in the center
    

#Load image button
open_button = tk.Button(
    window,
    text = "Load an image",
    command = select_file
)
open_button.place(relx=0.5, rely=0.2, anchor=CENTER)
entry = tk.Entry()
window.mainloop()
