import sys, os
pwd=os.getcwd()
# sys.path.insert(0, pwd+'\lib\NUMPY64BIT')
# sys.path.insert(0, pwd+'\lib\PYGAME')
sys.path.insert(0, pwd+'\lib\PGU')
# sys.path.insert(0, pwd+'\lib\LEAPMOTION')
sys.path.insert(0, pwd+'\lib\LEAP2')
# sys.path.insert(0,'\impl\data' )
# import src.impl.gui.mainWindow as MW
import src.impl.gui.mainWindow as MW



# x=np.array([[0.2, 0.3],[0.5, 0.8]])

myMW=MW.mainWindow()



# dataTabs.run()
