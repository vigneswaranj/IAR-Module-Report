# =====================================================================
#   IAR List File Report Generator
# =====================================================================
import plotly
import plotly.graph_objs as gra
from array import *
from plotly.graph_objs import Scatter, Layout, Figure
import plotly.plotly as py

Row = 0
Column = 0
# =====================================================================
#   ModuleReport - Class definition
# =====================================================================
class ModuleReport():

    def __init__(self):
        self.datatable = ""
        self.Row = 0
        self.InputFile = ""
        self.NumOfColumn = 2
        self.ExtractFileName ="Module_Extract.txt"
# =====================================================================
#   Parse function/variable name and size
# =====================================================================
    def _plotgraph(self, Row, datatable):
        self.Row        = Row
        self.datatable  = datatable

        Bx = [0]*self.Row 
        By = array('i', [0]*self.Row )
            
        for Row in range (1,self.Row):
            Bx[Row-1] = self.datatable[Row,0]
            By[Row-1] = int(self.datatable[Row,1])

        trace1  = gra.Bar(x=Bx, y=By, name='Bytes')
        data    = [trace1]

        layout  = Layout(title='IAR List File Analyser' )
        fig     = Figure(data=data,layout=layout)

        plotly.offline.plot(fig, filename='IAR Module Report - ' + self.InputFile.replace(".lst","") + ".html")

# =====================================================================
#   Extract Segment Part Size information
# =====================================================================
    def _extractSizeInfo(self, inputfilename):
        self.InputFile  = inputfilename
        filelist = open(self.InputFile, 'r')
        resultfile = open(PlotReport.ExtractFileName, 'w')

        start = 0

        previousline = ""

        for eachline in filelist:
            if(eachline.find("Function/Label") != -1):
                start = 1
            if(eachline.find("bytes in")  != -1):
                start = 0
            if start == 1:
                if (eachline.find("-----") == -1):             
                    if(eachline.find("                              ") != -1):
                        tempstring = previousline.replace('\n','') + eachline
                        resultfile.write(tempstring)  
                        previousline = ""
                    else:
                        resultfile.write(previousline)                
                        previousline = eachline

        resultfile.close()
        filelist.close()
# =====================================================================
#   ModuleReport - End of Class definition
# =====================================================================

# =====================================================================
#   Main function
# =====================================================================
if __name__ == "__main__":
    import argparse
	#Receive and parse the arguments
    parser = argparse.ArgumentParser(description="Extracts information from IAR List file and plot graph.")
    parser.add_argument("listfile", help="List file to parse.")
    args = parser.parse_args()

    if args.listfile == "":
        exit(0)
	
	#Start Parsing list file 
    PlotReport = ModuleReport()
    PlotReport._extractSizeInfo(args.listfile)

    resultfile = open(PlotReport.ExtractFileName, 'r')
    FilteredString = [0]  * PlotReport.NumOfColumn
    SizeTable = {}
	#Search and find the module summary in list file
    for eachline in resultfile:
        if (eachline.find("-----") == -1):
            TempString = eachline.replace('\n','')
            TempString = TempString.split(" ")
            elementID = 0
            for eachstring in TempString:                
                if(eachstring != "") :
                    FilteredString[elementID] = eachstring
                    elementID = elementID +1

            for eachtempstring in TempString:
                if(eachtempstring != ""):
                    SizeTable[Row,Column] = eachtempstring
                    Column = Column + 1

            Row = Row + 1
            Column = 0

    resultfile.close()
	#Plot graph with the extracted information
    PlotReport._plotgraph(Row-1, SizeTable)
# =====================================================================
#   End of File
# =====================================================================
