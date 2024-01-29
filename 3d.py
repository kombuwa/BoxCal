from py3dbp import Packer, Bin, Item, Painter


packer = Packer()

packer.addBin(Bin('small-envelope', 11.5, 6.125, 0.25, 10))
packer.addBin(Bin('large-envelope', 15.0, 12.0, 0.75, 15))
packer.addBin(Bin('small-box', 8.625, 5.375, 1.625, 70.0))
packer.addBin(Bin('medium-box', 11.0, 8.5, 5.5, 70.0))
packer.addBin(Bin('medium-2-box', 13.625, 11.875, 3.375, 70.0))
packer.addBin(Bin('large-box', 12.0, 12.0, 5.5, 70.0))
packer.addBin(Bin('large-2-box', 23.6875, 11.75, 3.0, 70.0))

packer.addItem(Item('50g [powder 1]', 3.9370, 1.9685, 1.9685, 1))
packer.addItem(Item('50g [powder 2]', 3.9370, 1.9685, 1.9685, 2))
packer.addItem(Item('50g [powder 3]', 3.9370, 1.9685, 1.9685, 3))
packer.addItem(Item('250g [powder 4]', 7.8740, 3.9370, 1.9685, 4))
packer.addItem(Item('250g [powder 5]', 7.8740, 3.9370, 1.9685, 5))
packer.addItem(Item('250g [powder 6]', 7.8740, 3.9370, 1.9685, 6))
packer.addItem(Item('250g [powder 7]', 7.8740, 3.9370, 1.9685, 7))
packer.addItem(Item('250g [powder 8]', 7.8740, 3.9370, 1.9685, 8))
packer.addItem(Item('250g [powder 9]', 7.8740, 3.9370, 1.9685, 9))

packer.pack()

"""for b in packer.bins:
    print(":::::::::::", b.string())

    print("FITTED ITEMS:")
    for item in b.items:
        print("====> ", item.string())

    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("====> ", item.string())

    print("***************************************************")
    print("***************************************************")"""
# paint the results
for b in packer.bins:
    painter = Painter(b)
    fig = painter.plotBoxAndItems(
        title=b.partno,
        alpha=0.2,         
        write_num=True,   
        fontsize=10        
    )
fig.show()