# HOWTO: create rules file
Creating rules is simple. First of all, a rule file contains two main parts:
```xml
<rules>
  <default>
    <files></files>
  </default>
  <specific>
    <files></files>
  </specific>
</rules>
```
1. `default`: the rules used when no specific rules was specified for an entity (file or function)
2. `specific`: all the rules for a file or a function directly named

**NOTE:** at this time, there is no way to be general in the specific rules section (no joker or whatever), so it can be tedious to fill this part. Work In Progress and I'd be happy if someone would contribute on that part.

## default rules part
```xml
<default>
    <files>
        <metrics metric_count="13">
            <metric id="M0">0</metric>
            <metric id="M1">0</metric>
            <metric id="M2">0</metric>
            <metric id="M3">0</metric>
            <metric id="M4">0</metric>
            <metric id="M5">0</metric>
            <metric id="M6">0</metric>
            <metric id="M7">disable</metric>
            <metric id="M8">0</metric>
            <metric id="M9">0</metric>
            <metric id="M10">0</metric>
            <metric id="M11">0</metric>
            <metric id="M12">0</metric>
        </metrics>
        <function_metrics>
            <complexity>10</complexity>
            <statements>disable</statements>
            <maximum_depth>disable</maximum_depth>
            <calls>disable</calls>
        </function_metrics>
    </files>
</default>
```
Everything must be specified and complete in the default rules section. You can also by default disable metrics by setting them to *0* or by writing *disable* in the section of your choice

## specific rules part
```xml
<specific>
  <files>
    <file name="STV\Trieuse\stv\src\ttpdsext.c">
      <metrics metric_count="13">
        <metric id="M0">disable</metric>
        <metric id="M1">disable</metric>
        <metric id="M2">disable</metric>
        <metric id="M3">1</metric>
        <metric id="M4">disable</metric>
        <metric id="M9">disable</metric>
        <metric id="M10">disable</metric>
        <metric id="M11">disable</metric>
        <metric id="M12">disable</metric>
      </metrics>
      <function_metrics>
          <function name="initttpdsext()">
              <complexity>5</complexity>
          </function>
      </function_metrics>

    </file>
  </files>
</specific>
```
You can also specify the name of a file or a function from a file. So you'll have to create a fele section with the `file` tag. This section can (but not necessary) contains two sub-section: `function_metrics` and a `metrics` section. In the last one you can indicate your specific rules for the file itself. The `function_metrics` state your specific rules for each function of the file. You muse use a `function` tag to name the function. **function's name must end with parenthesis** ! Then within the `function` tag, you can use `complexity`, `statements`, `maximum_depth`, `calls` metrics tags.

## Improvements
You are free to present your improvements for the rules section in the github issues ! :)
