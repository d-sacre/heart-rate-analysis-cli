import sys

# loading of non-standard modules in sub-folders
import importlib.util

# source: https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

# Loading of non-standard modules
clio = module_from_file("commandline_io", "./modules/commandline_io.py")
fio = module_from_file("file-io-handler", "./modules/file-io-handler.py")
parsing = module_from_file("data_parsing", "./modules/data_parsing.py")
convert = module_from_file("convert", "./modules/convert.py")
analysis = module_from_file("data-analysis", "./modules/data-analysis.py")
plot = module_from_file("plotter_matplotlib", "./modules/plotter_matplotlib.py")

# settings = {
#     "import": 
#     {
#         # "filepath": "test-data_withings-style.csv",
#         "filepath": "/home/mane/projects/withings/2022-01-12/raw_hr_hr.csv",
#         # "filepath": "/home/mane/projects/withings/2022-07-10/raw_hr_hr.csv",
#         "datatype": "csv",
#         "dataformat": "withings"
#     },
#     "export":
#     {
#         "directory": "/home/mane/cli-test/"
#     }
# }

# Code execution
if __name__ == "__main__":

    # Only run the program if Python 3.10.x or higher is present (requirement for usage of "match" statement)
    # Otherwise exit with error message
    if sys.version_info >= (3,10,0): 

        settings = fio.loadSettingsJSON()
        settings = clio.readCommandlineArguments(sys.argv[1:], settings)

        # Loading, parsing and pre-processing of data
        importedData = fio.loadFile(settings["import"]["filepath"],settings["import"]["datatype"])
        rawDataStandardized = parsing.formatDataToStandard(importedData,settings["import"]["datatype"],settings["import"]["dataformat"])
        completeRawDataDictionary = convert.ArrayToDict(rawDataStandardized)

        # Perform data analysis
        heartRateDataDailyAnalysis, heartRateDataDailyExtrema = analysis.heartRate_minMaxAvg(completeRawDataDictionary)

        # Convert data into more suitable format for plotting/(raw) data export
        date, minimum, average, maximum = convert.DictToPlotArray(heartRateDataDailyAnalysis) 
        completeRawData24hPlotArray = convert.DictTo24hPlotArray(completeRawDataDictionary)

        # Init export folders
        exportPaths = fio.createPlotAndDataExportFileStructure(settings["export"]["directory"])

        # Plot the data
        plot.plotHeartRate24hForAllDays(completeRawData24hPlotArray,exportPaths["singleDays"])
        plot.plotHeartRateExtremaOverHoursOfDay(date, minimum, maximum, exportPaths["minMax"])
        plot.generateAndPlotMonthlyHeartRateTendency(heartRateDataDailyAnalysis,exportPaths["monthlyTendency"])
    
    else:
        _errorString = "Fatal Error: The detected Python installation is version " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + ". This program requires Python 3.10 or higher to function properly."
        print(_errorString)
