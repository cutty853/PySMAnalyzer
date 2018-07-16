# Analyzer
the analyzer class is a special entity representing the main program.

## The class
```python
class Analyzer:
    def __init__(self, sm_input, rules_input):
        self.xml_parser = etree.XMLParser(remove_comments=True)

        # Trees
        self.sm_tree = etree.parse(sm_input, parser=self.xml_parser)
        self.rules_tree = etree.parse(rules_input, parser=self.xml_parser)

        # Entity
        self.files = set()
        self.report = None
```
### Attributes
- `sm_tree` is the source monitor raw tree
- `rules_tree` is the xml tree of your rules to analyze the source monitor report
- `files` is a set of `File` objet
- `report` attribute will be filled with the `Report` object when calling the  `Analyzer.make_report` method. This last method won't do anything (except from loading the HTML and XML Reporter) if you don't fill the `Analyzer.files` attribute. You can do it with the `Analyzer.load_files` method.

### Constructor arguments
- `sm_input` and `rules_input` are the strings corresponding to the source monitor and the rules path and filenames

## Things to do
The `Analyzer` class is the "public interface" of PySMAnalyzer, you can print all the bad files, functions or both (`print_bad_files`, `print_bad_functions`, `print_bad_entities`). You can also save the report in a file (`save_report`)

```python
>>> import analyzer
>>> a = analyzer.Analyzer("samples/sample.xml", "samples/rules_sample.xml")
>>> # extract all the files object from the source monitor report
>>> a.load_files()
>>> # analyze the files set and make a report of the bad entities
>>> a.make_report()
>>> # print all the bad entities (files and functions) found by the analyzer
>>> # according to your rules
>>> a.print_bad_entities()
>>> # save the report in html or xml format (here html)
>>> a.save_report("psma_report.html", method="html")
>>> # the report will be place in the html directory
>>> print(analyzer.HTML_BASE_DIRECTORY)
>>> 'hmlt/'
```
