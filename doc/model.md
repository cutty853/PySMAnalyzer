# Models in PySMA
Here you can find the model used in the package.  

## Entities
Several entities are used in the package

### files
A file has multiple attribute
```python
class File:
    """docstring for File."""
    def __init__(self, name):
        self.name = name
        self.metrics = None
        self.rules = None
        self.validity = True
        self.functions = set()
```
The `name` attribute represent the name of the file.  
The `metrics` are the data extracted from the source monitor report, it's a `FileMetrics` object and it's loaded by calling the `File.load_metrics` method.  
Thre `rules` are extracted from the rules files provided in the command line and are used to check the validity of the file's metrics, it's also a `FileMetric` object and it's loaded by calling the `File.load_rules` method.  
`validity` is updated according to rules and metrics. It's at False if the metrics don't match the rules. Validity can be loaded by calling the `File.check_validity` method, it will raise a TypeError if metrics and rules are not loaded (if they are at None).  
Finally, the `functions` are all function contained in a file. It's loaded by calling  the `File.load_functions` method. This attribute is a set of `Function` type object.  

There is a method `File.load`, which allow to do all the processing describe above. It will in fact also load all the metrics, rules and validity for the functions.  

### functions
A file has the following attributes
```python
class Function:
    """ Represent source-monitor function object """
    def __init__(self, source_file, name):
        self.source_file = source_file
        self.name = name
        self.metrics = None
        self.rules = None
        self.validity = True
```
The `name` attribute represents the name of the function and the `source_file` attribute represents the name of the file from which the function comes.  
The `metrics` are the data extracted from the source monitor report, it's a `FunctionMetrics` object and it's loaded by calling the `Function.load_metrics` method.  
Thre `rules` are extracted from the rules files provided in the command line and are used to check the validity of the file's metrics, it's also a `FunctionMetric` object and it's loaded by calling the `Function.load_rules` method.  
`validity` is updated according to rules and metrics. It's at False if the metrics don't match the rules. Validity can be loaded by calling the `Function.check_validity` method, it will raise a TypeError if metrics and rules are not loaded (if they are at None).  

### metrics
The program has two types of metrics, those for file and those for functions. These class are made to clearly define what the program manipulate.

#### FileMetrics
This class define the metrics for a file, it's just a dictionnary. We can get and set metrics values with the `FileMetrics.get` and the `FileMetrics.set` methods.

#### FunctionMetrics
This class define the metrics for a function. It's composed of the 4 function metrics available in source monitor (complexity, statements, maximum_depth, calls).  
Setter for each of those metrics is available.  

### reports
A report is class generated by the PySMA program. It reference all the files that have bad metrics and also all the functions that have bad metrics.  
A report can be converted into multiple format by calling the method named by the format name (for example to convert the report in html call the `Report.html` method).  
For the moment only xml and html conversion are available.  

The report has two behavior.
1. **Specify files set at initialisation:** If you specify all the files (all the `File` object extracted from a source monitor report) at initialisation, the report will be able to load itself (take out all the non valide `File` and `Function` object of the files set). You will then be able to directly convert the report into html or xml.
2. **Init the report and fill it later:** If you specify the files set after creating a report object, you will have to load the report by calling the `Report.make_report` before using it or converting it.

## Other software parts
Beyond the use of different entity (object), the program also use packages to divide up the code.  

### reader
The reader package define what I call "finders", they are used to clearly define XPath usage with the lxml.etree package.  

### writer
The writer package define the class used to write a report into an output file.  
An output file has a format (xml or html) and need to contains all the report informations, we must be able to recreate a report (without the files set attribute) from those output file, that is to say those informations:
1. Amount of bad files
2. Amount of bad functions
3. The amount of bad functions in the worst file of the project (the one to focus on)
4. All the bad files
5. All the bad functions with their source_file name (using a tree for example)
