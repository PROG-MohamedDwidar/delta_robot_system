from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import numpy as np
import pandas as pd
#options = Options()
#service = FFService(executable_path='/home/dwidar/Desktop/dataGen/geckodriver')
print("Starting")
driver = webdriver.Chrome()
print("Started")
driver.get("https://www.marginallyclever.com/other/samples/fk-ik-test.html")

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "f"))
    )
finally:
    pass
# input in field with id f 115
base = driver.find_element(By.ID, "f")
bass = driver.find_element(By.ID, "e")
bicep = driver.find_element(By.ID, "rf")
forearm = driver.find_element(By.ID, "re")
baseToFloor = driver.find_element(By.ID, "b")
x = driver.find_element(By.ID, "x")
y = driver.find_element(By.ID, "y")
z = driver.find_element(By.ID, "z")
t1 = driver.find_element(By.ID, "t1")
t2 = driver.find_element(By.ID, "t2")
t3 = driver.find_element(By.ID, "t3")

base.clear()
bass.clear()
bicep.clear()
forearm.clear()
baseToFloor.clear()

base.send_keys("70") #f
bass.send_keys("35") #e
bicep.send_keys("115") #rf
forearm.send_keys("340") #re
baseToFloor.send_keys("407") #b

def IK(xv,yv,zv):
    x.clear()
    y.clear()
    z.clear()
    x.send_keys(xv)
    y.send_keys(yv)
    z.send_keys(zv)
    ls=[]
    ls.append(t1.get_attribute("value"))
    ls.append(t2.get_attribute("value"))
    ls.append(t3.get_attribute("value"))
    return ls

#create a pandas dataframe with the columns x,y,z,t1,t2,t3
df = pd.DataFrame(columns=['x','y','z','t1','t2','t3'])

#generate a 100000 random values for x (-91.113 to 91.113 mm), y (-91.113 to 91.113 mm) , z (-407 to -224.773 mm)
xvec= np.random.uniform(-220.00,220.00,200000)
yvec = np.random.uniform(-220.00,220.00,200000)
zvec = np.random.uniform(-450,-224.00,200000)

#iterate over the generated values calling the IK function and appending the results to the dataframe
for i in range(200000):
    ls = IK(xvec[i],yvec[i],zvec[i])
    #if all ls is zeros
    if ls[0] == '0' and ls[1] == '0' and ls[2] == '0':
        continue

    df = df._append({'x':xvec[i],'y':yvec[i],'z':zvec[i],'t1':ls[0],'t2':ls[1],'t3':ls[2]},ignore_index=True)
    #print(i)

#save the dataframe to a csv file
#remove any rows with NaN values
df.dropna(inplace=True)

df.to_csv('data2.csv',index=False)
time.sleep(5)