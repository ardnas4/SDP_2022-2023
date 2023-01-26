import os
 
os.chdir('C:/Users/chibi/OneDrive/GitHub/SDP_2022-2023/tpc-imgs/nontoxic_images/Virginia_Creeper')
print(os.getcwd())

name = 2157
 
for f in os.listdir():
    f_name = str(name)
 
    new_name = f'{f_name}.jpg'
    os.rename(f, new_name)

    name += 1

    if name > 2156:
        break

print("Done!")