import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from py3dbp import Packer, Bin, Item, Painter



# Box dimensions
BOX_DIMENSIONS = {
    "A": (12, 8.6, 8.8),
    "B": (16.5, 12.5, 8.5),
    "C": (22, 15, 9.3),
    "F": (24.5, 18.5, 13.5)
}
BOX_WEIGHT = {
    "A": 0.4,
    "B": 0.8,
    "C": 1.2,
    "F": 1.6
}

def draw_big_box(ax, w, h, d):
    big_box_vertices = [
        [0, 0, 0],
        [w, 0, 0],
        [w, h, 0],
        [0, h, 0],
        [0, 0, d],
        [w, 0, d],
        [w, h, d],
        [0, h, d]
    ]

    big_box_faces = [
        [big_box_vertices[0], big_box_vertices[1], big_box_vertices[5], big_box_vertices[4]],
        [big_box_vertices[1], big_box_vertices[2], big_box_vertices[6], big_box_vertices[5]],
        [big_box_vertices[2], big_box_vertices[3], big_box_vertices[7], big_box_vertices[6]],
        [big_box_vertices[3], big_box_vertices[0], big_box_vertices[4], big_box_vertices[7]],
        [big_box_vertices[4], big_box_vertices[5], big_box_vertices[6], big_box_vertices[7]]
    ]

    big_box_collection = Poly3DCollection(big_box_faces, edgecolor='k', alpha=0.1)
    ax.add_collection3d(big_box_collection)

"""def calculate_fit():
    small_box_sizes = []
    holding_box_size = BOX_DIMENSIONS[holding_box_var.get()]
    items = small_box_listbox.get(0, tk.END)

    # Loop through the items
    for item in items:
        
        dimensions = [float(item.split(',')[i]) for i in range(3)]
        print(dimensions)
        small_box_sizes.append(dimensions)
    


    total_volume = sum(x * y * z for x, y, z in small_box_sizes)
    holding_box_volume = holding_box_size[0] * holding_box_size[1] * holding_box_size[2]

    if total_volume <= holding_box_volume:
        result_label.config(text="Boxes fit!")
    else:
        result_label.config(text="Boxes do not fit.")"""


def update_holding_box_dropdown():
    holding_box_dropdown['menu'].delete(0, 'end')  # Clear existing options

    for box_name in BOX_DIMENSIONS.keys():
        holding_box_dropdown['menu'].add_command(label=box_name, command=tk._setit(holding_box_var, box_name))


def add_holding_box_popup():
    popup = tk.Toplevel(root)
    popup.title("Add Holding Box")

    # Label and entry for holding box name
    name_label = tk.Label(popup, text="Holding Box Name:")
    name_label.grid(row=0, column=0)

    name_entry = tk.Entry(popup)
    name_entry.grid(row=0, column=1)

    # Label and entry for holding box size
    size_label = tk.Label(popup, text="Holding Box Size (W,H,D):")
    size_label.grid(row=1, column=0)

    size_entry = tk.Entry(popup)
    size_entry.grid(row=1, column=1)

    # Label and entry for holding box weight
    weight_label = tk.Label(popup, text="Holding Box Weight:")
    weight_label.grid(row=2, column=0)

    weight_entry = tk.Entry(popup)
    weight_entry.grid(row=2, column=1)

    def save_holding_box():
        holding_box_name = name_entry.get()
        holding_box_size = [float(dim) for dim in size_entry.get().split(',')]
        holding_box_weight = float(weight_entry.get())

        BOX_DIMENSIONS[holding_box_name] = tuple(holding_box_size)
        BOX_WEIGHT[holding_box_name] = holding_box_weight

        update_holding_box_dropdown()  # Update the dropdown options

        holding_box_var.set(holding_box_name)  # Set the selected box to the newly added one

        popup.destroy()

    # Save button
    save_button = tk.Button(popup, text="Save", command=save_holding_box)
    save_button.grid(row=3, columnspan=2)



def do_Clear():
    
    small_box_listbox.delete(0,tk.END)
    result_label.config(text=" ")
    weight_label.config(text=" ")
    small_box_entry.delete(0, tk.END)
    small_box_count.delete(0, tk.END)
    



   


def render_fit():
    holding_box_size = BOX_DIMENSIONS[holding_box_var.get()]
    packer = Packer()
    #  init bin 
    box = Bin('Packing', (holding_box_size[0], holding_box_size[1], holding_box_size[2]), 100,0,put_type=0)
    packer.addBin(box)
    pack_weight=float(0.0)
    
    hbox_weight= BOX_WEIGHT[holding_box_var.get()]
    

    small_box_sizes = []
    items = small_box_listbox.get(0, tk.END)

    # Loop through the items
    j=0
    for item in items:
        j=j+1
        dimensions = [float(item.split(',')[i]) for i in range(4)]
        pack_weight = pack_weight + dimensions[3]
        print(dimensions)
        #small_box_sizes.append(dimensions)
        packer.addItem(Item(partno='Box-{0}'.format(j),name='test',typeof='cube', WHD=(dimensions[0], dimensions[1], dimensions[2]), weight=float(dimensions[3]), level=1,loadbear=100, updown=True, color='yellow'))

    # calculate packing 
    packer.pack(
        bigger_first=True,
        distribute_items=False,
        fix_point=True,
        check_stable=True,
        support_surface_ratio=0.75,
        number_of_decimals=0
    )



    # print result
    b = packer.bins[0]
    volume = b.width * b.height * b.depth
    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    volume_t = 0
    volume_f = 0
    unfitted_name = ''
    for item in b.items:
        print("partno : ",item.partno)
        print("color : ",item.color)
        print("position : ",item.position)
        print("rotation type : ",item.rotation_type)
        print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
        print("volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("weight : ",float(item.weight))
        volume_t += float(item.width) * float(item.height) * float(item.depth)
        print("***************************************************")
    print("***************************************************")
    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("partno : ",item.partno)
        print("color : ",item.color)
        print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
        print("volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("weight : ",float(item.weight))
        volume_f += float(item.width) * float(item.height) * float(item.depth)
        unfitted_name += '{},'.format(item.partno)
        print("***************************************************")
    print("***************************************************")
    print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
    print('residual volumn : ', float(volume) - volume_t )
    print('unpack item : ',unfitted_name)
    print('unpack item volumn : ',volume_f)
    print("gravity distribution : ",b.gravity)
    print('pack weight: ',pack_weight)
    if volume_f>0 :
        result_label.config(text="Boxes do not fit.")
    else:
        result_label.config(text="Boxes fit!")
    
    weight_label.config(text="LB{0}".format(pack_weight+hbox_weight))



    # draw results
    painter = Painter(b)
    fig = painter.plotBoxAndItems(
        title=b.partno,
        alpha=0.8,
        write_num=False,
        fontsize=10
    )
    fig.show()










# Initialize the main window
root = tk.Tk()

root.title("Holding Box Size Calculator")

# Label and entry for holding box size
holding_box_label = tk.Label(root, text="Holding Box Size (W,H,D,Weight):")
holding_box_label.grid(row=0, column=0)

# Holding box selection
holding_box_var = tk.StringVar(root)
holding_box_var.set("A")  # Set default selection
holding_box_dropdown = tk.OptionMenu(root, holding_box_var, *BOX_DIMENSIONS.keys())
#holding_box_dropdown.pack()
holding_box_dropdown.grid(row=0, column=1)

# Listbox for small box sizes
small_box_listbox = tk.Listbox(root)
small_box_listbox.grid(row=1, column=0)
add_holding_box_button = tk.Button(root, text="Add Holding Box", command=add_holding_box_popup)
add_holding_box_button.grid(row=1, column=1)


# Function to add small box size
def add_small_box_size():
    small_box_size = small_box_entry.get()
    box_count = small_box_count.get()

    for x in range(int(box_count)):
        small_box_listbox.insert(tk.END, small_box_size)

    small_box_entry.delete(0, tk.END)  # Clear the entry field
    small_box_count.delete(0, tk.END)


def remove_small_box_size():
    selected_indices = small_box_listbox.curselection()
    # Remove the selected items from the Listbox
    for index in reversed(selected_indices):
        small_box_listbox.delete(index)


# Label and entry for small box size
small_box_label = tk.Label(root, text="Small Box Size (W,H,D,Weight):")
small_box_label.grid(row=2, column=0)

small_box_entry = tk.Entry(root)
small_box_entry.grid(row=2, column=1)
small_box_count = tk.Entry(root)
small_box_count.grid(row=2, column=2)

# Button to add small box size
add_button = tk.Button(root, text="Add Small Box", command=add_small_box_size)
add_button.grid(row=3, column=0)
add_button = tk.Button(root, text="Remove Small Box", command=remove_small_box_size)
add_button.grid(row=3, column=1)


# Calculate button
#calculate_button = tk.Button(root, text="Calculate", command=calculate_fit)
#calculate_button.grid(row=4, column=0)
clear_button = tk.Button(root, text="Clear", command=do_Clear)
clear_button.grid(row=4, column=0)
calculate_button = tk.Button(root, text="Render", command=render_fit)
calculate_button.grid(row=4, column=1)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0)
weight_label = tk.Label(root, text="")
weight_label.grid(row=5, column=1)

# Run the GUI
root.mainloop()
